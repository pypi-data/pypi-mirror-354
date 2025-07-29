import os
import time
import pandas as pd
import psycopg2
import mysql.connector
import pyodbc
import duckdb
import sqlite3
from pymongo import MongoClient
from sqlalchemy import create_engine, MetaData, Table, select, inspect, text
from multiprocessing import Pool
from project.logger_config import logger
libraries = {'cx_Oracle': 'cx_Oracle', 'redis': 'redis', 'couchdb':
    'couchdb', 'aerospike': 'aerospike', 'clickhouse_connect':
    'clickhouse_connect', 'questdb.ingress': 'questdb.ingress',
    'cassandra.cluster': 'cassandra.cluster', 'cassandra.auth':
    'cassandra.auth', 'influxdb_client': 'influxdb_client'}
summary = {}
for lib_name, module in libraries.items():
    try:
        __import__(module)
        summary[lib_name] = 'Available'
    except ImportError:
        summary[lib_name] = 'Not Installed'


class EngineBuilder:

    def __init__(self, host, port, user=None, password=None, database=None,
        engine_name='postgresql'):
        """
        
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.url_engine = (
            f'{engine_name}://{user}:{password}@{host}:{port}/{database}')
        self.error_msg_test_connection = ''

    def get_error_msg_test_connection(self) ->str:
        return self.error_msg_test_connection

    def set_url_engine(self, url_engine):
        """
        
        """
        self.url_engine = url_engine

    def set_database(self, database):
        """
        
        """
        self.database = database

    def set_file_path(self, file_path):
        """
        
        """
        self.file_path = file_path

    def set_keyspace_cassandra(self, keyspace_cassandra):
        """
        
        """
        self.keyspace_cassandra = keyspace_cassandra

    def set_redis_db(self, redis_db):
        """
        
        """
        self.redis_db = redis_db

    def set_database_path(self, database_path):
        """
        
        """
        self.database_path = database_path

    def set_socket_url(self, socket_url):
        """
        
        """
        self.socket_url = socket_url

    def set_json_url(self, json_url):
        """
        
        """
        self.json_url = json_url

    def set_dynamic_inputs(self, dynamic_inputs):
        """
        
        """
        self.dynamic_inputs = dynamic_inputs

    def set_py_code_processing(self, py_code_processing):
        """
        
        """
        self.py_code_processing = py_code_processing

    def set_library_arctic(self, database_path, library_arctic):
        """
        
        """
        self.database_path = database_path
        self.library_arctic = library_arctic

    def build_postgres(self):
        """
        
        """
        conn = psycopg2.connect(user=self.user, password=self.password,
            host=self.host, port=self.port, database=self.database)
        return conn

    def build_mysql(self):
        """
        
        """
        conn = mysql.connector.connect(host=self.host, user=self.user,
            passwd=self.password, port=self.port, database=self.database)
        return conn

    def build_mariadb(self):
        """

        """
        logger.debug(self.host)
        logger.debug(self.user)
        logger.debug(self.password)
        logger.debug(self.port)
        logger.debug(self.database)
        conn = mysql.connector.connect(host=self.host, user=self.user,
            passwd=self.password, port=self.port, database=self.database)
        return conn

    def build_mssql(self, trusted_connection, driver):
        try:
            conn = self.build_mssql_params(trusted_connection, driver)
            if conn is not None:
                return conn
            else:
                try:
                    conn = self.build_mssql_dsn(trusted_connection, driver)
                    if conn is not None:
                        return conn
                except:
                    pass
        except:
            conn = self.build_mssql_dsn(trusted_connection, driver)
            if conn is not None:
                return conn

    def build_mssql_params(self, trusted_connection, driver):
        """
        
        """
        try:
            server = f'{self.host}'
            if self.port is not None:
                if len(self.port) > 0:
                    server = f'{self.host},{self.port}'
            if trusted_connection:
                connection = pyodbc.connect(driver=f'{driver}', server=
                    server, database=f'{self.database}', trusted_connection
                    ='yes')
            else:
                connection = pyodbc.connect(driver=f'{driver}', server=
                    server, database=f'{self.database}', uid=f'{self.user}',
                    pwd=f'{self.password}')
            return connection
        except Exception as e:
            self.error_msg_test_connection = str(e)

    def build_mssql_dsn(self, trusted_connection, driver):
        """
        
        """
        try:
            if trusted_connection:
                connection = pyodbc.connect(
                    f'DRIVER={driver};SERVER={self.host},{self.port};DATABASE={self.database};Trusted_Connection=yes'
                    )
            else:
                connection = pyodbc.connect(
                    f'DRIVER={driver};SERVER={self.host},{self.port};DATABASE={self.database};UID={self.user};PWD={self.password}'
                    )
            return connection
        except Exception as e:
            self.error_msg_test_connection = str(e)

    def build_oracle(self, lib_dir=None, oracle_service_name='orcl'):
        """
        
        """
        import cx_Oracle
        if lib_dir is not None:
            try:
                cx_Oracle.init_oracle_client(lib_dir=lib_dir)
            except:
                pass
        dsn = cx_Oracle.makedsn(self.host, self.port, service_name=
            oracle_service_name)
        conn = cx_Oracle.connect(user=self.user, password=self.password,
            dsn=dsn, mode=cx_Oracle.SYSDBA)
        return conn

    def build_arctic(self, database_path, library_arctic):
        """
        
        """
        self.set_library_arctic(database_path, library_arctic)
        if database_path is not None:
            if len(database_path) > 0:
                logger.debug('database_path > ' + str(database_path))
                ac = adb.Arctic(database_path)
                return ac

    def build_cassandra(self, keyspace):
        """
        
        """
        from cassandra.cluster import Cluster
        self.set_keyspace_cassandra(keyspace)
        contact_points = [self.host]
        auth_provider = PlainTextAuthProvider(username=self.user, password=
            self.password) if self.user and self.password else None
        cluster = Cluster(contact_points=contact_points, port=self.port,
            auth_provider=auth_provider)
        return cluster

    def build_scylladb(self, keyspace):
        """
        
        """
        return self.build_cassandra(keyspace)

    def build_clickhouse(self):
        """
        
        """
        import clickhouse_connect
        try:
            client = clickhouse_connect.get_client(host=self.host, port=
                self.port, user=self.user, password=self.password, database
                =self.database)
            return client
        except:
            pass

    def build_couchdb(self):
        """
        
        """
        import couchdb
        try:
            url = f'{self.host}:{self.port}'
            couch = couchdb.Server(url)
            couch.resource.credentials = self.user, self.password
            return couch
        except:
            return None

    def build_aerospike(self):
        """
        
        """
        import aerospike
        config = {'hosts': [(self.host, self.port)]}
        if self.user and self.password:
            if len(self.user) > 0:
                config['user'] = self.user
            if len(self.password) > 0:
                config['password'] = self.password
        try:
            client = aerospike.client(config).connect()
            return client
        except:
            pass

    def build_redis(self, db=0):
        """
        
        """
        import redis
        self.set_redis_db(db)
        conn = redis.StrictRedis(host=self.host, port=self.port, password=
            self.password, username=self.user, db=db)
        return conn

    def build_duckdb(self, database_path, read_only=False):
        """
        
        """
        if database_path is None:
            return None
        if not os.path.exists(database_path) and database_path != ':memory:':
            return None
        self.set_database_path(database_path)
        conn = duckdb.connect(database_path, read_only=read_only)
        return conn

    def build_parquet(self, database_path, read_only=False):
        """
        
        """
        if database_path is None:
            return None
        if not os.path.exists(database_path) and database_path != ':memory:':
            return None
        self.set_database_path(database_path)
        conn = duckdb.connect()
        return conn

    def build_sqlite(self, database_path):
        """
        
        """
        self.set_database_path(database_path)
        conn = sqlite3.connect(database_path)
        return conn

    def build_questdb(self):
        """
        
        """
        from questdb.ingress import Sender, IngressError
        conf = f'http::addr={self.host}:{self.port};'
        if self.user is not None:
            if len(self.user) > 0:
                conf += f'username={self.user};'
        if self.password is not None:
            if len(self.password) > 0:
                conf += f'password={self.password};'
        return conf

    def build_mongo(self):
        """
        
        """
        client = MongoClient(host=self.host, port=self.port, username=self.user, password=self.password)
        return client

    def build_influxdb(self, token, organization, user, password):
        """
        
        """
        from influxdb_client import InfluxDBClient
        url = f'{self.host}:{self.port}'
        client = None
        if token is not None:
            if len(token) > 0:
                client = InfluxDBClient(url=url, token=token, org=organization)
        if client is None:
            if user is not None:
                if len(user) > 0:
                    client = InfluxDBClient(url=url, username=user,
                        password=password, org=organization)
        return client

    def build_csv(self, file_path):
        """
        
        """
        self.set_file_path(file_path)
        return self

    def build_xls(self, file_path):
        """
        
        """
        self.set_file_path(file_path)
        return self

    def build_json_api(self, json_url, dynamic_inputs=None,
        py_code_processing=None):
        """
        
        """
        self.set_json_url(json_url)
        self.set_dynamic_inputs(dynamic_inputs)
        self.set_py_code_processing(py_code_processing)

    def build_python(self, py_code_processing=None, dynamic_inputs=None):
        """
        
        """
        self.set_py_code_processing(py_code_processing)
        self.set_dynamic_inputs(dynamic_inputs)

    def build_wss(self, socket_url, dynamic_inputs=None, py_code_processing
        =None):
        """
        
        """
        self.set_socket_url(socket_url)
        self.set_dynamic_inputs(dynamic_inputs)
        self.set_py_code_processing(py_code_processing)

    def get_sqlachemy_engine(self):
        """
        SqlAlchemy Engine
        """
        return create_engine(self.url_engine)

    def get_available_views(self) ->list:
        """
        This method returns all the available views in the database using SQLAlchemy."""
        try:
            engine = self.get_sqlachemy_engine()
            insp = inspect(engine)
            views = insp.get_view_names()
            return sorted(views)
        except Exception as e:
            logger.debug('Exception while retrieving available views')
            logger.debug(e)
            return []

    def get_available_tables(self) ->list:
        """
        This method returns all the available tables of a database using sql_alchemy
        """
        try:
            engine = self.get_sqlachemy_engine()
            insp = inspect(engine)
            tables_name = insp.get_table_names()
            return sorted(tables_name)
        except Exception as e:
            logger.debug('Exception get available tables metadata')
            logger.debug(e)
            return []

    def get_table_columns(self, table_name) ->list:
        """
        This method returns all the available columns of a table using sql_alchemy
        """
        try:
            engine = self.get_sqlachemy_engine()
            inspector = inspect(engine)
            table_info = inspector.get_columns(table_name)
            if table_info:
                return [{'column': column['name'], 'type': str(column[
                    'type'])} for column in table_info]
        except Exception as e:
            logger.debug('Exception get table columuns metadata')
            logger.debug(e)
        return []

    def get_data_table(self, table_name):
        """
        This method loads a table
        """
        try:
            engine = self.get_sqlachemy_engine()
            sql_query = text(f'SELECT * FROM {table_name}')
            with engine.connect() as connection:
                result = connection.execute(sql_query)
                data = result.fetchall()
                return data
        except Exception as e:
            logger.debug(
                f"Exception while loading data from table '{table_name}'")
            logger.debug(e)
        return []

    def get_data_table_top(self, table_name, top_limit=100):
        """
        This method loads a table (top 100 elements)
        """
        try:
            engine = self.get_sqlachemy_engine()
            sql_query = text(f'SELECT * FROM {table_name} LIMIT {top_limit}')
            with engine.connect() as connection:
                result = connection.execute(sql_query)
                data = result.fetchall()
                return data
        except Exception as e:
            logger.debug(
                f"Exception while loading data from table '{table_name}'")
            logger.debug(e)
        return []

    def get_data_table_query(self, sql, table_name=None) ->pd.DataFrame:
        """
        This method loads a table by running and sql query
        Note: do not remove table_name input (for polymorphism)
        """
        if sql is not None:
            if len(sql) > 0:
                return self.read_sql_query(sql)
        return pd.DataFrame()

    def read_sql_query(self, sql, index_col=None, coerce_float=True, params
        =None, parse_dates=None, chunksize=None, dtype=None):
        """
        
        """
        return pd.read_sql_query(sql, con=self.connector, index_col=
            index_col, coerce_float=coerce_float, params=params,
            parse_dates=parse_dates, chunksize=chunksize, dtype=dtype)

#END OF QUBE
