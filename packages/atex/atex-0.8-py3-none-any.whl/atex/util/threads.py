import collections
import queue
import threading

# TODO: documentation; this is like concurrent.futures, but with daemon=True support


class ThreadQueue:
    ThreadReturn = collections.namedtuple("ThreadReturn", ("thread", "returned", "exception"))
    Empty = queue.Empty

    def __init__(self, daemon=False):
        self.queue = queue.SimpleQueue()
        self.daemon = daemon
        self.threads = set()

    def _wrapper(self, func, *args, **kwargs):
        current_thread = threading.current_thread()
        try:
            ret = func(*args, **kwargs)
            result = self.ThreadReturn(current_thread, ret, None)
        except Exception as e:
            result = self.ThreadReturn(current_thread, None, e)
        self.queue.put(result)

    def start_thread(self, target, name=None, args=None, kwargs=None):
        args = args or ()
        kwargs = kwargs or {}
        t = threading.Thread(
            target=self._wrapper,
            name=name,
            args=(target, *args),
            kwargs=kwargs,
            daemon=self.daemon,
        )
        t.start()
        self.threads.add(t)

    # get one return value from any thread's function, like .as_completed()
    # or concurrent.futures.FIRST_COMPLETED
    def get(self, block=True, timeout=None):
        if block and timeout is None and not self.threads:
            raise AssertionError("no threads are running, would block forever")
        treturn = self.queue.get(block=block, timeout=timeout)
        self.threads.remove(treturn.thread)
        if treturn.exception is not None:
            raise treturn.exception
        else:
            return treturn.returned

    # wait for all threads to finish (ignoring queue contents)
    def join(self):
        while self.threads:
            t = self.threads.pop()
            t.join()
