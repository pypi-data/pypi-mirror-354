import os
import gc
import re
import json
import time
import websocket
import cloudpickle
import base64
import getpass
import platform
import asyncio
from pathlib import Path
from pprint import pprint
from jupyter_client import KernelManager
from IPython.display import display, Javascript
from IPython.core.magics.namespace import NamespaceMagics
from nbconvert.filters import strip_ansi
from django.conf import settings as conf_settings
from spartaqube_app.path_mapper_obf import sparta_b6a401eb72
from project.sparta_312a90fa32.qube_0b39529dd9 import timeout
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import convert_to_dataframe, sparta_ad557db230
from project.sparta_8345d6a892.sparta_952c41e91e.qube_ef9e4f9eb1 import sparta_9c89cfd808
from project.logger_config import logger
B_DEBUG = False
SEND_INTERVAL = 0.8


def sparta_1d9b406406():
    return conf_settings.DEFAULT_TIMEOUT


def sparta_5d7b05cc58(file_path=None, text=None, b_log=True):
    if text is None:
        return
    if file_path is None:
        file_path = 'C:\\Users\\benme\\Desktop\\LOG_DEBUG.txt'
    try:
        mode = 'a' if os.path.exists(file_path) and os.path.getsize(file_path
            ) > 0 else 'w'
        with open(file_path, mode, encoding='utf-8') as file:
            if mode == 'a':
                file.write('\n')
            file.write(text)
        if b_log:
            logger.debug(f'Successfully wrote/appended to {file_path}')
    except Exception as e:
        if b_log:
            logger.debug(f'Error writing to file: {e}')


class KernelException(Exception):

    def __init__(self, message):
        super().__init__(message)
        if B_DEBUG:
            logger.debug('KernelException message')
            logger.debug(message)
        self.traceback_msg = message

    def get_traceback_errors(self):
        return self.traceback_msg


