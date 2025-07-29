import os, sys
import json
import base64
import cloudpickle
import importlib
import traceback
import asyncio
import subprocess
import platform
from django.conf import settings
from pathlib import Path
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from spartaqube_app.path_mapper_obf import sparta_bff35427ab
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_8f0cad92aa import sparta_226d9606de
from project.sparta_8688631f3d.sparta_2a93ddec7a.qube_9b8a1e243b import SenderKernel
from project.sparta_8688631f3d.sparta_34d32fb8c6.qube_cbe6ad2077 import sparta_4bb56d08cd, sparta_5fddc0f473
from project.logger_config import logger


class OutputRedirector:

    def __init__(self, websocket):
        self.websocket = websocket
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

    def __enter__(self):


        class StreamHandler:

            def __init__(self, websocket):
                self.websocket = websocket

            def write(self, message):
                if self.websocket:
                    try:
                        self.websocket.send(json.dumps({'res': 1000, 'msg':
                            message}))
                    except Exception as e:
                        logger.debug(f'WebSocket send error: {e}')
        self.custom_stream = StreamHandler(self.websocket)
        sys.stdout = self.custom_stream
        sys.stderr = self.custom_stream

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr


class ApiWebserviceWS(AsyncWebsocketConsumer):
    """

    """

    async def prepare_sender_kernel(self, kernel_manager_uuid):
        """
        
        """
        from project.models import KernelProcess
        kernel_process_list = await sync_to_async(lambda : list(
            KernelProcess.objects.filter(kernel_manager_uuid=
            kernel_manager_uuid)), thread_sensitive=False)()
        if len(kernel_process_list) > 0:
            kernel_process_obj = kernel_process_list[0]
            port = kernel_process_obj.port
            if self.sender_kernel_obj is None:
                self.sender_kernel_obj = SenderKernel(self, port)
            self.sender_kernel_obj.zmq_connect()

    async def connect(self):
        """
        Handle WebSocket connection
        """
        await self.accept()
        self.user = self.scope['user']
        self.sender_kernel_obj = None

    async def disconnect(self, close_code=None):
        """
        Handle WebSocket disconnection
        """
        logger.debug('Disconnect')
        try:
            await self.close()
        except:
            pass

    async def init_kernel_import_models(self, user_project_path):
        """
        This function import the 
        """
        user_backend_path = os.path.join(os.path.dirname(user_project_path),
            'backend')
        user_backend_app_path = os.path.join(user_backend_path, 'app')
        init_kernel_code = f"""
%load_ext autoreload
%autoreload 2    
import os, sys
import django
# Set the Django settings module
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
sys.path.insert(0, r"{user_backend_app_path}")
os.chdir(r"{user_backend_app_path}")
os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'
# Initialize Django
django.setup()
"""
        await self.sender_kernel_obj.send_zmq_request({'service':
            'execute_code', 'cmd': init_kernel_code})

    async def init_kernel(self, kernel_manager_uuid, user_project_path):
        await self.prepare_sender_kernel(kernel_manager_uuid)
        await self.init_kernel_import_models(user_project_path)

    async def receive(self, text_data):
        """
        Handle incoming WebSocket messages
        """
        if len(text_data) > 0:
            json_data = json.loads(text_data)
            kernel_manager_uuid = json_data['kernelManagerUUID']
            is_run_mode = json_data.get('isRunMode', False)
            init_only = json_data.get('initOnly', False)
            user_project_path = sparta_226d9606de(json_data['baseProjectPath'])
            user_backend_path = os.path.join(os.path.dirname(
                user_project_path), 'backend')
            service_name = json_data['service']
            post_data: dict = json_data.copy()
            await self.init_kernel(kernel_manager_uuid, user_project_path)
            if init_only:
                await self.send(json.dumps({'res': 1}))
                return
            code_to_exec = 'import os, sys, importlib\n'
            code_to_exec += f'sys.path.insert(0, r"{user_backend_path}")\n'
            code_to_exec += f'import webservices\n'
            code_to_exec += f'importlib.reload(webservices)\n'
            code_to_exec += f"""webservice_res_dict = webservices.sparta_573f98207c(service_name, post_data)
"""
            dict_var_to_workspace = {'service_name': service_name,
                'post_data': post_data}
            encoded_dict = base64.b64encode(cloudpickle.dumps(
                dict_var_to_workspace)).decode('utf-8')
            await self.sender_kernel_obj.send_zmq_request({'service':
                'set_workspace_variables', 'encoded_dict': encoded_dict})
            await self.sender_kernel_obj.send_zmq_request({'service':
                'execute_code', 'cmd': code_to_exec})
            webservice_res_dict = (await self.sender_kernel_obj.send_zmq_request({'service': 'get_workspace_variable',
                'kernel_variable': 'webservice_res_dict'}))
            if webservice_res_dict is not None:
                webservice_res_dict['webservice_resolve'] = 1
                await self.send(json.dumps(webservice_res_dict))

#END OF QUBE
