import os
import json
import platform
import websocket
import threading
import time
import pandas as pd
from pathlib import Path
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from project.logger_config import logger
from project.sparta_ef90090f65.sparta_40861746d9 import qube_380ad6266d as qube_380ad6266d
from project.sparta_8688631f3d.sparta_c77f2d3c37 import qube_8f0cad92aa as qube_8f0cad92aa
from project.sparta_8688631f3d.sparta_8559d0a6aa.qube_ea38b462b0 import sparta_4d4e6c9f5e
from project.sparta_8688631f3d.sparta_8559d0a6aa.qube_da7a195581 import sparta_0de44fa8d0
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_8f0cad92aa import convert_to_dataframe, convert_dataframe_to_json, sparta_226d9606de
from project.sparta_8688631f3d.sparta_2a93ddec7a.qube_9b8a1e243b import SenderKernel
from project.sparta_8688631f3d.sparta_34d32fb8c6.qube_cbe6ad2077 import sparta_4bb56d08cd, sparta_5fddc0f473, get_api_key_async


class NotebookWS(AsyncWebsocketConsumer):
    """

    """
    channel_session = True
    http_user_and_session = True

    async def connect(self):
        """
        
        """
        logger.debug('Connect Now')
        await self.accept()
        self.user = self.scope['user']
        self.json_data_dict = dict()
        self.sender_kernel_obj = None

    async def disconnect(self, close_code=None):
        """
        Release memory
        """
        logger.debug('Disconnect')
        if self.sender_kernel_obj is not None:
            self.sender_kernel_obj.zmq_close()
        try:
            await self.close()
        except:
            pass

    async def notebook_permission_code_exec(self, json_data):
        """
        For the case of read only notebook in exec mode, we don't allow to execute anything in the kernel but 
        the notebook cell id only
        """
        from project.sparta_8688631f3d.sparta_bbb8926efe import qube_f161d2fcc5 as qube_f161d2fcc5
        return await coreNotebook.notebook_permission_code_exec(json_data)

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

    async def get_kernel_type(self, kernel_manager_uuid) ->int:
        """
        Returns the kernel type
        """
        from project.models import KernelProcess
        kernel_process_list = await sync_to_async(lambda : list(
            KernelProcess.objects.filter(kernel_manager_uuid=
            kernel_manager_uuid)), thread_sensitive=False)()
        if len(kernel_process_list) > 0:
            kernel_process_obj = kernel_process_list[0]
            return kernel_process_obj.type
        return 1

    async def receive(self, text_data):
        if len(text_data) > 0:
            json_data = json.loads(text_data)
            service = json_data['service']
            kernel_manager_uuid = json_data['kernelManagerUUID']
            await self.prepare_sender_kernel(kernel_manager_uuid)
            kernel_type = await self.get_kernel_type(kernel_manager_uuid)

            def dashboard_init_default_gui_vars(code_to_exec, json_data):
                code_init_default_vars = 'import json\n'
                if 'defaultDashboardVars' in json_data:
                    default_dashboard_vars_dict = json_data[
                        'defaultDashboardVars']
                    for var_name, default_dict in default_dashboard_vars_dict.items(
                        ):
                        if len(var_name) > 0:
                            default_value = default_dict['outputDefaultValue']
                            code_init_default_vars += f"""if "{var_name}" in globals():
    pass
else:
    {var_name} = {repr(default_value)}
"""
                default_last_action_state_json = json.dumps({'value': None,
                    'col': -1, 'row': -1})
                code_init_default_vars += f"""if "last_action_state" in globals():
    pass
else:
    last_action_state = json.loads('{default_last_action_state_json}')
"""
                if len(code_init_default_vars) > 0:
                    code_to_exec = f'{code_init_default_vars}\n{code_to_exec}'
                return code_to_exec

            async def import_sys_path_project(json_data):
                """
                This function insert into sys.path the project folder path of the ipynb that is running, in order to use other resource files
                """
                if 'projectSysPath' in json_data:
                    if len(json_data['projectSysPath']) > 0:
                        project_path = sparta_226d9606de(json_data[
                            'projectSysPath'])
                        project_path = Path(project_path).resolve()
                        insert_project_path_cmd = f"""import sys, os
sys.path.insert(0, r"{str(project_path)}")
os.chdir(r"{str(project_path)}")
"""
                        await self.sender_kernel_obj.send_zmq_request({
                            'service': 'execute_code', 'cmd':
                            insert_project_path_cmd})

            async def activate_venv(json_data):
                """
                Activate a specific virtual environment
                """
                if 'dashboardVenv' in json_data:
                    if json_data['dashboardVenv'] is not None:
                        if len(json_data['dashboardVenv']) > 0:
                            venv_name = json_data['dashboardVenv']
                            await self.sender_kernel_obj.send_zmq_request({
                                'service': 'activate_venv', 'venv_name':
                                venv_name})
            if (service == 'init-socket' or service == 'reconnect-kernel' or
                service == 'reconnect-kernel-run-all'):
                res = {'res': 1, 'service': service}
                if 'defaultDashboardVars' in json_data:
                    code_to_exec = dashboard_init_default_gui_vars('',
                        json_data)
                    await self.sender_kernel_obj.send_zmq_request({
                        'service': 'execute_code', 'cmd': code_to_exec})
                await import_sys_path_project(json_data)
                await activate_venv(json_data)
                resJson = json.dumps(res)
                await self.send(text_data=resJson)
                return
            elif service == 'disconnect':
                self.disconnect()
            elif service == 'exec':
                await import_sys_path_project(json_data)
                start_time = time.time()
                logger.debug('=' * 50)
                input_cmd = json_data['cellCode']
                code_to_exec = input_cmd
                if kernel_type == 5:
                    logger.debug('Execute for the notebook Execution Exec case'
                        )
                    logger.debug(json_data)
                    code_to_exec = await self.notebook_permission_code_exec(
                        json_data)
                code_to_exec = dashboard_init_default_gui_vars(code_to_exec,
                    json_data)
                b_exec_as_shell = False
                if input_cmd is not None:
                    if len(input_cmd) > 0:
                        if input_cmd[0] == '!':
                            b_exec_as_shell = True
                if b_exec_as_shell:
                    await self.sender_kernel_obj.send_zmq_request({
                        'service': 'execute_shell', 'cmd': code_to_exec,
                        'json_data': json.dumps(json_data)})
                else:
                    await self.sender_kernel_obj.send_zmq_request({
                        'service': 'execute', 'cmd': code_to_exec,
                        'json_data': json.dumps(json_data)})
                try:
                    updated_plot_variables: list = sparta_4d4e6c9f5e(
                        json_data['cellCode'])
                except:
                    updated_plot_variables = []
                logger.debug('=' * 50)
                elapsed_time = time.time() - start_time
                resJson = json.dumps({'res': 2, 'service': service,
                    'elapsed_time': round(elapsed_time, 2), 'cell_id':
                    json_data['cellId'], 'updated_plot_variables':
                    updated_plot_variables, 'input': json.dumps(json_data)})
                await self.send(text_data=resJson)
            elif service == 'trigger-code-gui-component-input':
                import_sys_path_project(json_data)
                try:
                    try:
                        exec_code_title_list = json.loads(json_data[
                            'execCodeTitle'])
                        cmd_code_title = '\n'.join([elem['code'] for elem in
                            exec_code_title_list])
                    except:
                        cmd_code_title = ''
                    exec_code_input_list = json.loads(json_data[
                        'execCodeInput'])
                    cmd_without_default_gui_vars = '\n'.join([elem['code'] for
                        elem in exec_code_input_list])
                    cmd = dashboard_init_default_gui_vars(
                        cmd_without_default_gui_vars, json_data)
                    cmd += '\n' + cmd_code_title
                    await self.sender_kernel_obj.send_zmq_request(sender_dict
                        ={'service': 'execute_code', 'cmd': cmd},
                        b_send_websocket_msg=False)
                    updated_variables = sparta_4d4e6c9f5e(
                        cmd_without_default_gui_vars)
                    gui_input_varname = json_data['guiInputVarName']
                    gui_output_varname = json_data['guiOutputVarName']
                    gui_title_varname = json_data['cellTitleVarName']
                    raw_data_to_return = [gui_input_varname,
                        gui_output_varname, gui_title_varname]
                    workspace_variables_to_update = []
                    for elem in raw_data_to_return:
                        try:
                            repr_data = (await self.sender_kernel_obj.send_zmq_request({'service':
                                'get_kernel_variable_repr',
                                'kernel_variable': elem}))
                        except:
                            repr_data = json.dumps({'res': 1, 'output': ''})
                        raw_data = convert_dataframe_to_json(
                            convert_to_dataframe(await self.sender_kernel_obj.send_zmq_request({'service':
                            'get_workspace_variable', 'kernel_variable':
                            elem}), gui_input_varname))
                        workspace_variables_to_update.append({'variable':
                            elem, 'raw_data': raw_data, 'repr_data': repr_data}
                            )
                except Exception as e:
                    resJson = json.dumps({'res': -1, 'service': service,
                        'errorMsg': str(e)})
                    logger.debug('Error', resJson)
                    await self.send(text_data=resJson)
                    return
                resJson = json.dumps({'res': 1, 'service': service,
                    'updated_variables': updated_variables,
                    'workspace_variables_to_update':
                    workspace_variables_to_update})
                await self.send(text_data=resJson)
            elif service == 'trigger-code-gui-component-output':
                import_sys_path_project(json_data)
                try:
                    assign_state_variable = ''
                    assign_code = ''
                    if 'assignGuiComponentVariable' in json_data:
                        assign_dict = json_data['assignGuiComponentVariable']
                        assign_gui_var_dict = (
                            sparta_0de44fa8d0(assign_dict))
                        assign_state_variable = assign_gui_var_dict[
                            'assign_state_variable']
                        assign_code = assign_gui_var_dict['assign_code']
                    exec_code_output_list = json.loads(json_data[
                        'execCodeOutput'])
                    code_gui_output = '\n'.join([elem['code'] for elem in
                        exec_code_output_list])
                    cmd = assign_code + '\n'
                    cmd += assign_state_variable + '\n'
                    cmd += code_gui_output
                    await self.sender_kernel_obj.send_zmq_request(sender_dict
                        ={'service': 'execute_code', 'cmd': cmd},
                        b_send_websocket_msg=False)
                    updated_variables = sparta_4d4e6c9f5e(code_gui_output)
                    try:
                        updated_variables.append(json_data[
                            'assignGuiComponentVariable']['variable'])
                    except Exception as e:
                        pass
                except Exception as e:
                    resJson = json.dumps({'res': -1, 'service': service,
                        'errorMsg': str(e)})
                    await self.send(text_data=resJson)
                    return
                resJson = json.dumps({'res': 1, 'service': service,
                    'updated_variables': updated_variables})
                logger.debug(f'return final here {resJson}')
                await self.send(text_data=resJson)
            elif service == 'assign-kernel-variable-from-gui':
                try:
                    assign_dict = json_data['assignGuiComponentVariable']
                    data_assign_value = assign_dict['value']
                    assign_code = (
                        f"{assign_dict['variable']} = {data_assign_value}")
                    await self.sender_kernel_obj.send_zmq_request({
                        'service': 'execute_code', 'cmd': assign_code})
                except Exception as e:
                    resJson = json.dumps({'res': -1, 'service': service,
                        'errorMsg': str(e)})
                    await self.send(text_data=resJson)
                    return
                resJson = json.dumps({'res': 1, 'service': service})
                await self.send(text_data=resJson)
            elif service == 'exec-main-dashboard-notebook-init':
                await import_sys_path_project(json_data)
                await activate_venv(json_data)
                code_to_exec = json_data['dashboardFullCode']
                code_to_exec = dashboard_init_default_gui_vars(code_to_exec,
                    json_data)
                try:
                    await self.sender_kernel_obj.send_zmq_request({
                        'service': 'execute_code', 'cmd': code_to_exec},
                        b_send_websocket_msg=False)
                except Exception as e:
                    resJson = json.dumps({'res': -1, 'service': service,
                        'errorMsg': str(e)})
                    await self.send(text_data=resJson)
                    return
                plot_db_raw_variables_list = json_data['plotDBRawVariablesList'
                    ]
                variables_names = plot_db_raw_variables_list
                variables_raw = []
                variables_repr = []
                for variable in plot_db_raw_variables_list:
                    try:
                        variables_raw.append(convert_dataframe_to_json(
                            convert_to_dataframe(await self.sender_kernel_obj.send_zmq_request({'service':
                            'get_workspace_variable', 'kernel_variable':
                            variable}), variable)))
                        variables_repr.append(await self.sender_kernel_obj.send_zmq_request({'service':
                            'get_kernel_variable_repr', 'kernel_variable':
                            variable}))
                    except Exception as e:
                        logger.debug('Except get var')
                        logger.debug(e)
                resJson = json.dumps({'res': 1, 'service': service,
                    'variables_names': variables_names, 'variables_raw':
                    variables_raw, 'variables_repr': variables_repr})
                await self.send(text_data=resJson)
            elif service == 'trigger-action-plot-db':
                logger.debug('TRIGGER CODE ACTION PLOTDB')
                logger.debug(json_data)
                try:
                    cmd_to_exec = 'import json\n'
                    cmd_to_exec += (
                        f"last_action_state = json.loads('{json_data['actionDict']}')\n"
                        )
                    try:
                        trigger_code_list = json.loads(json_data['triggerCode']
                            )
                        trigger_code_cmd = '\n'.join([elem['code'] for elem in
                            trigger_code_list])
                    except:
                        trigger_code_cmd = ''
                    cmd_to_exec += '\n' + trigger_code_cmd
                    logger.debug('cmd to execute')
                    logger.debug('cmd_to_exec')
                    logger.debug(cmd_to_exec)
                    await self.sender_kernel_obj.send_zmq_request({
                        'service': 'execute_code', 'cmd': cmd_to_exec})
                    updated_variables = sparta_4d4e6c9f5e(trigger_code_cmd)
                except Exception as e:
                    resJson = json.dumps({'res': -1, 'service': service,
                        'errorMsg': str(e)})
                    await self.send(text_data=resJson)
                    return
                resJson = json.dumps({'res': 1, 'service': service,
                    'updated_variables': updated_variables})
                await self.send(text_data=resJson)
            elif service == 'dynamic-title':
                try:
                    exec_code_title_list = json.loads(json_data[
                        'execCodeTitle'])
                    cmd_code_title = '\n'.join([elem['code'] for elem in
                        exec_code_title_list])
                except:
                    cmd_code_title = ''
                if len(cmd_code_title) > 0:
                    cmd_code_title = dashboard_init_default_gui_vars(
                        cmd_code_title, json_data)
                    await import_sys_path_project(json_data)
                    await activate_venv(json_data)
                    try:
                        await self.sender_kernel_obj.send_zmq_request({
                            'service': 'execute_code', 'cmd': cmd_code_title})
                        title_varname = json_data['cellTitleVarName']
                        raw_data_to_return = [title_varname]
                        workspace_variables_to_update = []
                        for elem in raw_data_to_return:
                            try:
                                repr_data = (await self.sender_kernel_obj.send_zmq_request({'service':
                                    'get_kernel_variable_repr',
                                    'kernel_variable': elem}))
                            except:
                                repr_data = json.dumps({'res': 1, 'output': ''}
                                    )
                            raw_data = convert_dataframe_to_json(
                                convert_to_dataframe(await self.sender_kernel_obj.send_zmq_request({
                                'service': 'get_workspace_variable',
                                'kernel_variable': elem}), title_varname))
                            workspace_variables_to_update.append({
                                'variable': elem, 'raw_data': raw_data,
                                'repr_data': repr_data})
                        resJson = json.dumps({'res': 1, 'service': service,
                            'workspace_variables_to_update':
                            workspace_variables_to_update})
                        await self.send(text_data=resJson)
                    except Exception as e:
                        resJson = json.dumps({'res': -1, 'service': service,
                            'errorMsg': str(e)})
                        logger.debug('Error', resJson)
                        logger.debug(cmd_code_title)
                        await self.send(text_data=resJson)
                        return
            elif service == 'dashboard-map-dataframe-python':
                notebook_var = json_data['notebookVar']
                json_dataframe = json_data['jsonDataFrame']
                cmd_code_title = (
                    f"jsonDataFrameDictTmp = json.loads('{json_dataframe}')\n")
                cmd_code_title += (
                    f"{notebook_var} = pd.DataFrame(index=jsonDataFrameDictTmp['index'], columns=jsonDataFrameDictTmp['columns'], data=jsonDataFrameDictTmp['data'])"
                    )
                await self.sender_kernel_obj.send_zmq_request({'service':
                    'execute_code', 'cmd': cmd_code_title})
                resJson = json.dumps({'res': 1, 'service': service})
                await self.send(text_data=resJson)
            elif service == 'reset':
                await self.sender_kernel_obj.send_zmq_request({'service':
                    'reset_kernel_workspace'})
                await activate_venv(json_data)
                res = {'res': 1, 'service': service}
                resJson = json.dumps(res)
                await self.send(text_data=resJson)
            elif service == 'workspace-list':
                workspace_variables = (await self.sender_kernel_obj.send_zmq_request({'service': 'list_workspace_variables'}))
                res = {'res': 1, 'service': service, 'workspace_variables':
                    workspace_variables}
                res.update(json_data)
                resJson = json.dumps(res)
                await self.send(text_data=resJson)
            elif service == 'workspace-get-variable-as-df':
                kernel_variables_arr = []
                kernel_variable_arr_name = []
                kernel_variable_repr_arr = []
                for kernel_variable in json_data['kernel_variable_arr']:
                    workspace_variable = (await self.sender_kernel_obj.send_zmq_request({'service':
                        'get_workspace_variable', 'kernel_variable':
                        kernel_variable}))
                    workspace_variable_df = convert_to_dataframe(
                        workspace_variable, variable_name=kernel_variable)
                    try:
                        kernel_variables_arr.append(convert_dataframe_to_json
                            (workspace_variable_df))
                        kernel_variable_arr_name.append(kernel_variable)
                    except:
                        pass
                    try:
                        repr_data = (await self.sender_kernel_obj.send_zmq_request({'service':
                            'get_kernel_variable_repr', 'kernel_variable':
                            kernel_variable}))
                    except:
                        repr_data = json.dumps({'res': 1, 'output': ''})
                    kernel_variable_repr_arr.append(repr_data)
                res = {'res': 1, 'service': service, 'kernel_variable_arr':
                    kernel_variable_arr_name, 'workspace_variable_arr':
                    kernel_variables_arr, 'kernel_variable_repr_arr':
                    kernel_variable_repr_arr}
                resJson = json.dumps(res)
                await self.send(text_data=resJson)
            elif service == 'workspace-get-variable' or service == 'workspace-get-variable-preview':
                workspace_variable_repr = (await self.sender_kernel_obj.send_zmq_request({'service': 'get_kernel_variable_repr',
                    'kernel_variable': json_data['kernel_variable']}))
                res = {'res': 1, 'service': service, 'cell_id': json_data.get('cellId', None), 'workspace_variable':
                    workspace_variable_repr}
                resJson = json.dumps(res)
                await self.send(text_data=resJson)
            elif service == 'workspace-set-variable-from-datasource':
                if 'value' in list(json_data.keys()):
                    await self.sender_kernel_obj.send_zmq_request({
                        'service': 'set_workspace_variable_from_datasource',
                        'json_data': json.dumps(json_data)})
                    res = {'res': 1, 'service': service}
                    resJson = json.dumps(res)
                    await self.send(text_data=resJson)
            elif service == 'workspace-set-variable':
                if 'value' in list(json_data.keys()):
                    await self.sender_kernel_obj.send_zmq_request({
                        'service': 'set_workspace_variable', 'json_data':
                        json.dumps(json_data)})
                    res = {'res': 1, 'service': service}
                    resJson = json.dumps(res)
                    await self.send(text_data=resJson)
            elif service == 'workspace-set-variable-from-paste-modal':
                df = pd.DataFrame(json_data['clipboardData'])
                delimiters = json_data['delimiters']
                if delimiters is not None:
                    if len(delimiters) > 0:
                        cols = df.columns
                        df = df[cols[0]].str.split(delimiters, expand=True)
                if json_data['bFirstRowHeader']:
                    df.columns = df.iloc[0]
                    df = df[1:].reset_index(drop=True)
                if json_data['bFirstColIndex']:
                    df = df.set_index(df.columns[0])
                post_data = {'name': json_data['name'], 'df_json': df.to_json(orient='split')}
                await self.sender_kernel_obj.send_zmq_request({'service':
                    'set_workspace_variable_from_paste_modal', 'json_data':
                    json.dumps(post_data)})
                res = {'res': 1, 'service': service}
                resJson = json.dumps(res)
                await self.send(text_data=resJson)
            elif service == 'set-sys-path-import':
                if 'projectPath' in json_data:
                    await import_sys_path_project(json_data)
                res = {'res': 1, 'service': service}
                resJson = json.dumps(res)
                await self.send(text_data=resJson)
            elif service == 'set-kernel-venv':
                if 'dashboardVenv' in json_data:
                    if json_data['dashboardVenv'] is not None:
                        if len(json_data['dashboardVenv']) > 0:
                            venv_name = json_data['dashboardVenv']
                            await self.sender_kernel_obj.send_zmq_request({
                                'service': 'activate_venv', 'venv_name':
                                venv_name})
                res = {'res': 1, 'service': service}
                resJson = json.dumps(res)
                await self.send(text_data=resJson)
            elif service == 'deactivate-venv':
                await self.sender_kernel_obj.send_zmq_request({'service':
                    'deactivate_venv'})
                res = {'res': 1, 'service': service}
                resJson = json.dumps(res)
                await self.send(text_data=resJson)
            elif service == 'get-widget-iframe':
                logger.debug('Deal with iframe here')
                from IPython.core.display import display, HTML
                import warnings
                warnings.filterwarnings('ignore', message=
                    'Consider using IPython.display.IFrame instead',
                    category=UserWarning)
                try:
                    widget_id = json_data['widget_id']
                    api_token_id = await get_api_key_async(self.user)
                    widget_iframe = await sync_to_async(lambda : HTML(
                        f'<iframe src="/plot-widget/{widget_id}/{api_token_id}" width="100%" height="500" frameborder="0" allow="clipboard-write"></iframe>'
                        ).data)()
                    res = {'res': 1, 'service': service, 'widget_iframe':
                        widget_iframe}
                    resJson = json.dumps(res)
                    await self.send(text_data=resJson)
                except Exception as e:
                    res = {'res': -1, 'errorMsg': str(e)}
                    resJson = json.dumps(res)
                    await self.send(text_data=resJson)

#END OF QUBE