class IPythonKernel:
    """
        This class is designed to handle the IPython Kernel with the Client session
    """

    def __init__(self, api_key=None, django_settings_module=None,
        project_folder=None):
        self.api_key = api_key
        self.workspaceVarNameArr = []
        self.django_settings_module = django_settings_module
        self.project_folder = project_folder
        self.output_queue = []
        self.last_send_time = time.time()
        self.kernel_manager = KernelManager()
        self.zmq_identity = None
        self.zmq_request_dict = dict()

    async def initialize(self):
        """This async method should be called after creating an instance."""
        await self.startup_kernel()

    async def startup_kernel(self):
        """
        Startup and initialize kernel
        """
        if self.django_settings_module is not None:
            env = os.environ.copy()
            env['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
            self.kernel_manager.start_kernel(env=env)
        else:
            self.kernel_manager.start_kernel()
        self.kernel_client = self.kernel_manager.client()
        self.kernel_client.start_channels()
        try:
            self.kernel_client.wait_for_ready()
            start_time = time.time()
            logger.debug('Ready, initialize with Django')
            await self.initialize_kernel()
            logger.debug('--- %s seconds ---' % (time.time() - start_time))
        except Exception as e:
            logger.debug('Exception runtime now')
            self.kernel_client.stop_channels()
            self.kernel_manager.shutdown_kernel()

    def set_zmq_identity(self, zmq_identity):
        self.zmq_identity = zmq_identity
        self.output_queue = []
        self.last_send_time = time.time()

    def set_zmq_request(self, zmq_request_dict: dict):
        self.zmq_request_dict = zmq_request_dict

    async def send_sync(self, websocket, data, is_terminated=False):
        self.output_queue.append(data)
        if time.time() - self.last_send_time >= SEND_INTERVAL or is_terminated:
            if B_DEBUG:
                logger.debug(
                    f'Send batch now Interval diff: {time.time() - self.last_send_time}'
                    )
            await self.send_batch(websocket, is_terminated=is_terminated)

    async def send_batch(self, websocket, is_terminated=False):
        """
        
        """
        socket_name = (
            f'{websocket.__class__.__module__}.{websocket.__class__.__name__}')
        if len(self.output_queue) > 0:
            if websocket is not None:
                batch_output_dict = {'res': 1, 'is_terminated':
                    is_terminated, 'service': 'exec', 'batch_output': json.dumps(self.output_queue)}
                if socket_name == 'zmq.asyncio.Socket':
                    await websocket.send_multipart([self.zmq_identity, json.dumps(batch_output_dict).encode()])
                else:
                    websocket.send(json.dumps(batch_output_dict))
                self.output_queue = []
                self.last_send_time = time.time()
        else:
            terminated_dict = {'res': 1, 'is_terminated': True, 'method':
                'send_batch', 'service': 'break-loop', 'service-req': self.zmq_request_dict.get('service', '-1')}
            if websocket is not None:
                if socket_name == 'zmq.asyncio.Socket':
                    await websocket.send_multipart([self.zmq_identity, json.dumps(terminated_dict).encode()])
                else:
                    websocket.send(json.dumps(terminated_dict))
                self.output_queue = []
                self.last_send_time = time.time()

    def get_kernel_manager(self):
        """
        
        """
        return self.kernel_manager

    def get_kernel_client(self):
        """
        
        """
        return self.kernel_client

    async def initialize_kernel(self):
        """
        Kernel initialization with django setup
        """
        ini_code = 'import os, sys\n'
        ini_code += 'import django\n'
        ini_code += 'os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"\n'
        if self.project_folder is not None:
            code_multi_db = f"""user_app_db_path = r"{os.path.join(self.project_folder, 'app', 'db.sqlite3')}\"
"""
            code_multi_db += 'from django.conf import settings\n'
            code_multi_db += 'user_app_name = "notebook_app"\n'
            code_multi_db += """settings.DATABASES[user_app_name] = {"ENGINE": "django.db.backends.sqlite3", "NAME": user_app_db_path}
"""
            ini_code += code_multi_db
        ini_code += 'django.setup()\n'
        project_path = sparta_b6a401eb72()['project']
        core_api_path = sparta_b6a401eb72()['project/core/api']
        ini_code += f'sys.path.insert(0, r"{str(project_path)}")\n'
        ini_code += f'sys.path.insert(0, r"{str(core_api_path)}")\n'
        ini_code += f'os.environ["api_key"] = "{self.api_key}"\n'
        if self.project_folder is not None:
            ini_code += f'os.chdir(r"{self.project_folder}")\n'
        logger.debug('ini_code')
        logger.debug(ini_code)
        await self.execute(ini_code, b_debug=False)
        await self.backup_venv_at_startup()

    async def backup_venv_at_startup(self):
        """
        This function back up both PATH and VIRTUAL_ENV environment variables in order to switch to another virtual environment
        We are using the default spartaqube environment that we augment with the selected virtual environment.This is run only once, at startup of the kernel
        """
        backup_venv_cmd = f"""import sys, os, json
os.environ["PATH_BK"] = os.environ["PATH"]
os.environ["VIRTUAL_ENV_BK"] = os.environ["VIRTUAL_ENV"]
os.environ["SYS_PATH_BK"] = json.dumps(sys.path)
"""
        await self.execute(backup_venv_cmd)

    async def activate_venv(self, venv_name):
        """
        Activate a specific virtual environment
        """

        def get_sq_venv_base_path() ->str:
            """
            This function returns the folder path for the venv (sq_venv)
            """
            spartaqube_volume_path = sparta_9c89cfd808()
            default_project_path = os.path.join(spartaqube_volume_path,
                'sq_venv')
            default_project_path = os.path.normpath(default_project_path)
            os.makedirs(default_project_path, exist_ok=True)
            return default_project_path

        def get_sq_venv_selected_path() ->str:
            """
            Returns the selected virtual environment path
            """
            return os.path.normpath(os.path.join(get_sq_venv_base_path(),
                venv_name))

        def get_venv_script_path() ->str:
            """
            Example: C:\\Users\\benme\\SpartaQube\\sq_venv\\test_env\\Script
            """
            if os.name == 'nt':
                scripts_folder = os.path.join(get_sq_venv_selected_path(),
                    'Scripts')
            else:
                scripts_folder = os.path.join(get_sq_venv_selected_path(),
                    'bin')
            return os.path.normpath(scripts_folder)

        def get_venv_site_package_path() ->str:
            """
            Example: C:\\Users\\benme\\SpartaQube\\sq_venv\\test_env\\Lib\\site-packages
            """
            if os.name == 'nt':
                site_packages_folder = os.path.join(get_sq_venv_selected_path
                    (), 'Lib', 'site-packages')
            else:
                python_version_folder = (
                    f'python{sys.version_info.major}.{sys.version_info.minor}')
                site_packages_folder = os.path.join(get_sq_venv_selected_path
                    (), 'lib', python_version_folder, 'site-packages')
            return os.path.normpath(site_packages_folder)
        restore_ini_venv_cmd = f"""import sys, os
os.environ["PATH"] = os.environ["PATH_BK"]
os.environ["VIRTUAL_ENV"] = os.environ["VIRTUAL_ENV_BK"]
"""
        add_selected_venv = f"""os.environ["PATH"] = r"{get_venv_script_path()};" + os.environ["PATH"] 
site_packages_path = r"{get_venv_site_package_path()}"
sys.path = [elem for elem in sys.path if "site-packages" not in elem] 
sys.path.insert(0, site_packages_path)
"""
        cmd_to_execute = restore_ini_venv_cmd + add_selected_venv
        logger.debug('+' * 100)
        logger.debug('cmd_to_execute activate VENV')
        logger.debug(cmd_to_execute)
        logger.debug('+' * 100)
        await self.execute(cmd_to_execute)

    async def deactivate_venv(self):
        """
        Deactivate virtual environment and reset the sys.path to the initial sys.path at startup
        """
        restore_ini_venv_and_sys_path_cmd = f"""import sys, os, json
os.environ["PATH"] = os.environ["PATH_BK"]
os.environ["VIRTUAL_ENV"] = os.environ["VIRTUAL_ENV_BK"]
sys.path = json.loads(os.environ["SYS_PATH_BK"])
"""
        await self.execute(restore_ini_venv_and_sys_path_cmd)

    def stop_kernel(self):
        """
        Stop the kernel
        """
        self.kernel_client.stop_channels()
        self.kernel_manager.interrupt_kernel()
        self.kernel_manager.shutdown_kernel(now=True)

    async def cd_to_notebook_folder(self, notebook_path, websocket=None):
        """
        cd to a specific folder
        """
        cmd = f'import os, sys\n'
        cmd += f"os.chdir('{notebook_path}')\n"
        cmd += f"sys.path.insert(0, '{notebook_path}')"
        await self.execute(cmd, websocket)

    def escape_ansi(self, line):
        """
        
        """
        ansi_escape = re.compile('\\x1B(?:[@-Z\\\\-_]|\\[[0-?]*[ -/]*[@-~])')
        ansi_escape = re.compile(
            '(?:\\x1B[@-_]|[\\x80-\\x9F])[0-?]*[ -/]*[@-~]')
        ansi_escape = re.compile('(\\x9B|\\x1B\\[)[0-?]*[ -/]*[@-~]')
        ansi_regex = (
            '\\x1b((\\[\\??\\d+[hl])|([=<>a-kzNM78])|([\\(\\)][a-b0-2])|(\\[\\d{0,2}[ma-dgkjqi])|(\\[\\d+;\\d+[hfy]?)|(\\[;?[hf])|(#[3-68])|([01356]n)|(O[mlnp-z]?)|(/Z)|(\\d+)|(\\[\\?\\d;\\d0c)|(\\d;\\dR))'
            )
        ansi_escape = re.compile(ansi_regex, flags=re.IGNORECASE)
        return ansi_escape.sub('', line)

    async def execute(self, cmd, websocket=None, cell_id=None, b_debug=False):
        """
        Execute a python command in the kernel
        """
        self.last_send_time = time.time()
        msg_id = self.kernel_client.execute(cmd)
        state = 'busy'
        data = None
        has_execution_failed = False
        while state != 'idle' and self.kernel_client.is_alive():
            try:
                msg = self.kernel_client.get_iopub_msg()
                if not 'content' in msg:
                    continue
                content = msg['content']
                if B_DEBUG or b_debug:
                    logger.debug(
                        '/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/'
                        )
                    logger.debug(type(content))
                    logger.debug(content)
                    logger.debug(content.keys())
                    logger.debug(
                        '/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/'
                        )
                if 'traceback' in content:
                    if B_DEBUG or b_debug:
                        logger.debug('TRACEBACK RAISE EXCEPTION NOW')
                        logger.debug(content)
                    ipython_input_pat = re.compile(
                        '<ipython-input-\\d+-[0-9a-f]+>')
                    tb = [re.sub(ipython_input_pat, '<IPY-INPUT>',
                        strip_ansi(line)) for line in content['traceback']]
                    data = KernelException('\n'.join(tb))
                    if websocket is not None:
                        resJson = json.dumps({'res': -1, 'cell_id': cell_id,
                            'service': 'exec', 'errorMsg': '\n'.join(tb),
                            'errorMsgRaw': content})
                        await self.send_sync(websocket, resJson,
                            is_terminated=True)
                        has_execution_failed = True
                if 'name' in content:
                    if content['name'] == 'stdout':
                        data = content['text']
                        output_dict = self.format_output(data)
                        resJson = json.dumps({'res': 1, 'service': 'exec',
                            'output': output_dict, 'cell_id': cell_id})
                        await self.send_sync(websocket, resJson)
                    if content['name'] == 'stderr':
                        data = content['text']
                        resJson = json.dumps({'res': -1, 'cell_id': cell_id,
                            'service': 'exec', 'errorMsg': data})
                        await self.send_sync(websocket, resJson,
                            is_terminated=False)
                if 'data' in content:
                    data = content['data']
                    output_dict = self.format_output(data)
                    resJson = json.dumps({'res': 1, 'service': 'exec',
                        'output': output_dict, 'cell_id': cell_id})
                    await self.send_sync(websocket, resJson)
                if 'execution_state' in content:
                    state = content['execution_state']
            except Exception as e:
                logger.debug('Execute exception EXECUTION')
                logger.debug(e)
                has_execution_failed = True
        if not has_execution_failed:
            await self.send_batch(websocket, is_terminated=True)
        return data

    async def execute_shell(self, cmd, websocket=None, cell_id=None,
        b_debug=False):
        """
        Execute a shell command in the kernel
        """
        cmd = f'{cmd} && echo "custom_sig_term"'
        self.last_send_time = time.time()
        msg_id = self.kernel_client.execute(cmd)
        state = 'busy'
        data = None
        idle_detected = False
        idle_time = None
        timeout = 2
        has_execution_failed = False
        while self.kernel_client.is_alive():
            if idle_detected:
                if time.time() - idle_time > timeout:
                    break
            try:
                msg = self.kernel_client.get_iopub_msg(timeout=2)
                if not 'content' in msg:
                    continue
                content = msg['content']
                if B_DEBUG or b_debug:
                    logger.debug(
                        '/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/'
                        )
                    logger.debug(type(content))
                    logger.debug(content)
                    logger.debug(content.keys())
                    logger.debug(
                        '/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/'
                        )
                if 'traceback' in content:
                    if B_DEBUG or b_debug:
                        logger.debug('TRACEBACK RAISE EXCEPTION NOW')
                        logger.debug(content)
                    ipython_input_pat = re.compile(
                        '<ipython-input-\\d+-[0-9a-f]+>')
                    tb = [re.sub(ipython_input_pat, '<IPY-INPUT>',
                        strip_ansi(line)) for line in content['traceback']]
                    data = KernelException('\n'.join(tb))
                    if websocket is not None:
                        resJson = json.dumps({'res': -1, 'cell_id': cell_id,
                            'service': 'exec', 'errorMsg': '\n'.join(tb)})
                        await self.send_sync(websocket, resJson,
                            is_terminated=True)
                        has_execution_failed = True
                if 'name' in content:
                    if content['name'] == 'stdout':
                        data = content['text']
                        if 'custom_sig_term' in data:
                            logger.debug(
                                'Custom signal term detected. Breaking loop name.'
                                )
                            break
                        output_dict = self.format_output(data)
                        resJson = json.dumps({'res': 1, 'service': 'exec',
                            'output': output_dict, 'cell_id': cell_id})
                        await self.send_sync(websocket, resJson)
                    if content['name'] == 'stderr':
                        data = content['text']
                        if 'custom_sig_term' in data:
                            logger.debug(
                                'Custom signal term detected. Breaking loop name.'
                                )
                            break
                        resJson = json.dumps({'res': -1, 'cell_id': cell_id,
                            'service': 'exec', 'errorMsg': data})
                        await self.send_sync(websocket, resJson,
                            is_terminated=False)
                if 'data' in content:
                    data = content['data']
                    if 'custom_sig_term' in str(data):
                        logger.debug(
                            'Custom signal term detected. Breaking loop data.')
                        break
                    output_dict = self.format_output(data)
                    resJson = json.dumps({'res': 1, 'service': 'exec',
                        'output': output_dict, 'cell_id': cell_id})
                    await self.send_sync(websocket, resJson)
                if 'execution_state' in content:
                    state = content['execution_state']
                    logger.debug(f'STATE STATE STATE {state}')
                    if state == 'idle':
                        idle_detected = True
                        idle_time = time.time()
            except Exception as e:
                logger.debug('Execute exception shell EXECUTION')
                logger.debug(e)
        if not has_execution_failed:
            await self.send_batch(websocket, is_terminated=True)
        return data

    async def list_workspace_variables(self) ->list:
        """
        Get list of variables in the kernel workspace using %whos
        """

        def truncate(data, trunc_size):
            data = data[:trunc_size] + '...' if len(data
                ) > trunc_size else data
            return data
        cmd = '%whos'
        msg_id = self.kernel_client.execute(cmd)
        state = 'busy'
        workspace_variables = []
        while state != 'idle' and self.kernel_client.is_alive():
            try:
                msg = self.kernel_client.get_iopub_msg()
                if not 'content' in msg:
                    continue
                content = msg['content']
                if 'name' in content:
                    if content['name'] == 'stdout':
                        workspace_variables.append(content['text'])
                if 'execution_state' in content:
                    state = content['execution_state']
            except Exception as e:
                logger.debug(e)
                pass
        memory_variables_dict = await self.get_kernel_variables_memory_dict()
        if memory_variables_dict is None:
            memory_variables_dict = dict()
        try:
            workspace_variables = ''.join(workspace_variables).split('\n')
            workspace_variables = workspace_variables[2:-1]
            parsed_variables = []
            for line in workspace_variables:
                parts = re.split('\\s{2,}', line.strip())
                if len(parts) >= 2:
                    name = parts[0]
                    type_ = parts[1]
                    preview = ' '.join(parts[2:]) if len(parts) > 2 else ''
                    parsed_variables.append({'name': name, 'type': type_,
                        'preview': preview, 'size': memory_variables_dict.get(name, 0)})
            workspace_variables = parsed_variables
            for elem_dict in workspace_variables:
                elem_dict['preview_display'] = truncate(elem_dict['preview'
                    ], 30)
                elem_dict['is_df'] = False
                elem_dict['df_columns'] = json.dumps([])
                if elem_dict['type'] == 'DataFrame':
                    try:
                        var_df = convert_to_dataframe(await self._method_get_workspace_variable(elem_dict['name'
                            ]), elem_dict['name'])
                        elem_dict['df_columns'] = json.dumps(list(var_df.columns))
                        elem_dict['is_df'] = True
                    except:
                        pass
        except Exception as e:
            logger.debug('Except list workspace var')
            logger.debug(e)
        return workspace_variables

    async def get_kernel_variables_memory_dict(self) ->dict:
        """
        Returns the kernel size (size of all variables) as dict
        """
        code_get_size = """
import os, sys
def get_size_bytes_variables_dict():
    # Exclude the function itself and common IPython artifacts
    excluded_vars = {"get_size_mb", "_", "__builtins__", "__file__", "__name__", "__doc__"}
    all_vars = {k: v for k, v in globals().items() if k not in excluded_vars and not callable(v) and not k.startswith("__")}
    
    variables_mem_dict = dict()
    for var_name, obj in all_vars.items():
        variables_mem_dict[var_name] = sys.getsizeof(obj)
    
    return variables_mem_dict
size_in_bytes_variables_dict = get_size_bytes_variables_dict()    
"""
        await self.execute(code_get_size, b_debug=False)
        size_in_bytes_variables_dict = (await self._method_get_workspace_variable('size_in_bytes_variables_dict'))
        await self.remove_variable_from_kernel('size_in_bytes_variables_dict')
        return size_in_bytes_variables_dict

    async def get_kernel_memory_size(self) ->float:
        """
        Returns the kernel size (size of all variables)
        """
        code_get_size = """
def get_size_bytes():
    # Exclude the function itself and common IPython artifacts
    excluded_vars = {"get_size_mb", "_", "__builtins__", "__file__", "__name__", "__doc__"}
    all_vars = {k: v for k, v in globals().items() if k not in excluded_vars and not callable(v) and not k.startswith("__")}
    
    size_in_bytes = 0
    for var_name, obj in all_vars.items():
        size_in_bytes += sys.getsizeof(obj)
    
    return size_in_bytes
size_in_bytes = get_size_bytes()    
"""
        await self.execute(code_get_size, b_debug=False)
        size_in_bytes = await self._method_get_workspace_variable(
            'size_in_bytes')
        await self.remove_variable_from_kernel('size_in_bytes')
        return size_in_bytes

    def _method_get_kernel_variable_repr(self, kernel_variable: str) ->dict:
        """
        Get kernel variable (standard kernel output format, str, not raw data)
        """
        cmd = f'{kernel_variable}'
        msg_id = self.kernel_client.execute(cmd)
        state = 'busy'
        resJson = json.dumps({'res': -1, 'is_terminated': True})
        while state != 'idle' and self.kernel_client.is_alive():
            try:
                msg = self.kernel_client.get_iopub_msg()
                if not 'content' in msg:
                    continue
                content = msg['content']
                if 'data' in content:
                    data = content['data']
                    output_dict = self.format_output(data)
                    resJson = json.dumps({'res': 1, 'output': output_dict})
                if 'execution_state' in content:
                    state = content['execution_state']
            except Exception as e:
                logger.debug('Exception get_kernel_variable_repr')
                logger.debug(e)
                pass
        return resJson

    def format_output(self, output) ->dict:
        """
        Format kernel output for view rendering
        """
        if isinstance(output, dict):
            if 'text/html' in output:
                return {'output': output['text/html'], 'type': 'text/html'}
            if 'image/png' in output:
                return {'output': output['image/png'], 'type': 'image/png'}
            if 'text/plain' in output:
                return {'output': output['text/plain'], 'type': 'text/plain'}
        return {'output': output, 'type': 'text/plain'}

    async def _method_get_workspace_variable(self, kernel_variable: str):
        """
        Get variable from the workspace
        """
        workspace_variable = None
        try:
            cmd = f"""import cloudpickle
import base64
tmp_sq_ans = _
base64.b64encode(cloudpickle.dumps({kernel_variable})).decode()"""
            msg_id = self.kernel_client.execute(cmd)
            state = 'busy'
            while state != 'idle' and self.kernel_client.is_alive():
                try:
                    msg = self.kernel_client.get_iopub_msg()
                    if not 'content' in msg:
                        continue
                    content = msg['content']
                    if 'data' in content:
                        data = content['data']
                        output_dict = self.format_output(data)
                        workspace_variable = cloudpickle.loads(base64.b64decode(output_dict['output']))
                    if 'execution_state' in content:
                        state = content['execution_state']
                except Exception as e:
                    logger.debug(e)
                    pass
        except Exception as e:
            logger.debug('Exception _method_get_workspace_variable')
            logger.debug(e)
        await self.execute(f'del tmp_sq_ans')
        await self.execute(f'del cloudpickle')
        await self.execute(f'del base64')
        return workspace_variable

    async def set_workspace_variables(self, variables_dict, websocket=None):
        for key, val in variables_dict.items():
            await self._method_set_workspace_variable(key, val, websocket=
                websocket)

    async def _method_set_workspace_variable(self, name, value, websocket=None
        ):
        """
        Set a variable in the Kernel
        """
        try:
            code = f"""import cloudpickle
import base64
{name} = cloudpickle.loads(base64.b64decode("{base64.b64encode(cloudpickle.dumps(value)).decode()}"))"""
            await self.execute(code, websocket)
        except Exception as e:
            logger.debug('Exception setWorkspaceVariable')
            logger.debug(e)
        await self.execute(f'del cloudpickle')
        await self.execute(f'del base64')

    async def _method_set_workspace_variable_from_paste_modal(self, name, value
        ):
        """
        Set variable from clipboard paste modal (df)
        """
        import pandas as pd
        df_restored = pd.read_json(value, orient='split')
        return await self._method_set_workspace_variable(name, df_restored)

    async def reset_kernel_workspace(self):
        """
        Reset the kernel workspace
        """
        cmd = '%reset -f'
        await self.execute(cmd)

    async def remove_variable_from_kernel(self, kernel_variable: str):
        """
        Remove variable from the kernel
        """
        try:
            code_remove_variable = "del globals()['" + str(kernel_variable
                ) + "']"
            await self.execute(code_remove_variable)
        except:
            pass

    async def cloudpickle_kernel_variables(self):
        """
        Cloudpickle all the variables of the kernel 
        """
        await self.execute('import cloudpickle')
        await self.execute(
            """
import io
import cloudpickle
def test_picklability():
    variables = {k: v for k, v in globals().items() if not k.startswith('_')}
    picklable = {}
    unpicklable = {}
    var_not_to_pickle = ['In', 'Out', 'test_picklability', 'get_ipython']
    var_type_not_to_pickle = ['ZMQExitAutocall']
    
    for var_name, var_value in variables.items():
        var_type = type(var_value)
        if var_name in var_not_to_pickle:
            continue
        if var_type.__name__ in var_type_not_to_pickle:
            continue
        try:
            # Attempt to serialize the variable
            buffer = io.BytesIO()
            cloudpickle.dump(var_value, buffer)
            picklable[var_name] = buffer.getvalue()
        except Exception as e:
            unpicklable[var_name] = {
                "type_name": var_type.__name__,
                "module": var_type.__module__,
                "repr": repr(var_value),
                "error": str(e),
            }
    
    return picklable, unpicklable

kernel_cpkl_picklable, kernel_cpkl_unpicklable = test_picklability()
del test_picklability
"""
            )
        kernel_cpkl_picklable = await self._method_get_workspace_variable(
            'kernel_cpkl_picklable')
        kernel_cpkl_unpicklable = await self._method_get_workspace_variable(
            'kernel_cpkl_unpicklable')
        await self.remove_variable_from_kernel('kernel_cpkl_picklable')
        await self.remove_variable_from_kernel('kernel_cpkl_unpicklable')
        return kernel_cpkl_picklable, kernel_cpkl_unpicklable

    async def execute_code(self, cmd, websocket=None, cell_id=None,
        bTimeout=False):
        """
        Execute a Python code in the Kernel
        """
        if bTimeout:
            return await self.execute_code_timeout(cmd, websocket=websocket,
                cell_id=cell_id)
        else:
            return await self.execute_code_no_timeout(cmd, websocket=
                websocket, cell_id=cell_id)

    @timeout(sparta_1d9b406406())
    async def execute_code_timeout(self, cmd, websocket=None, cell_id=None):
        """
        Execute a Python code in the Kernel (with Timeout)
        """
        return await self.execute(cmd, websocket=websocket, cell_id=cell_id)

    async def execute_code_no_timeout(self, cmd, websocket=None, cell_id=None):
        """
        Execute a Python code in the Kernel (without Timeout)
        """
        return await self.execute(cmd, websocket=websocket, cell_id=cell_id)

    async def getLastExecutedVariable(self, websocket):
        """
        DEPRECATED
        Get ans value
        """
        try:
            code = f"""import cloudpickle
import base64
tmp_sq_ans = _
base64.b64encode(cloudpickle.dumps(tmp_sq_ans)).decode()"""
            return cloudpickle.loads(base64.b64decode(self.format_output(await
                self.execute(code, websocket))))
        except Exception as e:
            logger.debug('Excep last exec val')
            raise e

    async def _method_get_kernel_variable(self, nameVar):
        """
        DEPRECATED
        Return a Python variable from the Kernel
        """
        try:
            code = f"""import cloudpickle
import base64
tmp_sq_ans = _
base64.b64encode(cloudpickle.dumps({nameVar})).decode()"""
            return cloudpickle.loads(base64.b64decode(self.format_output(await
                self.execute(code))))
        except Exception as e:
            logger.debug('Exception get_kernel_variable')
            logger.debug(e)
            return None

    async def removeWorkspaceVariable(self, name):
        """
        Remove a python variable from the Kernel workspace
        """
        try:
            del self.workspaceVarNameArr[name]
        except Exception as e:
            logger.debug('Exception removeWorkspaceVariable')
            logger.debug(e)

    def getWorkspaceVariables(self):
        """
        TO IMPLEMENT
        Returns the list of all available workspace variables
        """
        return []

#END OF QUBE
