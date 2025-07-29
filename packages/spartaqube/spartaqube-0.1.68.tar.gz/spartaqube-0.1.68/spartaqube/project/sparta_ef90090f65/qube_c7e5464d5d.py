import os
import threading
from threading import Thread
import sys
import queue
import signal
import traceback
from project.logger_config import logger
import ctypes


def sparta_1eafa52b01(thread):
    """Terminates a python thread from another thread.:param thread: a threading.Thread instance
    """
    if not thread.isAlive():
        return
    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError('nonexistent thread id')
    elif res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError('PyThreadState_SetAsyncExc failed')


class TimeoutError(Exception):
    pass


class FailedProcess:
    """
        In order to catch an error in the code we are running, we are returning this object so that we can control the 
        type and raise an exception with the exceptionMsg
    """

    def __init__(self, exceptionMsg, exceptionType):
        self.exceptionMsg = exceptionMsg
        self.exceptionType = exceptionType


class InterruptableThread(threading.Thread):

    def __init__(self, func, *args, **kwargs):
        threading.Thread.__init__(self, daemon=True)
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._result = None

    def run(self):
        try:
            self._result = self._func(*self._args, **self._kwargs)
        except Exception as e:
            logger.debug(
                '*******************************************************************'
                )
            logger.debug('Traceback timeout')
            logger.debug(traceback.format_exc())
            logger.debug('error > ')
            logger.debug(str(e))
            logger.debug(
                '*******************************************************************'
                )
            self._result = FailedProcess(str(e), e.__class__.__name__)

    @property
    def result(self):
        return self._result


class timeout(object):

    def __init__(self, sec):
        self._sec = sec

    def __call__(self, f):

        def wrapped_f(*args, **kwargs):
            it = InterruptableThread(f, *args, **kwargs)
            it.daemon = True
            it.start()
            it.join(self._sec)
            if not it.is_alive():
                logger.debug(
                    'XXXXXXXXXXXXXXX RETURN NOW XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
                    )
                logger.debug(it.result)
                return it.result
            sparta_1eafa52b01(it)
            raise TimeoutError(
                f'Timeout exception (you code cannot run more than {self._sec} seconds, please contact us if you require more computation power)'
                )
        return wrapped_f

#END OF QUBE
