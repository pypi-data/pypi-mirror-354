import time
from project.logger_config import logger


def sparta_448a95d938():
    ti = 0
    tf = time.time()
    while True:
        ti = tf
        tf = time.time()
        yield tf - ti


TicToc = sparta_448a95d938()


def sparta_a89d4abaae(tempBool=True):
    tempTimeInterval = next(TicToc)
    if tempBool:
        logger.debug('Elapsed time: %f seconds.\n' % tempTimeInterval)
        return tempTimeInterval


def sparta_2fb68ae338():
    sparta_a89d4abaae(False)

#END OF QUBE
