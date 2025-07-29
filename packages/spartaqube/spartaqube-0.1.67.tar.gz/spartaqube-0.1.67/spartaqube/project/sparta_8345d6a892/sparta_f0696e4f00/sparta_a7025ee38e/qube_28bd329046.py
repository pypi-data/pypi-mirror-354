import pandas as pd
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_0bbca76031 import EngineBuilder


class MssqlConnector(EngineBuilder):

    def __init__(self, host, port, trusted_connection, driver, user,
        password, database):
        """
        
        """
        super().__init__(host=host, port=port, user=user, password=password,
            database=database, engine_name='mssql+pyodbc')
        self.trusted_connection = trusted_connection
        self.driver = driver
        self.connector = self.connect_db()

    def connect_db(self):
        return self.build_mssql(self.trusted_connection, self.driver)

    def test_connection(self) ->bool:
        """
        
        """
        self.connector = self.connect_db()
        if self.connector is None:
            return False
        res = False
        try:
            connection = self.connector
            cursor = connection.cursor()
            query = 'SELECT @@VERSION'
            cursor.execute(query)
            row = cursor.fetchone()
            while row:
                row = cursor.fetchone()
            res = True
        except Exception as e:
            self.error_msg_test_connection = str(e)
        try:
            if connection:
                connection.close()
        except:
            pass
        return res

    def get_available_tables(self) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available tables of a database
        """
        self.connector = self.connect_db()
        if self.connector is None:
            return []
        tables_list = []
        try:
            connection = self.connector
            query = (
                "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
                )
            df_tables = pd.read_sql(query, connection)
            tables_list = sorted(list(df_tables['TABLE_NAME'].values))
        except Exception as e:
            self.error_msg_test_connection = str(e)
            tables_list = []
        finally:
            if connection:
                connection.close()
        return tables_list

    def get_table_columns(self, table_name) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available columns of a table
        """
        self.connector = self.connect_db()
        if self.connector is None:
            return []
        columns_list = []
        try:
            connection = self.connector
            query = f"""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}'
                """
            df_tables = pd.read_sql(query, connection)
            columns_list = sorted(list(df_tables['COLUMN_NAME'].values))
        except Exception as e:
            self.error_msg_test_connection = str(e)
            columns_list = []
        finally:
            if connection:
                connection.close()
        return columns_list

    def get_data_table(self, table_name) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        self.connector = self.connect_db()
        if self.connector is None:
            return pd.DataFrame()
        try:
            connection = self.connector
            query = f'SELECT * FROM {table_name}'
            df_tables = pd.read_sql(query, connection)
            return df_tables
        except Exception as e:
            self.error_msg_test_connection = str(e)
            return pd.DataFrame()
        finally:
            if connection:
                connection.close()

    def get_data_table_top(self, table_name, top_limit=100) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        self.connector = self.connect_db()
        if self.connector is None:
            return pd.DataFrame()
        try:
            connection = self.connector
            query = f'SELECT TOP {top_limit} * FROM {table_name}'
            df_tables = pd.read_sql(query, connection)
            return df_tables
        except Exception as e:
            self.error_msg_test_connection = str(e)
            return pd.DataFrame()
        finally:
            if connection:
                connection.close()

    def get_data_table_query(self, sql, table_name=None) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        self.connector = self.connect_db()
        if self.connector is None:
            return pd.DataFrame()
        try:
            connection = self.connector
            query = sql
            df_tables = pd.read_sql(query, connection)
            return df_tables
        except Exception as e:
            self.error_msg_test_connection = str(e)
            return pd.DataFrame()
        finally:
            if connection:
                connection.close()

    def get_available_views(self) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available views of a database
        """
        self.connector = self.connect_db()
        if self.connector is None:
            return []
        views_list = []
        try:
            connection = self.connector
            query = 'SELECT name FROM sys.views ORDER BY name'
            df_views = pd.read_sql(query, connection)
            views_list = sorted(list(df_views['name'].values))
        except Exception as e:
            self.error_msg_test_connection = str(e)
            views_list = []
        finally:
            if connection:
                connection.close()
        return views_list

#END OF QUBE
