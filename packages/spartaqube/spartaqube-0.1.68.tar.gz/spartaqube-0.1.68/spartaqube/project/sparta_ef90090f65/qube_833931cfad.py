import os


class writeLog:

    def __init__(self):
        pass

    def write(self, thisText):
        thisPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        thisPath = thisPath + str('/log/log.txt')
        file1 = open(thisPath, 'a')
        file1.write(thisText)
        file1.writelines('\n')
        file1.close()

#END OF QUBE
