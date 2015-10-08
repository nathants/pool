import concurrent.futures
import logging
import threading
import time
import s.cached


_size = 20


@s.cached.func
def _pool():
    logging.debug('new thread pool, size: %s', _size)
    return concurrent.futures.ThreadPoolExecutor(_size)


def new(fn, *a, **kw):
    daemon = kw.pop('_daemon', True)
    obj = threading.Thread(target=fn, args=a, kwargs=kw)
    obj.daemon = daemon
    obj.start()
    return obj

def _new(fn):
    if callable(fn):
        return new(fn)
    else:
        try:
            fn, *args = fn
            return new(fn, *args)
        except ValueError:
            fn, args, kwargs = fn
            return new(fn, *args, **kwargs)


def wait(*fns):
    for thread in [_new(fn) for fn in fns]:
        thread.join()
    return None


def submit(fn, *a, **kw):
    return _pool().submit(fn, *a, **kw)


def supervise(*fns, sleep=1):
    threads = [_new(fn) for fn in fns]
    while True:
        assert all(thread.is_alive() for thread in threads)
        time.sleep(sleep)
