import os
import duckdb
import pandas as pd
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_0bbca76031 import EngineBuilder
from project.logger_config import logger


class DuckDBConnector(EngineBuilder):

    def __init__(self, database_path, read_only=False):
        """
        
        """
        super().__init__(host=None, port=None, database=database_path)
        self.database_path = database_path
        self.read_only = read_only
        self.connector = self.connect_db()

    def connect_db(self):
        return self.build_duckdb(database_path=self.database_path,
            read_only=self.read_only)

    def test_connection(self) ->bool:
        """
        Test connection
        """
        if self.database is None:
            self.error_msg_test_connection = 'Empty database path'
            return False
        if not os.path.exists(self.database) and self.database != ':memory:':
            self.error_msg_test_connection = 'Invalid database path'
            return False
        try:
            self.connector.execute('SELECT 1')
            self.connector.close()
            return True
        except Exception as e:
            self.error_msg_test_connection = str(e)
            return False

    def get_available_tables(self) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available tables of a database
        """
        try:
            tables = self.connector.execute('SHOW TABLES').fetchall()
            self.connector.close()
            table_names = [table[0] for table in tables]
            return table_names
        except Exception as e:
            self.connector.close()
            logger.debug(f'Failed to list tables: {e}')
            return []

    def get_table_columns(self, table_name) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available columns of a table
        """
        try:
            columns_query = f"PRAGMA table_info('{table_name}')"
            columns = self.connector.execute(columns_query).fetchall()
            self.connector.close()
            column_names = [column[1] for column in columns]
            return column_names
        except Exception as e:
            self.connector.close()
            logger.debug(
                f"Failed to list columns for table '{table_name}': {e}")
            return []

    def get_data_table(self, table_name) ->pd.DataFrame:
        """
        
        """
        try:
            query = f'SELECT * FROM {table_name}'
            table_df = self.connector.execute(query).df()
            self.connector.close()
            return table_df
        except Exception as e:
            self.connector.close()
            raise Exception(e)

    def get_data_table_top(self, table_name, top_limit=100) ->pd.DataFrame:
        """
        
        """
        try:
            query = f'SELECT * FROM {table_name} LIMIT {top_limit}'
            table_df = self.connector.execute(query).df()
            self.connector.close()
            return table_df
        except Exception as e:
            self.connector.close()
            raise Exception(e)

#END OF QUBE
