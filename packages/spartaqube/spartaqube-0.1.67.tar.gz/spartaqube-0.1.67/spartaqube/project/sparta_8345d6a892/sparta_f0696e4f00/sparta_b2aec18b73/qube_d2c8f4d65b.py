try:
    from questdb.ingress import Sender, IngressError, TimestampNanos
except:
    pass
import os
import time
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_0bbca76031 import EngineBuilder
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import convert_to_dataframe


class QuestDBConnector(EngineBuilder):

    def __init__(self, host, port, user, password, database):
        """
        
        """
        self.proxies_dict = {'http': os.environ.get('http_proxy', None),
            'https': os.environ.get('https_proxy', None)}
        if host.startswith('localhost'):
            host = 'http://localhost'
        super().__init__(host=host, port=port, user=user, password=password,
            database=database, engine_name='questdb')
        self.conf = self.build_questdb()

    def test_connection(self) ->bool:
        """
        Test connection
        """
        try:
            with Sender.from_conf(self.conf) as sender:
                sender.flush()
            return True
        except IngressError as e:
            self.error_msg_test_connection = str(e)
            return False

    def get_available_tables(self) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available tables of a database
        """
        url = f'{self.host}:{self.port}/exec'
        query = 'SHOW TABLES'
        try:
            response = requests.get(url, params={'query': query}, auth=
                HTTPBasicAuth(self.user, self.password), proxies=self.proxies_dict)
            response.raise_for_status()
            data = response.json()
            tables = [row[0] for row in data['dataset']]
            return sorted(tables)
        except requests.RequestException as e:
            self.error_msg_test_connection = str(e)
            return []

    def get_table_columns(self, table_name) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available columns of a table
        """
        url = f'{self.host}:{self.port}/exec'
        query = f'SHOW COLUMNS FROM {table_name}'
        try:
            response = requests.get(url, params={'query': query}, auth=
                HTTPBasicAuth(self.user, self.password), proxies=self.proxies_dict)
            response.raise_for_status()
            data = response.json()
            tables = [row['table'] for row in data['dataset']]
            return tables
        except requests.RequestException as e:
            self.error_msg_test_connection = str(e)
            return []

    def get_data_table(self, table_name) ->pd.DataFrame:
        """
        
        """
        url = f'{self.host}:{self.port}/exec'
        query = f'SELECT * FROM {table_name}'
        response = requests.get(url, params={'query': query}, auth=
            HTTPBasicAuth(self.user, self.password), proxies=self.proxies_dict)
        response.raise_for_status()
        data = response.json()
        columns = [row['name'] for row in data['columns']]
        res_df = convert_to_dataframe(data['dataset'])
        res_df.columns = columns
        return res_df

    def get_data_table_top(self, table_name, top_limit=100) ->pd.DataFrame:
        """
        
        """
        url = f'{self.host}:{self.port}/exec'
        query = f'SELECT * FROM {table_name} LIMIT {top_limit}'
        response = requests.get(url, params={'query': query}, auth=
            HTTPBasicAuth(self.user, self.password), proxies=self.proxies_dict)
        response.raise_for_status()
        data = response.json()
        columns = [row['name'] for row in data['columns']]
        res_df = convert_to_dataframe(data['dataset'])
        res_df.columns = columns
        return res_df

    def get_data_table_query(self, sql, table_name=None) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        url = f'{self.host}:{self.port}/exec'
        query = sql
        response = requests.get(url, params={'query': query}, auth=
            HTTPBasicAuth(self.user, self.password), proxies=self.proxies_dict)
        response.raise_for_status()
        data = response.json()
        columns = [row['name'] for row in data['columns']]
        res_df = convert_to_dataframe(data['dataset'])
        res_df.columns = columns
        return res_df

#END OF QUBE
