import concurrent.futures
import logging
import threading
import time
import util.cached


_size = 20


@util.cached.func
def _pool():
    logging.debug('new thread pool, size: %s', _size)
    return concurrent.futures.ThreadPoolExecutor(_size)


def new(fn, *a, **kw):
    daemon = kw.pop('_daemon', True)
    obj = threading.Thread(target=fn, args=a, kwargs=kw)
    obj.daemon = daemon
    obj.start()
    return obj


def _unpack(fn):
    args, kwargs = [], {}
    if not callable(fn):
        try:
            fn, args = fn
        except ValueError:
            fn, args, kwargs = fn
    return fn, args, kwargs


def wait(*fns, max_threads=None):
    if max_threads:
        with concurrent.futures.ThreadPoolExecutor(max_threads) as pool:
            concurrent.futures.wait([pool.submit(fn, *a, **kw) for fn, a, kw in map(_unpack, fns)])
    else:
        for thread in [new(fn, *a, **kw) for fn, a, kw in map(_unpack, fns)]:
            thread.join()


def submit(fn, *a, **kw):
    return _pool().submit(fn, *a, **kw)


def supervise(*fns, sleep=1):
    threads = [new(fn, *a, **kw) for fn, a, kw in map(_unpack, fns)]
    while True:
        assert all(thread.is_alive() for thread in threads)
        time.sleep(sleep)
