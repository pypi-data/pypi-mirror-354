import json
import pandas as pd
import pymysql
import pymysql.cursors
import psycopg2
import pandas as pd
import pandas.io.sql as psql
from sqlalchemy import create_engine
from project.sparta_ef90090f65.sparta_7ec111c368.qube_3837e25ffa import qube_3837e25ffa
from project.logger_config import logger


class db_connection_postgre(db_connection_sql):

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

    def getDBType(self):
        return 2

    def setConnection(self, hostname, username, name, password='', port=
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
            logger.debug('create_connection for POSTGRESQL now')
            logger.debug('self.hostname => ' + str(self.hostname))
            logger.debug('self.user => ' + str(self.user))
            logger.debug('self.password => ' + str(self.password))
            logger.debug('self.port => ' + str(self.port))
            logger.debug('self.schemaName => ' + str(self.schemaName))
            logger.debug('self.database => ' + str(self.db))
        if self.schemaName is None:
            self.schemaName = self.user
        if len(str(self.port)) > 0:
            self.connection = psycopg2.connect(host=self.hostname, user=
                self.user, password=self.password, database=self.db, port=
                self.port)
        else:
            self.connection = psycopg2.connect(host=self.hostname, user=
                self.user, password=self.password, database=self.db)

    def getAllTablesAndColumns(self):
        """

        """
        schemaName = self.schemaName
        strReq = (
            "SELECT * FROM information_schema.columns WHERE table_schema = '" +
            str(schemaName) + "' ORDER BY table_name,ordinal_position")
        self.create_connection()
        res_df = pd.read_sql(strReq, con=self.connection)
        self.close_connection()
        return res_df

    def getAllTablesAndColumnsRenamed(self):
        """

        """
        schemas_df = self.getAllTablesAndColumns()
        schemas_df = schemas_df[['table_name', 'column_name', 'data_type']]
        schemas_df.rename(columns={'table_name': 'TABLE_NAME'}, inplace=True)
        return schemas_df

    def getAllTablesNbRecords(self):
        """
            Get name of all the tables and their number of row records
        """
        schemaName = self.schemaName
        strReq = (
            "WITH tbl AS             (SELECT table_schema,                     TABLE_NAME             FROM information_schema.tables             WHERE TABLE_NAME not like 'pg_%'                 AND table_schema = '"
             + str(schemaName) +
            "')             SELECT table_schema,                 TABLE_NAME,                 (xpath('/row/c/text()', query_to_xml(format('select count(*) as c from %I.%I', table_schema, TABLE_NAME), FALSE, TRUE, '')))[1]::text::int AS rows_n             FROM tbl             ORDER BY rows_n DESC;"
            )
        self.create_connection()
        res_df = pd.read_sql(strReq, con=self.connection)
        res_df.rename(columns={'table_name': 'TABLE_NAME', 'rows_n':
            'TABLE_ROWS'}, inplace=True)
        res_df = res_df[['TABLE_NAME', 'TABLE_ROWS']]
        self.close_connection()
        return res_df

    def getAllTablesNbRecords2(self, tableNameArr, websocket):
        self.create_connection()
        for tableName in tableNameArr:
            try:
                dbcur = self.connection.cursor()
                sqlShow = 'SELECT count(*) FROM ' + tableName.replace("'", "''"
                    ) + ''
                dbcur.execute(sqlShow)
                result = dbcur.fetchone()[0]
                res = {'res': 1, 'recordsNb': result, 'table': tableName}
                resJson = json.dumps(res)
                websocket.send(text_data=resJson)
            except:
                res = {'res': -1, 'recordsNb': 0, 'table': tableName}
                resJson = json.dumps(res)
                websocket.send(text_data=resJson)
        dbcur.close()
        self.close_connection()

    def getCountTable(self, tableName):
        self.create_connection()
        dbcur = self.connection.cursor()
        sqlShow = 'SELECT count(*) FROM ' + tableName.replace("'", "''") + ''
        if self.bPrint:
            logger.debug(sqlShow)
        dbcur.execute(sqlShow)
        result = dbcur.fetchone()[0]
        dbcur.close()
        self.close_connection()
        return result

    def getAllSChemas(self):
        strReq = (
            "SELECT schema_name FROM information_schema.SCHEMATA WHERE schema_name IN ('"
             + self.db + "')")
        self.create_connection()
        res_df = pd.read_sql(strReq, con=self.connection)
        self.close_connection()
        return res_df

    def getThisSchema(self, schemaName):
        strReq = (
            "SELECT schema_name FROM information_schema.SCHEMATA WHERE schema_name NOT IN ('information_schema', 'mysql') AND schema_name IN ('"
             + schemaName + "')")
        self.create_connection()
        res_df = pd.read_sql(strReq, con=self.connection)
        self.close_connection()
        return res_df

    def getAllTables(self):
        strReq = (
            "SELECT table_name FROM information_schema.tables WHERE TABLE_SCHEMA = '"
             + self.schemaName + "'")
        self.create_connection()
        res_df = pd.read_sql(strReq, con=self.connection)
        self.close_connection()
        return res_df

    def checkTableExists(self, tableName):
        self.create_connection()
        dbcur = self.connection.cursor()
        sqlShow = (
            "select table_name from information_schema.tables where table_name='"
             + tableName.replace("'", "''") + "'")
        if self.bPrint:
            logger.debug(sqlShow)
        dbcur.execute(sqlShow)
        result = dbcur.fetchone()
        dbcur.close()
        self.close_connection()
        if result:
            return True
        else:
            return False

    def pd2DB(self, tableName, thisDf):
        """
            This function send a pandas dataframe into the PostgreSQL db
        """
        engine = create_engine('postgresql://' + str(self.user) + ':' + str
            (self.password) + '@' + str(self.hostname) + ':' + str(self.port) + '/' + str(self.db))
        thisDf.to_sql(name=tableName, con=engine, if_exists='append')

    def getDataFrame(self, tableName) ->pd.core.frame.DataFrame:
        """
            Difference between the db_connection_sql file is the quotes between tableName
        """
        try:
            strReq = 'SELECT * FROM "' + tableName + '"'
            if self.bPrint:
                logger.debug('strReq => ' + str(strReq))
            self.create_connection()
            res_df = pd.read_sql(strReq, con=self.connection)
            self.close_connection()
            return res_df
        except Exception as e:
            self.close_connection()
            if not self.checkTableExists(tableName):
                if self.bPrint:
                    logger.debug('This table does not exist...')
            elif self.bPrint:
                logger.debug('Request could not be executed with error 2 ' +
                    str(e))
            return None

    def getDataFrameLimit(self, tableName, limit=100
        ) ->pd.core.frame.DataFrame:
        """
            Difference between the db_connection_sql file is the quotes between tableName
        """
        try:
            strReq = 'SELECT * FROM "' + tableName + '" LIMIT ' + str(limit)
            if self.bPrint:
                logger.debug('strReq => ' + str(strReq))
            self.create_connection()
            res_df = pd.read_sql(strReq, con=self.connection)
            self.close_connection()
            return res_df
        except Exception as e:
            self.close_connection()
            if not self.checkTableExists(tableName):
                if self.bPrint:
                    logger.debug('This table does not exist...')
            elif self.bPrint:
                logger.debug('Request could not be executed with error 2 ' +
                    str(e))
            return None

#END OF QUBE
