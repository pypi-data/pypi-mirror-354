import time
import json
import pandas as pd
from pandas.api.extensions import no_default
import project.sparta_8345d6a892.sparta_f0696e4f00.qube_3df3f7aa47 as qube_3df3f7aa47
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_419c8070aa.qube_ae4410d62b import AerospikeConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_b2e90d6ccc.qube_ea8fc4a4fe import CassandraConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_4fb5d546b2.qube_fc52d9fc5f import ClickhouseConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_513ccf7ac5.qube_61894ff70c import CouchdbConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_2a1acea8e5.qube_5e5a204618 import CsvConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_21161fa7fb.qube_0c51350988 import DuckDBConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_228d7405d1.qube_c6c94d8432 import JsonApiConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_3dfc430757.qube_dbc1b78b5a import InfluxdbConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_101d4c7bdb.qube_65f3d4230b import MariadbConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_eaf230feef.qube_31acf67bc4 import MongoConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_a7025ee38e.qube_28bd329046 import MssqlConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_fed68af56d.qube_70355453e9 import MysqlConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_bea376e844.qube_2bc55fb1fa import OracleConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_12610740c3.qube_35a9d2f2ad import ParquetConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_617c1a77d5.qube_93ce08e3e4 import PostgresConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_a03ca462df.qube_00130a7e8c import PythonConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_b2aec18b73.qube_d2c8f4d65b import QuestDBConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_4a607657ba.qube_c9baa7a49d import RedisConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_e2af8ae515.qube_967b22d80b import ScylladbConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_89dfdfb9fa.qube_bb7885368f import SqliteConnector
from project.sparta_8345d6a892.sparta_f0696e4f00.sparta_0943da523f.qube_22643c0cae import WssConnector
from project.logger_config import logger


