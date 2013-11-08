""" Bunch of helping classes and functions """
from multiprocessing import Process, Queue

import logging
LOGGER = logging.getLogger(__name__)


def help_wrapper(messages, msg_ids):
    """ helps to format messages output """
    rez = list(messages) if msg_ids == 'All'else \
        [msg for msg in messages if msg['id'] in msg_ids]
    for msg in rez:
        msg['page'] = ""
        msg['msg'] = msg['help']
    return rez


def processes_wrapper(queue, funk, kwargs):
    """ helper for getting results from different processes """
    try:
        rez = funk(**kwargs)
        queue.put(rez)
    # there is a need to catch all possible exceptions
    except Exception, msg:  # pylint: disable=W0703
        LOGGER.error(msg)
        queue.put([])


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
            for checker_rez in queues:
                for rez in checker_rez.get():
                    yield rez
