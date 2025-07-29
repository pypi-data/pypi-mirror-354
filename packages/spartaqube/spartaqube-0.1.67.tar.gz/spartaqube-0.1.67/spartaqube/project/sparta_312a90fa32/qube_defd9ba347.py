import time
from project.logger_config import logger
def sparta_ea2aef86e2():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_ea2aef86e2()
def sparta_3bd38a51f0(tempBool=True):
	A=next(TicToc)
	if tempBool:logger.debug('Elapsed time: %f seconds.\n'%A);return A
def sparta_759c228b16():sparta_3bd38a51f0(False)