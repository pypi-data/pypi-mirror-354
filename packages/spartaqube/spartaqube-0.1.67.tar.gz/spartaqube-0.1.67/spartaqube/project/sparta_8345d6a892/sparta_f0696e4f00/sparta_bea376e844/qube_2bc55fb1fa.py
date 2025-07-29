try:
    import cx_Oracle
except:
    pass
import pandas as pd
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_0bbca76031 import EngineBuilder
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import convert_to_dataframe
from project.logger_config import logger


class OracleConnector(EngineBuilder):

    def __init__(self, host, port, user, password, database=None, lib_dir=
        None, oracle_service_name='orcl'):
        """
        
        """
        super().__init__(host=host, port=port, user=user, password=password,
            database=database, engine_name='oracle+cx_oracle')
        self.lib_dir = lib_dir
        self.oracle_service_name = oracle_service_name
        self.connector = self.connect_db()

    def connect_db(self):
        return self.build_oracle(self.lib_dir, self.oracle_service_name)

    def test_connection(self) ->bool:
        """
        Test connection
        """
        connection = self.connector
        res = False
        try:
            cursor = connection.cursor()
            b_use_schema = False
            if self.database is not None:
                if len(self.database) > 0:
                    b_use_schema = True
            if b_use_schema:
                schema = self.database
                cursor.execute(f'ALTER SESSION SET CURRENT_SCHEMA = {schema}')
            cursor.execute("SELECT 'Connection successful' FROM dual")
            result = cursor.fetchone()
            res = True
        except cx_Oracle.DatabaseError as e:
            self.error_msg_test_connection = str(e)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return res

    def get_available_tables(self) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available tables of a database
        """
        connection = self.connector
        table_list = []
        try:
            cursor = connection.cursor()
            b_use_schema = False
            if self.database is not None:
                if len(self.database) > 0:
                    b_use_schema = True
            if b_use_schema:
                schema = self.database
                cursor.execute(f'ALTER SESSION SET CURRENT_SCHEMA = {schema}')
            cursor.execute('SELECT table_name FROM user_tables')
            tables = cursor.fetchall()
            table_list = [table[0] for table in tables]
        except cx_Oracle.DatabaseError as e:
            logger.debug('There was a problem with Oracle', e)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return table_list

    def get_table_columns(self, table_name) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available columns of a table
        """
        connection = self.connector
        table_list = []
        try:
            cursor = connection.cursor()
            b_use_schema = False
            if self.database is not None:
                if len(self.database) > 0:
                    b_use_schema = True
            if b_use_schema:
                schema = self.database
                cursor.execute(f'ALTER SESSION SET CURRENT_SCHEMA = {schema}')
            cursor.execute(
                """
                SELECT column_name 
                FROM all_tab_columns 
                WHERE table_name = :table_name
            """
                , table_name=table_name)
            tables = cursor.fetchall()
            table_list = [table[0] for table in tables]
        except cx_Oracle.DatabaseError as e:
            logger.debug('There was a problem with Oracle', e)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return table_list

    def get_data_table(self, table_name) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        connection = self.connector
        data = None
        exception = None
        try:
            cursor = connection.cursor()
            b_use_schema = False
            if self.database is not None:
                if len(self.database) > 0:
                    b_use_schema = True
            if b_use_schema:
                schema = self.database
                cursor.execute(f'ALTER SESSION SET CURRENT_SCHEMA = {schema}')
            cursor.execute(f'SELECT * FROM {table_name}')
            rows = cursor.fetchall()
            col_names = [row[0] for row in cursor.description]
            data = [dict(zip(col_names, row)) for row in rows]
        except cx_Oracle.DatabaseError as e:
            logger.debug('There was a problem with Oracle', e)
            exception = e
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        if data is not None:
            return convert_to_dataframe(data)
        raise Exception(exception)

    def get_data_table_top(self, table_name, top_limit=100) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        connection = self.connector
        data = None
        exception = None
        try:
            cursor = connection.cursor()
            b_use_schema = False
            if self.database is not None:
                if len(self.database) > 0:
                    b_use_schema = True
            if b_use_schema:
                schema = self.database
                cursor.execute(f'ALTER SESSION SET CURRENT_SCHEMA = {schema}')
            query = (
                f'SELECT * FROM {table_name} FETCH FIRST {top_limit} ROWS ONLY'
                )
            cursor.execute(query)
            rows = cursor.fetchall()
            col_names = [row[0] for row in cursor.description]
            data = [dict(zip(col_names, row)) for row in rows]
        except cx_Oracle.DatabaseError as e:
            logger.debug('There was a problem with Oracle', e)
            exception = e
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        if data is not None:
            return convert_to_dataframe(data)
        raise Exception(exception)

    def get_data_table_query(self, sql, table_name=None) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        connection = self.connector
        data = None
        exception = None
        try:
            cursor = connection.cursor()
            b_use_schema = False
            if self.database is not None:
                if len(self.database) > 0:
                    b_use_schema = True
            if b_use_schema:
                schema = self.database
                cursor.execute(f'ALTER SESSION SET CURRENT_SCHEMA = {schema}')
            cursor.execute(sql)
            rows = cursor.fetchall()
            col_names = [row[0] for row in cursor.description]
            data = [dict(zip(col_names, row)) for row in rows]
        except cx_Oracle.DatabaseError as e:
            logger.debug('There was a problem with Oracle', e)
            exception = e
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        if data is not None:
            return convert_to_dataframe(data)
        raise Exception(exception)

#END OF QUBE
