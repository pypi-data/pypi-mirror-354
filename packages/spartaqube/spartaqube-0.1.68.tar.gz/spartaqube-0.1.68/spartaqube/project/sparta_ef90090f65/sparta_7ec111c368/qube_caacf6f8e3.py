import pandas as pd
import sqlite3
import os
from project.logger_config import logger


class db_connection_sqlite:

    def __init__(self, hostname='', schemaName=None, user='', db='db',
        password='', port='', path=''):
        self.hostname = hostname
        self.schemaName = schemaName
        self.user = user
        self.db = db
        self.password = password
        self.port = port
        self.bPrint = False
        self.path = path
        if os.environ['DJANGO_SETTINGS_MODULE'
            ] == 'spartaqube.project.settings':
            self.db = 'db'
        self.create_connection()

    def getDBType(self):
        return 0

    def setBPrint(self, bPrint):
        self.bPrint = bPrint

    def setPath(self, thisPath):
        self.path = thisPath

    def setDbName(self, db_):
        self.db = db_

    def setConnection(self, hostname='', username='', name=''):
        self.hostname = hostname
        self.user = username
        self.db = name

    def create_connection(self):
        self.connection = sqlite3.connect(self.path + '/' + str(self.db) +
            '.sqlite3')

    def printOutput(self, bPrint):
        self.bPrint = bPrint

    def close_connection(self):
        self.connection.close()

    def pd2DB(self, tableName, thisDf):
        self.df2Sql(tableName, thisDf)

    def getAllSChemas(self):
        strReq = "SELECT name FROM sqlite_master WHERE type='table'"
        self.create_connection()
        res_df = pd.read_sql(strReq, con=self.connection)
        self.close_connection()
        return res_df

    def df2Sql(self, tableName, pandasDataframe: pd.core.frame.DataFrame):
        self.create_connection()
        pandasDataframe_cp = pandasDataframe.copy()
        pandasDataframe_cp.to_sql(name=tableName, con=self.connection,
            if_exists='replace', index=True)
        self.close_connection()

    def df2Sql_noReplace(self, tableName, pandasDataframe: pd.core.frame.DataFrame):
        self.create_connection()
        pandasDataframe_cp = pandasDataframe.copy()
        pandasDataframe_cp.to_sql(name=tableName, con=self.connection,
            if_exists='append', index=True)
        self.close_connection()

    def getCountTable(self, tableName):
        """
        
        """
        self.create_connection()
        dbcur = self.connection.cursor()
        sqlShow = "SELECT count(*) FROM '" + tableName.replace("'", "''"
            ) + "';"
        if self.bPrint:
            logger.debug(sqlShow)
        dbcur.execute(sqlShow)
        result = dbcur.fetchone()[0]
        dbcur.close()
        self.close_connection()
        return result

    def checkTableExists(self, tableName):
        """
        
        """
        self.create_connection()
        dbcur = self.connection.cursor()
        sqlShow = (
            "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='"
             + tableName.replace("'", "''") + "';")
        if self.bPrint:
            logger.debug(sqlShow)
        dbcur.execute(sqlShow)
        result = dbcur.fetchone()[0]
        dbcur.close()
        self.close_connection()
        if result > 0:
            return True
        else:
            return False

    def createBlobTable(self, tableName):
        """
        This function create a table to store blob
        """
        sqlCreate = 'CREATE TABLE `' + str(tableName
            ) + '` (Id INT(11) PRIMARY KEY, File LONGBLOB)'
        self.executeSqlRequest(sqlCreate)

    def insertBLOB(self, sqlInsert, data_tuple):
        """
        EXAMPLE : insertBLOB('INSERT INTO TABLE (col1, col2, col3) VALUES (?,?,?)', (, , ,))
        """
        sqlInsert = sqlInsert + ' VALUES (?, ?)'
        self.create_connection()
        dbcur = self.connection.cursor()
        dbcur.execute(sqlInsert, data_tuple)
        try:
            self.connection.commit()
            dbcur.close()
            self.close_connection()
        except Exception as e:
            if self.bPrint:
                logger.debug(
                    'Request could not be executed with error l10 ' + str(e))

    def getBLOB(self, tableName, dispoDate=None):
        if dispoDate is None:
            sqlReq = ('SELECT File FROM `' + tableName +
                '` ORDER BY Dispo DESC LIMIT 1')
        else:
            sqlReq = ('SELECT File FROM `' + tableName + "` WHERE Dispo='" +
                str(dispoDate) + "' ORDER BY Id DESC LIMIT 1")
        self.create_connection()
        dbcur = self.connection.cursor()
        dbcur.execute(sqlReq)
        result = dbcur.fetchone()
        if result is not None:
            if len(result) == 1:
                result = result[0]
        dbcur.close()
        self.close_connection()
        return result

    def get_blob(self, tableName):
        """
    
        """
        sqlReq = 'SELECT * FROM `' + tableName + '`'
        self.create_connection()
        dbcur = self.connection.cursor()
        dbcur.execute(sqlReq)
        result = dbcur.fetchall()
        dbcur.close()
        self.close_connection()
        return result

    def executeSqlRequest(self, sqlReq):
        """
        
        """
        insertedId = None
        self.create_connection()
        dbcur = self.connection.cursor()
        if self.bPrint:
            logger.debug(sqlReq)
        try:
            dbcur.execute(sqlReq)
            self.connection.commit()
            insertedId = dbcur.lastrowid
            dbcur.close()
            self.close_connection()
        except Exception as e:
            if self.bPrint:
                logger.debug(
                    'Request could not be executed with error l0 => ' + str(e))
        return insertedId

    def executeSqlRequestArgs(self, sqlReq, sqlArgs):
        insertedId = None
        self.create_connection()
        dbcur = self.connection.cursor()
        if self.bPrint:
            logger.debug(sqlReq)
        try:
            dbcur.execute(sqlReq, sqlArgs)
            self.connection.commit()
            insertedId = dbcur.lastrowid
            dbcur.close()
            self.close_connection()
        except Exception as e:
            self.bPrint = True
            if self.bPrint:
                logger.debug(
                    'Request could not be executed with error l0 => ' + str(e))
        return insertedId

    def getDataFrame(self, tableName) ->pd.core.frame.DataFrame:
        try:
            strReq = 'SELECT * FROM ' + tableName
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
                logger.debug(
                    'Request could not be executed with error l1 => ' + str(e))
            return None

    def getDataFrameLimit(self, tableName, limit=100
        ) ->pd.core.frame.DataFrame:
        try:
            strReq = 'SELECT * FROM ' + tableName + ' LIMIT ' + str(limit)
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
                logger.debug(
                    'Request could not be executed with error l1 => ' + str(e))
            return None

    def getDataFrameReq(self, strReq) ->pd.core.frame.DataFrame:
        try:
            self.create_connection()
            res_df = pd.read_sql(strReq, con=self.connection)
            self.close_connection()
            return res_df
        except Exception as e:
            self.close_connection()
            if self.bPrint:
                logger.debug(
                    'Request could not be executed with error l2 => ' + str(e))
            return None

    def getData(self, tableName, flds=None, startDate=None, endDate=None,
        orderBy=None) ->pd.core.frame.DataFrame:
        try:
            strReq = 'SELECT * FROM ' + tableName
            if startDate is not None:
                strReq = strReq + " WHERE Idx >= '" + startDate + "'"
                if endDate is not None:
                    strReq = strReq + " AND Idx <= '" + endDate + "'"
            elif endDate is not None:
                strReq = strReq + " WHERE Idx <= '" + endDate + "'"
            if orderBy is not None:
                strReq = strReq + ' ORDER BY ' + orderBy
            if self.bPrint:
                logger.debug(strReq)
            self.create_connection()
            res_df = pd.read_sql(strReq, con=self.connection)
            res_df.set_index('Idx', inplace=True)
            res_df = res_df.drop(['Id'], axis=1)
            self.close_connection()
            if flds is not None:
                return res_df[flds]
            else:
                return res_df
        except Exception as e:
            self.close_connection()
            if not self.checkTableExists(tableName):
                if self.bPrint:
                    logger.debug('This table does not exist...')
            elif self.bPrint:
                logger.debug(
                    'Request could not be executed with error l3 => ' + str(e))

#END OF QUBE
