import pandas as pd
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_0bbca76031 import EngineBuilder
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import convert_to_dataframe


class ArcticConnector(EngineBuilder):

    def __init__(self, database_path, library_arctic):
        """
        
        """
        self.database_path = database_path
        self.library_arctic = library_arctic
        super().__init__(host=None, port=None, engine_name='arctic')
        try:
            self.connector = self.build_arctic(database_path, library_arctic)
        except:
            self.connector = None

    def test_connection(self) ->bool:
        """
        Test connection
        """
        if self.database_path is None:
            self.error_msg_test_connection = 'Missing path or endpoint'
            return False
        if len(self.database_path) == 0:
            self.error_msg_test_connection = 'Missing path or endpoint'
            return False
        if self.library_arctic is None:
            self.error_msg_test_connection = 'Missing library'
            return False
        if len(self.library_arctic) == 0:
            self.error_msg_test_connection = 'Missing library'
            return False
        try:
            ac = self.connector
            if self.library_arctic in ac.list_libraries():
                return True
            else:
                self.error_msg_test_connection = (
                    'Invalid path folder, endpoint or library')
                return False
        except Exception as e:
            self.error_msg_test_connection = str(e)
            return False

    def get_available_tables(self) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available tables of a database
        """
        try:
            ac = self.connector
            lib = ac[self.library_arctic]
            return list(lib.list_symbols())
        except Exception as e:
            self.error_msg_test_connection = str(e)
            return []

    def get_table_columns(self, table_name) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available columns of a table
        """
        try:
            ac = self.connector
            lib = ac[self.library_arctic]
            metadata = lib.read_metadata(table_name)
            columns = metadata['schema']['fields']
            column_names = [field['name'] for field in columns]
            return column_names
        except Exception as e:
            self.error_msg_test_connection = str(e)
            return []

    def get_data_table(self, table_name) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        ac = self.connector
        lib = ac[self.library_arctic]
        return convert_to_dataframe(lib.read(table_name).data)

    def get_data_table_top(self, table_name, top_limit=100):
        """
        This method loads a table (top 100 elements)
        """
        res_df = self.get_data_table(table_name)
        try:
            return res_df.head(top_limit)
        except:
            return pd.DataFrame()

#END OF QUBE
