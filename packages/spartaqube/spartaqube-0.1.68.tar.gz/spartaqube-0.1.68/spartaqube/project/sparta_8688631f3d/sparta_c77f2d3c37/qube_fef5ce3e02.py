import os
from multiprocessing import Process


def sparta_eaad2374e8(func):
    """Decorate a function so that its calls are async in a detached process.Usage
    -----.. code::
            import time

            @sparta_eaad2374e8
            def f(message):
                time.sleep(5)
                print(message)

            f('Async and detached!!!')

    """

    def forkify(*args, **kwargs):
        if os.fork() != 0:
            return
        func(*args, **kwargs)

    def wrapper(*args, **kwargs):
        proc = Process(target=lambda : forkify(*args, **kwargs))
        proc.start()
        proc.join()
        return
    return wrapper

#END OF QUBE
