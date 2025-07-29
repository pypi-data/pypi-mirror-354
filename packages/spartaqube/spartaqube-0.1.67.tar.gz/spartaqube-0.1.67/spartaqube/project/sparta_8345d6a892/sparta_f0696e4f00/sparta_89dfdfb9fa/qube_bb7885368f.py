import sqlite3
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_0bbca76031 import EngineBuilder
from project.logger_config import logger


class SqliteConnector(EngineBuilder):

    def __init__(self, database_path):
        """
        
        """
        super().__init__(host=None, port=None, engine_name='sqlite')
        self.database_path = database_path
        self.set_url_engine(f'sqlite:///{self.database_path}')
        self.connector = self.connect_db()

    def connect_db(self):
        return self.build_sqlite(database_path=self.database_path)

    def test_connection(self) ->bool:
        """
        Test connection
        """
        try:
            if self.connector:
                self.connector.close()
                return True
            else:
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
            connection = self.connector
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';"
                )
            table_names = cursor.fetchall()
            connection.close()
            return sorted([this_obj[0] for this_obj in table_names])
        except Exception as e:
            logger.debug('get available tables error')
            logger.debug(e)
        try:
            connection.close()
        except:
            pass
        return []

    def get_table_columns(self, table_name) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available columns of a table
        """
        try:
            connection = self.connector
            cursor = connection.cursor()
            cursor.execute(f'PRAGMA table_info({table_name});')
            columns_info = cursor.fetchall()
            column_list = [{'column': column[1], 'type': column[2]} for
                column in columns_info]
            connection.close()
            return column_list
        except Exception as e:
            logger.debug('get available tables error')
            logger.debug(e)
        try:
            connection.close()
        except:
            pass
        return []

#END OF QUBE
