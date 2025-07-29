import pandas as pd
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_0bbca76031 import EngineBuilder
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import convert_to_dataframe


class ScylladbConnector(EngineBuilder):

    def __init__(self, host, port, user, password, keyspace):
        """
        
        """
        self.keyspace = keyspace
        super().__init__(host=host, port=port, user=user, password=password,
            engine_name='scylladb')
        self.set_url_engine(
            f'cassandra://{user}:{password}@{host}:{port}/{keyspace}')
        self.cluster = self.build_scylladb(self.keyspace)
        self.connector = self.cluster.connect(keyspace)
        self.connector.set_keyspace(keyspace)

    def test_connection(self) ->bool:
        """
        Test connection
        """
        try:
            session = self.connector
            keyspaces = session.execute(
                'SELECT keyspace_name FROM system_schema.keyspaces')
            keyspace_names = [ks.keyspace_name for ks in keyspaces]
            if self.keyspace in keyspace_names:
                res = True
            else:
                self.error_msg_test_connection = (
                    f"Keyspace '{self.keyspace}' does not exist")
                res = False
            self.cluster.shutdown()
            return res
        except Exception as e:
            self.error_msg_test_connection = str(e)
            return False

    def get_available_tables(self) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available tables of a database
        """
        try:
            session = self.connector
            query = (
                f"SELECT table_name FROM system_schema.tables WHERE keyspace_name='{self.keyspace}'"
                )
            rows = session.execute(query)
            keyspace_names = [row.table_name for row in rows]
            self.cluster.shutdown()
            return keyspace_names
        except Exception as e:
            self.error_msg_test_connection = str(e)
            return []

    def get_table_columns(self, table_name) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available columns of a table
        """
        try:
            session = self.connector
            query = (
                f'SELECT column_name FROM system_schema.columns WHERE keyspace_name={self.keyspace} AND table_name={table_name}'
                )
            rows = session.execute(query)
            columns = [row.column_name for row in rows]
            self.cluster.shutdown()
            return columns
        except Exception as e:
            self.error_msg_test_connection = str(e)
            return []

    def get_data_table(self, table_name) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        try:
            session = self.connector
            query = f'SELECT * FROM {table_name}'
            rows = session.execute(query)
            data = [dict(row._asdict()) for row in rows]
            return convert_to_dataframe(data)
        except Exception as e:
            self.cluster.shutdown()
            raise Exception(e)

    def get_data_table_top(self, table_name, top_limit=100) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        try:
            session = self.connector
            query = f'SELECT * FROM {table_name} LIMIT {top_limit}'
            rows = session.execute(query)
            data = [dict(row._asdict()) for row in rows]
            return convert_to_dataframe(data)
        except Exception as e:
            self.cluster.shutdown()
            raise Exception(e)

    def get_data_table_query(self, sql, table_name=None) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        try:
            session = self.connector
            query = sql
            rows = session.execute(query)
            data = [dict(row._asdict()) for row in rows]
            return convert_to_dataframe(data)
        except Exception as e:
            self.cluster.shutdown()
            raise Exception(e)

#END OF QUBE
