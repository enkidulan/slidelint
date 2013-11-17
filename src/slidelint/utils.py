""" Bunch of helping classes and functions """
from multiprocessing import Process, Queue

import logging
LOGGER = logging.getLogger(__name__)


def encoding_normalazer(messages):
    """ encodes message report text to utf-8 """
    for msg in messages:
        for key, value in msg.items():
            if isinstance(value, basestring):
                value = value.encode('utf-8')
            msg[key] = value
    return messages


def provide_help(messages, msg_ids):
    """ helps to format messages output """
    rez = list(messages) if msg_ids == 'All'else \
        [msg for msg in messages if msg['id'] in msg_ids]
    for msg in rez:
        msg['page'] = ""
        msg['msg'] = msg['help'].encode('utf-8')
        msg['help'] = msg['help'].encode('utf-8')
    return rez


def help_wrapper(messages):
    """ decorator for providing help messages (arguments allowing trick)"""
    def help_decorator(function):
        """ real decorator """
        def wrapped(**kargs):
            """ actual wrapper that returns help messages if msg_info are
            present into function args"""
            msg_info = kargs.get('msg_info', None)
            if msg_info:
                return provide_help(messages, msg_info)
            return encoding_normalazer(function(**kargs))
        return wrapped
    return help_decorator


def processes_wrapper(queue, funk, kwargs):
    """ helper for getting results from different processes """
    try:
        rez = funk(**kwargs)
        queue.put(rez)
    # there is a need to catch all possible exceptions
    except Exception, msg:  # pylint: disable=W0703
        info = "The function '%s' of '%s' module "\
               "raised an Exception:\n" % (funk.__name__, funk.__module__)
        queue.put(info + msg.message)


class MultiprocessingManager(object):
    """ class for handling multiprocessing run """
    def __init__(self, debug=False):
        self.poll = []
        self.debug = debug

    def append(self, func, kwargs):
        """ append function and its args to poll """
        self.poll.append((func, kwargs))

    def __iter__(self):
        if self.debug:
            for func, kwargs in self.poll:
                for rez in func(**kwargs):
                    yield rez
        else:
            queues = []
            processes = []
            for func, kwargs in self.poll:
                queue = Queue()
                processes.append(
                    Process(target=processes_wrapper,
                            args=(queue, func, kwargs)))
                queues.append(queue)
            for process in processes:
                process.start()
            for checker in queues:
                checker_rez = checker.get()
                if isinstance(checker_rez, basestring):
                    raise IOError(checker_rez)
                for rez in checker_rez:
                    yield rez
            for process in processes:
                process.join()
