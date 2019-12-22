import os
import signal
import traceback
import functools

def exceptions_kill_parent(decoratee):
    pid = os.getpid()
    @functools.wraps(decoratee)
    def decorated(*a, **kw):
        try:
            return decoratee(*a, **kw)
        except SystemExit:
            os.kill(pid, signal.SIGTERM)
        except:
            traceback.print_exc()
            os.kill(pid, signal.SIGTERM)
    return decorated
