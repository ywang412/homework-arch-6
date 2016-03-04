import os
import sys
import linecache
import signal
import functools

class TimeoutError(Exception):
    pass

def timeout(seconds, error_message='Function call timed out'):
    def decorated(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return functools.wraps(func)(wrapper)
    return decorated

def trace(f):
    def globaltrace(frame, why, arg):
        if why == 'call':
            return localtrace
        return None
    def localtrace(frame, why, arg):
        if why == 'line':
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            bname = os.path.basename(filename)
            print "{}({}): {}".format(bname, lineno, linecache.getline(filename, lineno))
        return localtrace
    def _f(*ars, **kwargs):
        sys.settrace(globaltrace)
        result = f(*args, **kwargs)
        sys.settrace(None)
        return result
    return _f
