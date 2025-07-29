import os
import re
import openpyxl
import duckdb
import pandas as pd
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_0bbca76031 import EngineBuilder
from project.logger_config import logger


class ParquetConnector(EngineBuilder):

    def __init__(self, database_path):
        """
        
        """
        super().__init__(host=None, port=None, engine_name='parquet')
        self.database = database_path
        self.connector = self.connect_db()

    def connect_db(self):
        return self.build_parquet(database_path=self.database_path)

    def test_connection(self) ->bool:
        """
        Test connection
        """
        try:
            if os.path.isfile(self.database):
                return True
            else:
                return False
        except Exception as e:
            logger.debug(f'Error: {e}')
            self.error_msg_test_connection = str(e)
            return False

    def get_available_tables(self) ->list:
        """
        This method returns all the available tables of a database using sql_alchemy
        """

        def get_file_name_without_extension(file_path):
            file_name_with_extension = os.path.basename(file_path)
            file_name_without_extension = os.path.splitext(
                file_name_with_extension)[0]
            return file_name_without_extension
        try:
            if os.path.isfile(self.database):
                return [get_file_name_without_extension(self.database)]
            else:
                return []
        except Exception as e:
            logger.debug(f'Error: {e}')
            self.error_msg_test_connection = str(e)
            return False

    def get_table_columns(self, table_name) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available columns of a table
        """
        try:
            query = f"PRAGMA table_info('{self.database}')"
            schema_df = self.connector.execute(query).fetchdf()
            column_names = schema_df['name'].tolist()
            return column_names
        except Exception as e:
            logger.debug(
                f"Failed to list columns for table '{table_name}': {e}")
            return []

    def get_data_table(self, table_name) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        try:
            query = f"SELECT * FROM '{self.database}'"
            result_df = self.connector.execute(query).fetchdf()
            return result_df
        except Exception as e:
            raise Exception(e)

    def get_data_table_top(self, table_name, top_limit=100) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        try:
            query = f"SELECT * FROM '{self.database}' LIMIT {top_limit}"
            result_df = self.connector.execute(query).fetchdf()
            return result_df
        except Exception as e:
            raise Exception(e)

    def get_data_table_query(self, sql, table_name=None) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """

        def remove_sql_comments(sql_query):
            sql_query = re.sub('--.*', '', sql_query)
            sql_query = re.sub('#.*', '', sql_query)
            sql_query = re.sub('/\\*.*?\\*/', '', sql_query, flags=re.DOTALL)
            sql_query = ' '.join(sql_query.split())
            return sql_query
        try:
            query = sql
            query = query.replace('"SQ_PARQUET"', 'SQ_PARQUET')
            query = query.replace("'SQ_PARQUET'", 'SQ_PARQUET')
            query = query.replace('SQ_PARQUET', f"'{self.database}'")
            query = remove_sql_comments(query)
            result_df = self.connector.execute(query).fetchdf()
            return result_df
        except Exception as e:
            raise Exception(e)

#END OF QUBE