class Connector:

    def __init__(self, db_engine='postgres'):
        """
        Init connector
        """
        self.db_engine = db_engine

    def close_db(self):
        """
        Close connection
        """
        try:
            self.connector.close()
        except:
            pass

    def init_with_model(self, connector_obj):
        """
        Init with SpartaQube Model
        """
        host = connector_obj.host
        port = connector_obj.port
        user = connector_obj.user
        password_e = connector_obj.password_e
        try:
            password = qube_3df3f7aa47.sparta_3f375a99fa(password_e)
        except:
            password = None
        try:
            if connector_obj.password is not None:
                password = connector_obj.password
        except:
            pass
        database = connector_obj.database
        oracle_service_name = connector_obj.oracle_service_name
        keyspace = connector_obj.keyspace
        library_arctic = connector_obj.library_arctic
        database_path = connector_obj.database_path
        read_only = connector_obj.read_only
        json_url = connector_obj.json_url
        socket_url = connector_obj.socket_url
        db_engine = connector_obj.db_engine
        csv_path = connector_obj.csv_path
        csv_delimiter = connector_obj.csv_delimiter
        token = connector_obj.token
        organization = connector_obj.organization
        lib_dir = connector_obj.lib_dir
        driver = connector_obj.driver
        trusted_connection = connector_obj.trusted_connection
        dynamic_inputs = []
        if connector_obj.dynamic_inputs is not None:
            try:
                dynamic_inputs = json.loads(connector_obj.dynamic_inputs)
            except:
                pass
        py_code_processing = connector_obj.py_code_processing
        self.db_engine = db_engine
        self.init_with_params(host=host, port=port, user=user, password=
            password, database=database, oracle_service_name=
            oracle_service_name, csv_path=csv_path, csv_delimiter=
            csv_delimiter, keyspace=keyspace, library_arctic=library_arctic,
            database_path=database_path, read_only=read_only, json_url=
            json_url, socket_url=socket_url, dynamic_inputs=dynamic_inputs,
            py_code_processing=py_code_processing, token=token,
            organization=organization, lib_dir=lib_dir, driver=driver,
            trusted_connection=trusted_connection)

    def init_with_params(self, host, port, user=None, password=None,
        database=None, oracle_service_name='orcl', csv_path=None,
        csv_delimiter=None, keyspace=None, library_arctic=None,
        database_path=None, read_only=False, json_url=None, socket_url=None,
        redis_db=0, token=None, organization=None, lib_dir=None, driver=
        None, trusted_connection=True, dynamic_inputs=None,
        py_code_processing=None):
        """
        Initialize database connector with params (exhaustive list with default values)
        """
        if self.db_engine == 'aerospike':
            self.db_connector = AerospikeConnector(host=host, port=port,
                user=user, password=password, database=database)
        if self.db_engine == 'cassandra':
            self.db_connector = CassandraConnector(host=host, port=port,
                user=user, password=password, keyspace=keyspace)
        if self.db_engine == 'clickhouse':
            self.db_connector = ClickhouseConnector(host=host, port=port,
                database=database, user=user, password=password)
        if self.db_engine == 'couchdb':
            self.db_connector = CouchdbConnector(host=host, port=port, user
                =user, password=password)
        if self.db_engine == 'csv':
            self.db_connector = CsvConnector(csv_path=csv_path,
                csv_delimiter=csv_delimiter)
        if self.db_engine == 'duckdb':
            self.db_connector = DuckDBConnector(database_path=database_path,
                read_only=read_only)
        if self.db_engine == 'influxdb':
            self.db_connector = InfluxdbConnector(host=host, port=port,
                token=token, organization=organization, bucket=database,
                user=user, password=password)
        if self.db_engine == 'json_api':
            self.db_connector = JsonApiConnector(json_url=json_url,
                dynamic_inputs=dynamic_inputs, py_code_processing=
                py_code_processing)
        if self.db_engine == 'mariadb':
            self.db_connector = MariadbConnector(host=host, port=port, user
                =user, password=password, database=database)
        if self.db_engine == 'mongo':
            self.db_connector = MongoConnector(host=host, port=port, user=
                user, password=password, database=database)
        if self.db_engine == 'mssql':
            self.db_connector = MssqlConnector(host=host, port=port,
                trusted_connection=trusted_connection, driver=driver, user=
                user, password=password, database=database)
        if self.db_engine == 'mysql':
            self.db_connector = MysqlConnector(host=host, port=port, user=
                user, password=password, database=database)
        if self.db_engine == 'oracle':
            self.db_connector = OracleConnector(host=host, port=port, user=
                user, password=password, database=database, lib_dir=lib_dir,
                oracle_service_name=oracle_service_name)
        if self.db_engine == 'parquet':
            self.db_connector = ParquetConnector(database_path=database_path)
        if self.db_engine == 'postgres':
            self.db_connector = PostgresConnector(host=host, port=port,
                user=user, password=password, database=database)
        if self.db_engine == 'python':
            self.db_connector = PythonConnector(py_code_processing=
                py_code_processing, dynamic_inputs=dynamic_inputs)
        if self.db_engine == 'questdb':
            self.db_connector = QuestDBConnector(host=host, port=port, user
                =user, password=password, database=database)
        if self.db_engine == 'redis':
            self.db_connector = RedisConnector(host=host, port=port, user=
                user, password=password, db=redis_db)
        if self.db_engine == 'scylladb':
            self.db_connector = ScylladbConnector(host=host, port=port,
                user=user, password=password, keyspace=keyspace)
        if self.db_engine == 'sqlite':
            self.db_connector = SqliteConnector(database_path=database_path)
        if self.db_engine == 'wss':
            self.db_connector = WssConnector(socket_url=socket_url,
                dynamic_inputs=dynamic_inputs, py_code_processing=
                py_code_processing)

    def get_db_connector(self):
        """
        Returns implemented db_connector object (like CsvConnector, WssConnector etc...)
        """
        return self.db_connector

    def test_connection(self) ->bool:
        """
        This method test the connector of the connector
        """
        return self.db_connector.test_connection()

    def preview_output_connector_bowler(self) ->str:
        """
        Preview connector output
        """
        return self.db_connector.preview_output_connector_bowler()

    def get_error_msg_test_connection(self) ->str:
        """
        Return error message (in case test_connection failed and return False)       
        """
        return self.db_connector.get_error_msg_test_connection()

    def get_available_tables(self) ->list:
        """
        This method returns the list of all available tables of the database
        """
        tables = self.db_connector.get_available_tables()
        return tables

    def get_available_views(self) ->list:
        """
        This method returns the list of all available tables of the database
        """
        views = self.db_connector.get_available_views()
        return views

    def get_table_columns(self, table_name) ->list:
        """
        This method returns the list of all columns of a specific table
        """
        table_columns = self.db_connector.get_table_columns(table_name)
        return table_columns

    def get_data_table(self, table_name) ->pd.DataFrame:
        """
        This method loads a table
        """
        if self.db_engine == 'json_api':
            return self.db_connector.get_json_api_dataframe()
        else:
            data_table = self.db_connector.get_data_table(table_name)
            if isinstance(data_table, pd.DataFrame):
                return data_table
            return pd.DataFrame(data_table)

    def get_data_table_top(self, table_name, top_limit=100) ->pd.DataFrame:
        """
        This method loads a table
        """
        if self.db_engine == 'json_api':
            return self.db_connector.get_json_api_dataframe()
        else:
            data_table = self.db_connector.get_data_table_top(table_name,
                top_limit)
            if isinstance(data_table, pd.DataFrame):
                return data_table
            return pd.DataFrame(data_table)

    def get_data_table_query(self, sql, table_name=None):
        """
        This method loads a table by running and sql query
        """
        return self.db_connector.get_data_table_query(sql, table_name=
            table_name)

#END OF QUBE
