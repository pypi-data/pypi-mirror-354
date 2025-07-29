import os
from project.sparta_ef90090f65.sparta_7ec111c368.qube_688ce26e9f import qube_688ce26e9f
from project.sparta_ef90090f65.sparta_7ec111c368.qube_caacf6f8e3 import qube_caacf6f8e3
from project.logger_config import logger


class db_custom_connection:

    def __init__(self):
        self.dbCon = None
        self.dbIdManager = ''
        self.spartAppId = ''

    def setSettingsSqlite(self, dbId, dbLocalPath, dbFileNameWithExtension):
        from bqm import settings
        from bqm import settingsLocalDesktop
        self.dbType = 0
        self.spartAppId = dbId
        newDatabase = {}
        newDatabase['id'] = dbId
        newDatabase['ENGINE'] = 'django.db.backends.sqlite3'
        newDatabase['NAME'] = str(dbLocalPath) + '/' + str(
            dbFileNameWithExtension)
        newDatabase['USER'] = ''
        newDatabase['PASSWORD'] = '2change'
        newDatabase['HOST'] = ''
        newDatabase['PORT'] = ''
        settings.DATABASES[dbId] = newDatabase
        settingsLocalDesktop.DATABASES[dbId] = newDatabase
        dbConn = qube_caacf6f8e3()
        dbConn.setPath(dbLocalPath)
        dbConn.setDbName('spartApp')
        self.dbCon = dbConn
        self.dbIdManager = 'spartApp'
        logger.debug(settings.DATABASES)

    def getConnection(self):
        return self.dbCon

    def setAuthDB(self, authDB):
        self.dbType = authDB.dbType

#END OF QUBE
