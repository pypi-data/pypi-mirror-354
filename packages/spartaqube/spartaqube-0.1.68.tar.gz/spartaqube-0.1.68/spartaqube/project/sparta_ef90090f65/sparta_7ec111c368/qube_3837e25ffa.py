import pandas as pd
import pymysql
import pymysql.cursors
import pandas as pd
import json
from sqlalchemy import create_engine
from project.logger_config import logger


class db_connection_sql:

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
        return 1

    def setConnection(self, hostname, username, name, password='', port=
        3306, schemaName=None):
        self.hostname = hostname
        self.user = username
        self.db = name
        self.password = password
        if schemaName is None:
            self.schemaName = username
        else:
            self.schemaName = schemaName
        if len(str(port)) > 0:
            self.port = int(port)

    def create_connection(self):
        if self.bPrint:
            logger.debug('create_connection')
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

    def close_connection(self):
        """
        
        """
        self.close_connection()

    def pd2DB(self, tableName, thisDf):
        self.pd2Mysql(tableName, thisDf)

    def pd2Mysql(self, tableName, thisDf):
        engine = create_engine('mysql://' + str(self.user) + ':' + str(self.password) + '@' + str(self.hostname) + ':' + str(self.port) +
            '/' + str(self.db))
        thisDf.to_sql(name=tableName, con=engine, if_exists='append')

    def createBlobTable(self, tableName):
        """
        This function create a table to store blob
        """
        sqlCreate = 'CREATE TABLE `' + str(tableName
            ) + '` (Id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, File LONGBLOB)'
        self.executeSqlRequest(sqlCreate)

    def insertBLOB(self, sqlInsert, data_tuple):
        sqlInsert = sqlInsert + ' VALUES (%s, %s)'
        self.create_connection()
        dbcur = self.connection.cursor()
        dbcur.execute(sqlInsert, data_tuple)
        try:
            self.connection.commit()
            dbcur.close()
            self.close_connection()
        except Exception as e:
            if self.bPrint:
                logger.debug('Request could not be executed with error ' +
                    str(e))

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
        result = dbcur.fetchone()[0]
        dbcur.close()
        self.close_connection()
        return result

    def getAllDispoBLOB(self, tableName):
        """
            Load all the binary (for all the dispo dates)
            This is used for the serializer where we need to load all the binary in order to share it to other users 
            (from LOCAL > CENTRAL when we upload or CENTRAL > LOCAL when we download the data)
        """
        sqlReq = 'SELECT * FROM `' + tableName + '`'
        self.create_connection()
        dbcur = self.connection.cursor()
        dbcur.execute(sqlReq)
        result = dbcur.fetchall()
        dbcur.close()
        self.close_connection()
        return result

    def set_connection_from_dbAuth(self, dbAuthObj):
        """
            
        """
        self.hostname = dbAuthObj.hostname
        self.user = dbAuthObj.username
        self.db = dbAuthObj.name
        self.password = dbAuthObj.password
        self.schemaName = dbAuthObj.schema
        if len(str(dbAuthObj.port)) > 0:
            self.port = int(dbAuthObj.port)
        else:
            self.port = ''

    def printOutput(self, bPrint):
        self.bPrint = bPrint

    def close_connection(self):
        try:
            self.connection.close()
        except:
            pass

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
            "SELECT table_name FROM information_schema.tables WHERE TABLE_SCHEMA IN ('"
             + self.schemaName + "')")
        self.create_connection()
        res_df = pd.read_sql(strReq, con=self.connection)
        self.close_connection()
        return res_df

    def getAllTablesAndColumns(self):
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
        schemas_df = schemas_df[['TABLE_NAME', 'COLUMN_NAME', 'DATA_TYPE',
            'COLUMN_KEY', 'EXTRA']]
        return schemas_df

    def getColumnsOfTable(self, tableName):
        schemaName = self.schemaName
        strReq = (
            "SELECT * FROM information_schema.columns WHERE table_schema = '" +
            str(schemaName) + "' AND TABLE_NAME = '" + str(tableName) +
            "' ORDER BY table_name,ordinal_position")
        self.create_connection()
        res_df = pd.read_sql(strReq, con=self.connection)
        self.close_connection()
        return res_df

    def getAllTablesNbRecords(self):
        schemaName = self.schemaName
        strReq = (
            "SELECT TABLE_NAME, TABLE_ROWS FROM INFORMATION_SCHEMA.TABLES as t WHERE TABLE_SCHEMA = '"
             + str(schemaName) +
            "'             AND NOT EXISTS (SELECT 1 FROM information_schema.columns c WHERE c.table_name = t.table_name)"
            )
        self.create_connection()
        res_df = pd.read_sql(strReq, con=self.connection)
        self.close_connection()
        return res_df

    def getAllTablesNbRecords(self):
        schemaName = self.schemaName
        strReq = (
            "SELECT TABLE_NAME, TABLE_ROWS FROM INFORMATION_SCHEMA.TABLES as t WHERE TABLE_SCHEMA = '"
             + str(schemaName) +
            "'             AND NOT EXISTS (SELECT 1 FROM information_schema.columns c WHERE c.table_name = t.table_name)"
            )
        self.create_connection()
        res_df = pd.read_sql(strReq, con=self.connection)
        self.close_connection()
        return res_df

    def getAllTablesNbRecords2(self, tableNameArr, websocket):
        self.create_connection()
        for tableName in tableNameArr:
            try:
                dbcur = self.connection.cursor()
                sqlShow = 'SELECT count(*) FROM `' + tableName.replace("'",
                    "''") + '`'
                dbcur.execute(sqlShow)
                result = dbcur.fetchone()[0]
                res = {'res': 1, 'recordsNb': result, 'table': tableName}
                resJson = json.dumps(res)
                websocket.send(text_data=resJson)
            except Exception as e:
                res = {'res': -1, 'recordsNb': 0, 'table': tableName}
                resJson = json.dumps(res)
                websocket.send(text_data=resJson)
        dbcur.close()
        self.close_connection()

    def insertOrReplaceData(self, tableName, pandasDataframe: pd.core.frame.DataFrame):
        tableName = tableName.lower()
        pandasDataframe_cp = pandasDataframe.copy()
        if self.checkTableExists(tableName):
            self.insertDataFuncDeleteExisting(tableName, pandasDataframe_cp)
        else:
            self.createTable(tableName, pandasDataframe_cp.columns,
                pandasDataframe_cp.index.name)
            self.insertDataFuncDeleteExisting(tableName, pandasDataframe_cp)

    def insertOrReplaceTickerDateData(self, tableName, pandasDataframe: pd.core.frame.DataFrame):
        tableName = tableName.lower()
        pandasDataframe_cp = pandasDataframe.copy()
        if self.checkTableExists(tableName):
            self.insertDataFuncDeleteTickerDate(tableName, pandasDataframe_cp)
        else:
            self.createTable(tableName, pandasDataframe_cp.columns,
                pandasDataframe_cp.index.name)
            self.insertDataFuncDeleteTickerDate(tableName, pandasDataframe_cp)

    def insertData(self, tableName, pandasDataframe: pd.core.frame.DataFrame):
        tableName = tableName.lower()
        pandasDataframe_cp = pandasDataframe.copy()
        if self.checkTableExists(tableName):
            self.insertDataFunc(tableName, pandasDataframe_cp)
        else:
            self.createTable(tableName, pandasDataframe_cp.columns,
                pandasDataframe_cp.index.name)
            self.insertDataFunc(tableName, pandasDataframe_cp)

    def insertDataFunc(self, tableName, pandasDataframe: pd.core.frame.DataFrame):
        pandasDataframe['sql'] = pandasDataframe.apply(self.prepareData2insert, axis=1)
        sqlCol = ''
        colNameIter = pandasDataframe.columns
        colNameIter = colNameIter[:-1]
        for index, column in enumerate(colNameIter):
            if index == 0:
                sqlCol = '`' + column.replace("'", "''") + '`'
            else:
                sqlCol = sqlCol + ',`' + column.replace("'", "''") + '`'
        indexArr = pandasDataframe.index.tolist()
        self.create_connection()
        dbcur = self.connection.cursor()
        for idx, row in enumerate(pandasDataframe['sql']):
            thisIdx = str(indexArr[idx]).replace("'", "''")
            sql = 'INSERT INTO ' + tableName.replace("'", "''"
                ) + ' (Idx,' + sqlCol + ") VALUES ('" + thisIdx + "'," + row + ')'
            dbcur.execute(sql)
            if self.bPrint:
                logger.debug(sql)
        self.connection.commit()
        dbcur.close()
        self.close_connection()

    def insertDataFuncDeleteTickerDate(self, tableName, pandasDataframe: pd.core.frame.DataFrame):
        pandasDataframe['sql'] = pandasDataframe.apply(self.prepareData2insert, axis=1)
        sqlCol = ''
        colNameIter = pandasDataframe.columns
        colNameIter = colNameIter[:-1]
        for index, column in enumerate(colNameIter):
            if index == 0:
                sqlCol = '`' + column.replace("'", "''") + '`'
            else:
                sqlCol = sqlCol + ',`' + column.replace("'", "''") + '`'
        indexArr = pandasDataframe.index.tolist()
        self.create_connection()
        dbcur = self.connection.cursor()
        for idx, row in enumerate(pandasDataframe['sql']):
            thisIdx = str(indexArr[idx]).replace("'", "''")
            sqlDel = ('DELETE FROM ' + tableName.replace("'", "''") +
                " WHERE Idx ='" + thisIdx + "' AND Ticker = '" +
                pandasDataframe['Ticker'].values[idx] + "'")
            sql = 'INSERT INTO ' + tableName.replace("'", "''"
                ) + ' (Idx,' + sqlCol + ") VALUES ('" + thisIdx + "'," + row + ')'
            dbcur.execute(sqlDel)
            dbcur.execute(sql)
            if self.bPrint:
                logger.debug(sqlDel)
                logger.debug(sql)
        self.connection.commit()
        dbcur.close()
        self.close_connection()

    def insertDataFuncDeleteExisting(self, tableName, pandasDataframe: pd.core.frame.DataFrame):
        pandasDataframe['sql'] = pandasDataframe.apply(self.prepareData2insert, axis=1)
        sqlCol = ''
        colNameIter = pandasDataframe.columns
        colNameIter = colNameIter[:-1]
        for index, column in enumerate(colNameIter):
            if index == 0:
                sqlCol = '`' + column.replace("'", "''") + '`'
            else:
                sqlCol = sqlCol + ',`' + column.replace("'", "''") + '`'
        indexArr = pandasDataframe.index.tolist()
        self.create_connection()
        dbcur = self.connection.cursor()
        for idx, row in enumerate(pandasDataframe['sql']):
            thisIdx = str(indexArr[idx]).replace("'", "''")
            sqlDel = 'DELETE FROM ' + tableName.replace("'", "''"
                ) + " WHERE Idx ='" + thisIdx + "'"
            sql = 'INSERT INTO ' + tableName.replace("'", "''"
                ) + ' (Idx,' + sqlCol + ") VALUES ('" + thisIdx + "'," + row + ')'
            if self.bPrint:
                logger.debug(sqlDel)
                logger.debug(sql)
            dbcur.execute(sqlDel)
            dbcur.execute(sql)
        self.connection.commit()
        dbcur.close()
        self.close_connection()

    def prepareData2insert(self, row):
        sqlReq = ''
        for index, column in enumerate(row.tolist()):
            if index == 0:
                sqlReq = "'" + str(column).replace("'", "''") + "'"
            else:
                sqlReq = sqlReq + ",'" + str(column).replace("'", "''") + "'"
        return sqlReq

    def createTable(self, tableName, columnName, idx):
        tableName = tableName.replace("'", "''")
        tableName = tableName.lower()
        sqlReq = ''
        for index, column in enumerate(columnName):
            if index == 0:
                if column == 'Date' or column == 'Dispo':
                    sqlReq = column.replace("'", "''") + ' datetime'
                else:
                    sqlReq = column.replace("'", "''") + ' varchar(64)'
            elif column == 'Date' or column == 'Dispo':
                sqlReq = sqlReq + ',' + column.replace("'", "''") + ' datetime'
            else:
                sqlReq = sqlReq + ',' + column.replace("'", "''"
                    ) + ' varchar(64)'
        idxCol = ''
        if idx == 'Date' or idx == 'Dispo':
            idxCol = 'Idx datetime,'
        else:
            idxCol = 'Idx varchar(64),'
        sqlReq = ('CREATE TABLE ' + tableName +
            ' (Id INT NOT NULL AUTO_INCREMENT,' + idxCol + sqlReq +
            ',PRIMARY KEY (Id))')
        if self.bPrint:
            logger.debug(sqlReq)
        self.create_connection()
        dbcur = self.connection.cursor()
        dbcur.execute(sqlReq)
        dbcur.close()
        self.close_connection()

    def getCountTable(self, tableName):
        self.create_connection()
        dbcur = self.connection.cursor()
        sqlShow = 'SELECT count(*) FROM `' + tableName.replace("'", "''"
            ) + '`;'
        if self.bPrint:
            logger.debug(sqlShow)
        dbcur.execute(sqlShow)
        result = dbcur.fetchone()[0]
        dbcur.close()
        self.close_connection()
        return result

    def checkTableExists(self, tableName):
        self.create_connection()
        dbcur = self.connection.cursor()
        sqlShow = "SHOW TABLES LIKE '" + tableName.replace("'", "''") + "'"
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

    def executeSqlRequest(self, sqlReq):
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
                logger.debug('Request could not be executed with error 1 ' +
                    str(e))
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
            if self.bPrint:
                logger.debug(
                    'Request could not be executed with error l0 => ' + str(e))
        return insertedId

    def getDataFrame(self, tableName) ->pd.core.frame.DataFrame:
        try:
            strReq = 'SELECT * FROM ' + tableName
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
        try:
            strReq = 'SELECT * FROM ' + tableName + ' LIMIT ' + str(limit)
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

    def getDataFrameReq(self, strReq) ->pd.core.frame.DataFrame:
        try:
            self.create_connection()
            res_df = pd.read_sql(strReq, con=self.connection)
            self.close_connection()
            return res_df
        except Exception as e:
            logger.debug('Exception sql')
            logger.debug(e)
            self.close_connection()
            if self.bPrint:
                logger.debug('Request could not be executed with error 3 ' +
                    str(e))
            raise Exception(str(e))

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
                logger.debug('Request could not be executed with error 4 ' +
                    str(e))

    def df2Sql(self, tableName, pandasDataframe: pd.core.frame.DataFrame):
        self.insertData(tableName, pandasDataframe)

    def df2Sql_noReplace(self, tableName, pandasDataframe: pd.core.frame.DataFrame):
        self.insertData(tableName, pandasDataframe)

#END OF QUBE
