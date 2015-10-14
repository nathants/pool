import concurrent.futures
import time
import logging
import multiprocessing
import s.cached


_size = multiprocessing.cpu_count() + 2


@s.cached.func
def _pool():
    logging.debug('new process pool, size: %s', _size)
    return concurrent.futures.ProcessPoolExecutor(_size)


def new(fn, *a, **kw):
    daemon = kw.pop('_daemon', True)
    obj = multiprocessing.Process(target=fn, args=a, kwargs=kw)
    obj.daemon = daemon
    obj.start()
    return obj


def _new(fn):
    if callable(fn):
        return new(fn)
    else:
        try:
            fn, args = fn
            return new(fn, *args)
        except ValueError:
            fn, args, kwargs = fn
            return new(fn, *args, **kwargs)


def wait(*fns):
    for proc in [_new(fn) for fn in fns]:
        proc.join()
    return None


def submit(fn, *a, **kw):
    return _pool().submit(fn, *a, **kw)


def supervise(*fns, sleep=1):
    procs = [_new(fn) for fn in fns]
    while True:
        assert all(proc.is_alive() for proc in procs)
        time.sleep(sleep)
