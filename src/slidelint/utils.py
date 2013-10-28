from multiprocessing import Process, Queue

def help(messages, msg_ids):
    rez = list(messages) if msg_ids == 'All'else \
        [m for m in messages if m['id'] in msg_ids]
    for m in rez:
        m['page'] = ""
        m['msg'] = m['help']
    return rez


class MultiprocessingManager():
    """ class for handling multiprocessing run """
    def __init__(self, debug=False):
        self.poll = []
        self.debug = debug

    def append(self, func, kwargs):
        self.poll.append((func, kwargs))

    def wrapper(self, queue, funk, kwargs):
        try:
            rez = funk(**kwargs)
            queue.put(rez)
        except Exception, msg:
            logger.error(msg)
            queue.put([])

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
                processes.append(Process(target=self.wrapper, args=(queue, func, kwargs)))
                queues.append(queue)
            for p in processes:
                p.start()
            for checker_rez in queues:
                for rez in checker_rez.get():
                    yield rez
