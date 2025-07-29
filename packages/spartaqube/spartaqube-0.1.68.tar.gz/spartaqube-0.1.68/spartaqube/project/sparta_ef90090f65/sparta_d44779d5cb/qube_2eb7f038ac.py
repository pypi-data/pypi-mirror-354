import os
import json
import platform
import websocket
import threading
import time
import pandas as pd
from project.sparta_8688631f3d.sparta_5d2f5154f8 import qube_82ff246dc8 as qube_82ff246dc8
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_8f0cad92aa import convert_to_dataframe
from project.sparta_8688631f3d.sparta_577b784581.qube_2949549c51 import Connector as Connector
from project.logger_config import logger
IS_WINDOWS = False
if platform.system() == 'Windows':
    IS_WINDOWS = True
from channels.generic.websocket import WebsocketConsumer
from project.sparta_ef90090f65.sparta_40861746d9 import qube_380ad6266d as qube_380ad6266d
from project.sparta_8688631f3d.sparta_c77f2d3c37 import qube_8f0cad92aa as qube_8f0cad92aa


class WssConnectorWS(WebsocketConsumer):
    """

    """
    channel_session = True
    http_user_and_session = True

    def connect(self):
        """
        
        """
        logger.debug('Connect Now')
        self.accept()
        self.user = self.scope['user']
        self.json_data_dict = dict()

    def init_socket(self, json_data):
        is_model_connector = json_data['is_model_connector']
        self.connector_obj = Connector(db_engine='wss')
        if is_model_connector:
            connector_id = json_data['connector_id']
            db_connector_obj = qube_82ff246dc8.sparta_8aea4a0475(connector_id,
                self.user)
            if db_connector_obj is None:
                res = {'res': -2, 'errorMsg':
                    'Invalid connector, please try again'}
                resJson = json.dumps(res)
                self.send(text_data=resJson)
                return
            self.connector_obj.init_with_model(db_connector_obj)
        else:
            self.connector_obj.init_with_params(host=json_data['host'],
                port=json_data['port'], user=json_data['user'], password=
                json_data['password'], database=json_data['database'],
                oracle_service_name=json_data['oracle_service_name'],
                csv_path=json_data['csv_path'], csv_delimiter=json_data[
                'csv_delimiter'], keyspace=json_data['keyspace'],
                library_arctic=json_data['library_arctic'], database_path=
                json_data['database_path'], read_only=json_data['read_only'
                ], json_url=json_data['json_url'], socket_url=json_data[
                'socket_url'], redis_db=json_data['redis_db'],
                dynamic_inputs=json_data['dynamic_inputs'],
                py_code_processing=json_data['py_code_processing'])
        self.connector_obj.get_db_connector().start_stream(gui_websocket=self)

    def disconnect(self, close_code):
        """
        Release memory
        """
        logger.debug('Disconnect')
        try:
            self.connector_obj.get_db_connector().stop_threads()
        except:
            pass
        try:
            self.close()
        except:
            pass

    def receive(self, text_data):
        if len(text_data) > 0:
            json_data = json.loads(text_data)
            service = json_data['service']
            if service == 'init-socket':
                self.init_socket(json_data)
                res = {'res': 1, 'service': service}
                resJson = json.dumps(res)
                self.send(text_data=resJson)
            if service == 'stop-socket':
                self.connector_obj.get_db_connector().stop_stream(gui_websocket
                    =self)

#END OF QUBE
