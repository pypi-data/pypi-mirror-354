import os, sys
import json
import importlib
import traceback
import asyncio
import subprocess
import platform
from pathlib import Path
from channels.generic.websocket import WebsocketConsumer
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_8f0cad92aa import sparta_226d9606de
from project.logger_config import logger


class OutputRedirector:

    def __init__(self, websocket, filepath):
        self.websocket = websocket
        self.filepath = filepath
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.file = None

    def __enter__(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        self.file = open(self.filepath, 'w')


        class StreamHandler:

            def __init__(self, file, websocket):
                self.file = file
                self.websocket = websocket

            def write(self, message):
                if self.file:
                    self.file.write(message)
                if self.websocket:
                    try:
                        self.websocket.send(json.dumps({'res': 1000, 'msg':
                            message}))
                    except Exception as e:
                        logger.debug(f'WebSocket send error: {e}', file=
                            self.file)

            def flush(self):
                if self.file:
                    self.file.flush()
        self.custom_stream = StreamHandler(self.file, self.websocket)
        sys.stdout = self.custom_stream
        sys.stderr = self.custom_stream

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
        if self.file:
            self.file.close()


class ApiWebsocketWS(WebsocketConsumer):
    """

    """

    def connect(self):
        """
        Handle WebSocket connection
        """
        logger.debug('Connect Now')
        self.user = self.scope['user']
        self.accept()

    def disconnect(self, close_code=None):
        """
        Handle WebSocket disconnection
        """
        logger.debug('Disconnect')
        try:
            self.close()
        except:
            pass

    def receive(self, text_data):
        """
        Handle incoming WebSocket messages
        """
        if len(text_data) > 0:
            json_data = json.loads(text_data)
            is_run_mode = json_data.get('isRunMode', False)
            user_project_path = sparta_226d9606de(json_data['baseProjectPath'])
            user_backend_path = os.path.join(os.path.dirname(
                user_project_path), 'backend')
            sys.path.insert(0, user_backend_path)
            import sqWebsockets
            importlib.reload(sqWebsockets)
            service_name = json_data['service']
            post_data: dict = json_data.copy()
            del json_data['baseProjectPath']
            log_file_path = os.path.join(user_backend_path, 'logs',
                'output.log')
            if is_run_mode:
                webservice_res_dict = sqWebsockets.sparta_6fdef3e79c(service_name,
                    post_data, self.user)
                self.send(json.dumps(webservice_res_dict))
            else:
                with OutputRedirector(self, log_file_path):
                    try:
                        webservice_res_dict = sqWebsockets.sparta_6fdef3e79c(
                            service_name, post_data, self.user)
                        self.send(json.dumps(webservice_res_dict))
                    except Exception as e:
                        logger.debug(traceback.format_exc())
                        self.send(json.dumps({'res': -1, 'errorMsg': str(e)}))

#END OF QUBE
