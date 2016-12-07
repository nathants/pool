import concurrent.futures
import time
import logging
import multiprocessing
import util.cached


_size = multiprocessing.cpu_count() + 2


@util.cached.func
def _pool():
    logging.debug('new process pool, size: %s', _size)
    return concurrent.futures.ProcessPoolExecutor(_size)


def new(fn, *a, **kw):
    daemon = kw.pop('_daemon', True)
    obj = multiprocessing.Process(target=fn, args=a, kwargs=kw)
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


def as_completed(*fns, max_procs=_size):
    with concurrent.futures.ProcessPoolExecutor(max_procs) as pool:
        for f in concurrent.futures.as_completed([pool.submit(fn, *a, **kw) for fn, a, kw in map(_unpack, fns)]):
            yield f.result()


def wait(*fns, max_procs=None):
    if max_procs:
        with concurrent.futures.ProcessPoolExecutor(max_procs) as pool:
            concurrent.futures.wait([pool.submit(fn, *a, **kw) for fn, a, kw in map(_unpack, fns)])
    else:
        for proc in [new(fn, *a, **kw) for fn, a, kw in map(_unpack, fns)]:
            proc.join()


def submit(fn, *a, **kw):
    return _pool().submit(fn, *a, **kw)


def map(fn, *iterables):
    return _pool().map(fn, *iterables)


def supervise(*fns, sleep=1):
    procs = [new(fn, *a, **kw) for fn, a, kw in map(_unpack, fns)]
    while True:
        assert all(proc.is_alive() for proc in procs)
        time.sleep(sleep)
