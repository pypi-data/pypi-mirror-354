import os
import re
import openpyxl
import duckdb
import pandas as pd
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_0bbca76031 import EngineBuilder
from project.logger_config import logger


class CsvConnector(EngineBuilder):

    def __init__(self, csv_path, csv_delimiter=None):
        """
        
        """
        super().__init__(host=None, port=None)
        self.connector = self.build_csv(file_path=csv_path)
        self.is_csv = os.path.splitext(csv_path)[1].lower() == '.csv'
        self.csv_path = csv_path
        self.csv_delimiter = csv_delimiter

    def test_connection(self) ->bool:
        """
        Test connection
        """
        try:
            if os.path.isfile(self.connector.file_path):
                return True
            else:
                self.error_msg_test_connection = 'Invalid file path'
                return False
        except Exception as e:
            logger.debug(f'Error: {e}')
            self.error_msg_test_connection = str(e)
            return False

    def get_available_tables(self) ->list:
        """
        This method returns all the available tables of a database using sql_alchemy
        """
        if self.is_csv:
            return self.get_available_tables_csv()
        else:
            return self.get_available_tables_xls()

    def get_available_tables_csv(self) ->list:
        """
        No sheets for CSV
        """
        return ['sheet1']

    def get_available_tables_xls(self) ->list:
        """
        
        """
        try:
            workbook = openpyxl.load_workbook(self.csv_path)
            sheet_names = workbook.sheetnames
            return sorted(sheet_names)
        except Exception as e:
            logger.debug('Exception get available tables metadata')
            logger.debug(e)
            self.error_msg_test_connection = str(e)
            return []

    def get_data_table(self, table_name):
        """
        
        """
        if self.is_csv:
            return self.get_data_table_csv()
        else:
            return self.get_data_table_xls(table_name)

    def get_data_table_top(self, table_name, top_limit=100) ->pd.DataFrame:
        """
        Retrieves the top `top_limit` rows from the specified table in a memory-efficient way.Parameters:
        - table_name (str): The name of the table (for Excel files) or the dataset source.- top_limit (int): The number of rows to return (default: 100).Returns:
        - pd.DataFrame: A DataFrame containing the top rows of the table."""
        if self.is_csv:
            df = pd.read_csv(self.csv_path, sep=self.csv_delimiter, nrows=
                top_limit)
        else:
            df = pd.read_excel(self.csv_path, sheet_name=table_name, nrows=
                top_limit)
        return df

    def get_data_table_query(self, sql, table_name):
        """
        OVERRIDE get_data_table_query from db_connectors
        """

        def extract_table_name(sql_query):
            match = re.search('FROM\\s+(\\w+)', sql_query, re.IGNORECASE)
            if match:
                return match.group(1)
            return None
        sheet_name = extract_table_name(sql)
        globals()[sheet_name] = self.get_data_table(sheet_name)
        return duckdb.query(sql).df()

    def get_data_table_csv(self):
        """
        This method loads a table
        """
        if self.csv_delimiter is not None:
            return pd.read_csv(self.csv_path, sep=self.csv_delimiter)
        else:
            return pd.read_csv(self.csv_path)

    def get_data_table_xls(self, table_name):
        """
        This method loads a table
        """
        return pd.read_excel(self.csv_path, sheet_name=table_name)

#END OF QUBE
