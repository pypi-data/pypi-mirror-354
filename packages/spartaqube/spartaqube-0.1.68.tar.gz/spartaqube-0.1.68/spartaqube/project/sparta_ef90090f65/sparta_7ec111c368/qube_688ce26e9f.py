import pandas as pd
import pymysql
import pymysql.cursors
import pandas as pd
from sqlalchemy import create_engine
from project.sparta_ef90090f65.sparta_7ec111c368.qube_3837e25ffa import qube_3837e25ffa
from project.logger_config import logger


class db_connection_mysql(db_connection_sql):

    def __init__(self):
        self.hostname = 'localhost'
        self.user = 'root'
        self.schemaName = None
        self.db = 'qbm'
        self.port = 3306
        self.path = None
        self.password = ''
        self.connection = -1
        self.bPrint = False
        try:
            from django.conf import settings as conf_settings
            if conf_settings.PLATFORM in conf_settings.USE_DEFAULT_DB_SETTINGS:
                dataBasesDict = conf_settings.DATABASES['default']
                self.hostname = dataBasesDict['HOST']
                self.user = dataBasesDict['USER']
                self.schemaName = dataBasesDict['NAME']
                self.db = dataBasesDict['NAME']
                self.password = dataBasesDict['PASSWORD']
                self.port = int(dataBasesDict['PORT'])
        except:
            pass

    def get_db_type(self):
        return 1

    def set_connection(self, hostname, username, name, password='', port=
        3306, schemaName=None):
        self.hostname = hostname
        self.user = username
        self.db = name
        self.password = password
        if schemaName is None:
            self.schemaName = name
        elif len(schemaName) > 0:
            self.schemaName = schemaName
        else:
            self.schemaName = name
        if len(str(port)) > 0:
            self.port = int(port)

    def create_connection(self):
        if self.bPrint:
            logger.debug('create_connection for MYSQL')
            logger.debug('self.hostname => ' + str(self.hostname))
            logger.debug('self.user => ' + str(self.user))
            logger.debug('self.password => ' + str(self.password))
            logger.debug('self.port => ' + str(self.port))
        if self.schemaName is None:
            self.schemaName = self.user
        if len(str(self.port)) > 0:
            self.connection = pymysql.connect(host=self.hostname, user=self.user, password=self.password, db=self.db, port=self.port)
        else:
            self.connection = pymysql.connect(host=self.hostname, user=self.user, password=self.password, db=self.db)

#END OF QUBE
