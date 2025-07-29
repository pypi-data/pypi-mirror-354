try:
    import couchdb
except:
    pass
import pandas as pd
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_0bbca76031 import EngineBuilder
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import convert_to_dataframe
from project.logger_config import logger


class CouchdbConnector(EngineBuilder):

    def __init__(self, host, port, user, password):
        """
        
        """
        if host.startswith('localhost'):
            host = 'http://localhost'
        super().__init__(host=host, port=port, user=user, password=password,
            engine_name='couchdb')
        self.connector = self.build_couchdb()

    def test_connection(self) ->bool:
        """
        Test connection
        """
        try:
            url = f'{self.host}:{self.port}'
            couch = couchdb.Server(url)
            couch.resource.credentials = self.user, self.password
            try:
                if self.database in couch:
                    db = couch[self.database]
                    return True
                else:
                    self.error_msg_test_connection = 'Invalid database'
                    return False
            except Exception as e:
                self.error_msg_test_connection = 'Invalid user/password'
        except Exception as e:
            self.error_msg_test_connection = str(e)
            return False

    def get_available_tables(self) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available tables of a database
        """
        try:
            db = self.connector
            databases = list(db)
            return databases
        except Exception as e:
            logger.debug(e)
            return []

    def get_table_columns(self, table_name) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available columns of a table
        """
        try:
            db = self.connector
            database = table_name
            doc_id = table_name
            doc = db[doc_id]
            fields = list(doc.keys())
            return fields
        except Exception as e:
            return []

    def get_data_table(self, table_name) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        documents = []
        db = self.connector[table_name]
        documents = []
        for row in db.view('_all_docs', include_docs=True):
            documents.append(row.doc)
        return convert_to_dataframe(pd.DataFrame(documents))

    def get_data_table_top(self, table_name, top_limit=100) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        documents = []
        db = self.connector[table_name]
        documents = []
        for row in db.view('_all_docs', include_docs=True, limit=top_limit):
            documents.append(row.doc)
        return convert_to_dataframe(pd.DataFrame(documents))

    def get_data_table_query(self, sql, table_name=None) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        exec(sql, globals(), locals())
        selector_to_apply = eval('selector')
        query = {'selector': selector_to_apply}
        documents = []
        db = self.connector[table_name]
        result = db.find(query)
        documents = [doc for doc in result]
        return convert_to_dataframe(pd.DataFrame(documents))

#END OF QUBE
