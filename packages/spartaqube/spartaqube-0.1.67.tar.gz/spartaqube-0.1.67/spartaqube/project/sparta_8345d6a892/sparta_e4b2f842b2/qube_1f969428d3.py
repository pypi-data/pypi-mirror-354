import os
import sys
import subprocess
import shutil
import getpass
import platform
import json
import base64
import zipfile
import io
import uuid
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime, timedelta
from pathlib import Path
import pytz
UTC = pytz.utc
from project.models_spartaqube import Dashboard, DashboardShared, Developer, DeveloperShared, Notebook, NotebookShared, Kernel, KernelShared
from project.models import ShareRights
from project.sparta_8345d6a892.sparta_87f32c6e97 import qube_93b4ab09a2 as qube_93b4ab09a2
from project.sparta_8345d6a892.sparta_db87358646 import qube_af0123880b as qube_af0123880b
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import sparta_ad557db230, sparta_91bd932e94
from project.sparta_8345d6a892.sparta_952c41e91e.qube_ef9e4f9eb1 import sparta_9c89cfd808
from project.sparta_8345d6a892.sparta_490625ab5b import qube_0c12c56358 as qube_0c12c56358
from project.logger_config import logger


def sparta_bcefba0d6f(user_obj) ->list:
    """
    
    """
    user_group_set = qube_93b4ab09a2.sparta_b0ee4cd292(user_obj)
    if len(user_group_set) > 0:
        user_groups = [this_obj.user_group for this_obj in user_group_set]
    else:
        user_groups = []
    return user_groups


def sparta_a4d67b84b5():
    """
    This function returns the folder path for the venv
    """
    spartaqube_volume_path = sparta_9c89cfd808()
    default_project_path = os.path.join(spartaqube_volume_path, 'sq_venv')
    os.makedirs(default_project_path, exist_ok=True)
    return default_project_path


def sparta_115ffaed22(env_name):
    """Gets the path to the pip executable in a platform-independent way."""
    env_path = sparta_a4d67b84b5()
    if sys.platform == 'win32':
        pip_path = os.path.join(env_path, env_name, 'Scripts', 'pip.exe')
    else:
        pip_path = os.path.join(env_path, env_name, 'bin', 'pip')
    return pip_path


def sparta_5b9eccc11a(json_data, user_obj) ->dict:
    """
    This function returns the list of available venv 
    """
    base_path = sparta_a4d67b84b5()
    available_venvs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    return {'res': 1, 'available_venvs': available_venvs}


def sparta_bdff51a6c0(json_data, user_obj) ->dict:
    """
    This function creates a venv 
    """
    base_path = sparta_a4d67b84b5()
    env_name = json_data['env_name']
    env_path = os.path.join(base_path, env_name)
    try:
        subprocess.run([sys.executable, '-m', 'venv', env_path], check=True)
        MANDATORY_LIB_TO_INSTALL = ['cloudpickle']
        for lib in MANDATORY_LIB_TO_INSTALL:
            pip_path = sparta_115ffaed22(env_name)
            pip_cmd_input = f'pip install {lib}'
            pip_cmd = pip_cmd_input.replace('pip', pip_path)
            process = subprocess.Popen(pip_cmd, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True)
            for line in process.stdout:
                logger.debug(line)
        return {'res': 1}
    except Exception as e:
        return {'res': -1, 'errorMsg':
            f'Failed to create virtual environment with error {str(e)}'}


def sparta_eba6095864(json_data, user_obj) ->dict:
    """
    This function set a venv 
    """
    dashboard_id = json_data['dashboardId']
    dashboard_set = Dashboard.objects.filter(dashboard_id__startswith=
        dashboard_id, is_delete=False).all()
    if dashboard_set.count() == 1:
        dashboard_obj = dashboard_set[dashboard_set.count() - 1]
        dashboard_id = dashboard_obj.dashboard_id
        user_groups = sparta_bcefba0d6f(user_obj)
        if len(user_groups) > 0:
            dashboard_shared_set = DashboardShared.objects.filter(Q(
                is_delete=0, user_group__in=user_groups,
                dashboard__is_delete=0, dashboard=dashboard_obj) | Q(
                is_delete=0, user=user_obj, dashboard__is_delete=0,
                dashboard=dashboard_obj))
        else:
            dashboard_shared_set = DashboardShared.objects.filter(is_delete
                =0, user=user_obj, dashboard__is_delete=0, dashboard=
                dashboard_obj)
        has_edit_rights = False
        if dashboard_shared_set.count() > 0:
            dashboard_shared_obj = dashboard_shared_set[0]
            share_rights_obj = dashboard_shared_obj.share_rights
            if share_rights_obj.is_admin or share_rights_obj.has_write_rights:
                has_edit_rights = True
        if has_edit_rights:
            env_name = json_data['env_name']
            dashboard_obj.dashboard_venv = env_name
            dashboard_obj.save()
    res_kernel_activate_venv = qube_0c12c56358.sparta_b21ccc50f9(
        json_data, user_obj)
    return {'res': 1}


def sparta_00f869edca(json_data, user_obj) ->dict:
    """
    This function remove a virtual env from a dashboard project
    """
    dashboard_id = json_data['dashboardId']
    dashboard_set = Dashboard.objects.filter(dashboard_id__startswith=
        dashboard_id, is_delete=False).all()
    if dashboard_set.count() == 1:
        dashboard_obj = dashboard_set[dashboard_set.count() - 1]
        dashboard_id = dashboard_obj.dashboard_id
        user_groups = sparta_bcefba0d6f(user_obj)
        if len(user_groups) > 0:
            dashboard_shared_set = DashboardShared.objects.filter(Q(
                is_delete=0, user_group__in=user_groups,
                dashboard__is_delete=0, dashboard=dashboard_obj) | Q(
                is_delete=0, user=user_obj, dashboard__is_delete=0,
                dashboard=dashboard_obj))
        else:
            dashboard_shared_set = DashboardShared.objects.filter(is_delete
                =0, user=user_obj, dashboard__is_delete=0, dashboard=
                dashboard_obj)
        has_edit_rights = False
        if dashboard_shared_set.count() > 0:
            dashboard_shared_obj = dashboard_shared_set[0]
            share_rights_obj = dashboard_shared_obj.share_rights
            if share_rights_obj.is_admin or share_rights_obj.has_write_rights:
                has_edit_rights = True
        if has_edit_rights:
            env_name = None
            dashboard_obj.dashboard_venv = env_name
            dashboard_obj.save()
    return {'res': 1}


def sparta_05a22862ae(json_data, user_obj) ->dict:
    """
    This function deletes a venv 
    """
    dashboard_id = json_data['dashboardId']
    developer_id = json_data['developerId']
    if str(dashboard_id) != '-1':
        sparta_00f869edca(json_data, user_obj)
    if str(developer_id) != '-1':
        sparta_f39df83d4a(json_data, user_obj)
    base_path = sparta_a4d67b84b5()
    env_name = json_data['env_name']
    env_path = os.path.join(base_path, env_name)
    try:
        shutil.rmtree(env_path)
        return {'res': 1}
    except FileNotFoundError as e:
        return {'res': -1, 'errorMsg': str(e)}
    except Exception as e:
        return {'res': -1, 'errorMsg': str(e)}


def sparta_5207f54fc3(json_data, user_obj) ->dict:
    """
    Get the output of pip list for a specific virtual environment
    """
    env_name = json_data['env_name']
    pip_path = sparta_115ffaed22(env_name)
    libraries = []
    try:
        result = subprocess.run([pip_path, 'list'], capture_output=True,
            text=True, check=True)
        lines = result.stdout.strip().splitlines()[2:]
        for line in lines:
            package, version = line.split()[:2]
            libraries.append({'name': package, 'version': version})
        return {'res': 1, 'libraries': libraries}
    except Exception as e:
        return {'res': -1, 'errorMsg': str(e)}


def sparta_942f7a24e3(env_name, project_path) ->dict:
    """
    Get the output of pip list for a specific virtual environment
    """
    requirements_file_path = os.path.join(project_path, 'requirements.txt')
    pip_path = sparta_115ffaed22(env_name)
    try:
        with open(requirements_file_path, 'w') as requirements_file:
            subprocess.run([pip_path, 'freeze'], stdout=requirements_file)
        return {'res': 1}
    except Exception as e:
        return {'res': -1, 'errorMsg': str(e)}


def sparta_aaaee63040(json_data, user_obj) ->dict:
    """
    Set venv for developer mode
    """
    logger.debug('SET VENV DEVELOPER DEBUG > set_venv_developer')
    logger.debug(json_data)
    developer_id = json_data['developerId']
    developer_set = Developer.objects.filter(developer_id__startswith=
        developer_id, is_delete=False).all()
    if developer_set.count() == 1:
        developer_obj = developer_set[developer_set.count() - 1]
        developer_id = developer_obj.developer_id
        user_groups = sparta_bcefba0d6f(user_obj)
        if len(user_groups) > 0:
            developer_shared_set = DeveloperShared.objects.filter(Q(
                is_delete=0, user_group__in=user_groups,
                developer__is_delete=0, developer=developer_obj) | Q(
                is_delete=0, user=user_obj, developer__is_delete=0,
                developer=developer_obj))
        else:
            developer_shared_set = DeveloperShared.objects.filter(is_delete
                =0, user=user_obj, developer__is_delete=0, developer=
                developer_obj)
        has_edit_rights = False
        if developer_shared_set.count() > 0:
            developer_shared_obj = developer_shared_set[0]
            share_rights_obj = developer_shared_obj.share_rights
            if share_rights_obj.is_admin or share_rights_obj.has_write_rights:
                has_edit_rights = True
        if has_edit_rights:
            env_name = json_data['env_name']
            developer_obj.developer_venv = env_name
            developer_obj.save()
    res_kernel_activate_venv = qube_0c12c56358.sparta_b21ccc50f9(
        json_data, user_obj)
    return {'res': 1}


def sparta_f39df83d4a(json_data, user_obj) ->dict:
    """
    This function remove a virtual env from a developer project
    """
    developer_id = json_data['developerId']
    developer_set = Developer.objects.filter(developer_id__startswith=
        developer_id, is_delete=False).all()
    if developer_set.count() == 1:
        developer_obj = developer_set[developer_set.count() - 1]
        developer_id = developer_obj.developer_id
        user_groups = sparta_bcefba0d6f(user_obj)
        if len(user_groups) > 0:
            developer_shared_set = DeveloperShared.objects.filter(Q(
                is_delete=0, user_group__in=user_groups,
                developer__is_delete=0, developer=developer_obj) | Q(
                is_delete=0, user=user_obj, developer__is_delete=0,
                developer=developer_obj))
        else:
            developer_shared_set = DeveloperShared.objects.filter(is_delete
                =0, user=user_obj, developer__is_delete=0, developer=
                developer_obj)
        has_edit_rights = False
        if developer_shared_set.count() > 0:
            developer_shared_obj = developer_shared_set[0]
            share_rights_obj = developer_shared_obj.share_rights
            if share_rights_obj.is_admin or share_rights_obj.has_write_rights:
                has_edit_rights = True
        if has_edit_rights:
            env_name = None
            developer_obj.developer_venv = env_name
            developer_obj.save()
    return {'res': 1}


def sparta_1a2cdc9101(json_data, user_obj) ->dict:
    """
    Set venv for notebook
    """
    logger.debug('SET VENV DEVELOPER DEBUG > set_venv_developer')
    logger.debug(json_data)
    notebook_id = json_data['notebookId']
    notebook_set = Notebook.objects.filter(notebook_id__startswith=
        notebook_id, is_delete=False).all()
    if notebook_set.count() == 1:
        notebook_obj = notebook_set[notebook_set.count() - 1]
        notebook_id = notebook_obj.notebook_id
        user_groups = sparta_bcefba0d6f(user_obj)
        if len(user_groups) > 0:
            notebook_shared_set = NotebookShared.objects.filter(Q(is_delete
                =0, user_group__in=user_groups, notebook__is_delete=0,
                notebook=notebook_obj) | Q(is_delete=0, user=user_obj,
                notebook__is_delete=0, notebook=notebook_obj))
        else:
            notebook_shared_set = NotebookShared.objects.filter(is_delete=0,
                user=user_obj, notebook__is_delete=0, notebook=notebook_obj)
        has_edit_rights = False
        if notebook_shared_set.count() > 0:
            notebook_shared_obj = notebook_shared_set[0]
            share_rights_obj = notebook_shared_obj.share_rights
            if share_rights_obj.is_admin or share_rights_obj.has_write_rights:
                has_edit_rights = True
        if has_edit_rights:
            env_name = json_data['env_name']
            notebook_obj.notebook_venv = env_name
            notebook_obj.save()
    res_kernel_activate_venv = qube_0c12c56358.sparta_b21ccc50f9(
        json_data, user_obj)
    return {'res': 1}


def sparta_c8a25eb11d(json_data, user_obj) ->dict:
    """
    This function remove a virtual env from a notebook project
    """
    notebook_id = json_data['notebookId']
    notebook_set = Notebook.objects.filter(notebook_id__startswith=
        notebook_id, is_delete=False).all()
    if notebook_set.count() == 1:
        notebook_obj = notebook_set[notebook_set.count() - 1]
        notebook_id = notebook_obj.notebook_id
        user_groups = sparta_bcefba0d6f(user_obj)
        if len(user_groups) > 0:
            notebook_shared_set = NotebookShared.objects.filter(Q(is_delete
                =0, user_group__in=user_groups, notebook__is_delete=0,
                notebook=notebook_obj) | Q(is_delete=0, user=user_obj,
                notebook__is_delete=0, notebook=notebook_obj))
        else:
            notebook_shared_set = NotebookShared.objects.filter(is_delete=0,
                user=user_obj, notebook__is_delete=0, notebook=notebook_obj)
        has_edit_rights = False
        if notebook_shared_set.count() > 0:
            notebook_shared_obj = notebook_shared_set[0]
            share_rights_obj = notebook_shared_obj.share_rights
            if share_rights_obj.is_admin or share_rights_obj.has_write_rights:
                has_edit_rights = True
        if has_edit_rights:
            env_name = None
            notebook_obj.notebook_venv = env_name
            notebook_obj.save()
    return {'res': 1}


def sparta_72eae12b98(json_data, user_obj) ->dict:
    """
    Set kernel venv
    """
    from project.sparta_8345d6a892.sparta_490625ab5b import qube_0c12c56358 as qube_0c12c56358
    kernel_manager_uuid = json_data['kernelManagerUUID']
    kernel_set = Kernel.objects.filter(kernel_manager_uuid__startswith=
        kernel_manager_uuid, is_delete=False).all()
    if kernel_set.count() == 1:
        kernel_obj = kernel_set[kernel_set.count() - 1]
        kernel_manager_uuid = kernel_obj.kernel_manager_uuid
        user_groups = sparta_bcefba0d6f(user_obj)
        if len(user_groups) > 0:
            kernel_shared_set = KernelShared.objects.filter(Q(is_delete=0,
                user_group__in=user_groups, kernel__is_delete=0, kernel=
                kernel_obj) | Q(is_delete=0, user=user_obj,
                kernel__is_delete=0, kernel=kernel_obj))
        else:
            kernel_shared_set = KernelShared.objects.filter(is_delete=0,
                user=user_obj, kernel__is_delete=0, kernel=kernel_obj)
        has_edit_rights = False
        if kernel_shared_set.count() > 0:
            kernel_shared_obj = kernel_shared_set[0]
            share_rights_obj = kernel_shared_obj.share_rights
            if share_rights_obj.is_admin or share_rights_obj.has_write_rights:
                has_edit_rights = True
        if has_edit_rights:
            env_name = json_data['env_name']
            kernel_obj.kernel_venv = env_name
            kernel_obj.save()
    res_kernel_activate_venv = qube_0c12c56358.sparta_b21ccc50f9(
        json_data, user_obj)
    return {'res': 1}


def sparta_1c923c6ad7(json_data, user_obj) ->dict:
    """
    Deactivate venv inside kernel
    """
    kernel_manager_uuid = json_data['kernelManagerUUID']
    kernel_set = Kernel.objects.filter(kernel_manager_uuid__startswith=
        kernel_manager_uuid, is_delete=False).all()
    if kernel_set.count() == 1:
        kernel_obj = kernel_set[kernel_set.count() - 1]
        kernel_manager_uuid = kernel_obj.kernel_manager_uuid
        user_groups = sparta_bcefba0d6f(user_obj)
        if len(user_groups) > 0:
            kernel_shared_set = KernelShared.objects.filter(Q(is_delete=0,
                user_group__in=user_groups, kernel__is_delete=0, kernel=
                kernel_obj) | Q(is_delete=0, user=user_obj,
                kernel__is_delete=0, kernel=kernel_obj))
        else:
            kernel_shared_set = KernelShared.objects.filter(is_delete=0,
                user=user_obj, kernel__is_delete=0, kernel=kernel_obj)
        has_edit_rights = False
        if kernel_shared_set.count() > 0:
            kernel_shared_obj = kernel_shared_set[0]
            share_rights_obj = kernel_shared_obj.share_rights
            if share_rights_obj.is_admin or share_rights_obj.has_write_rights:
                has_edit_rights = True
        if has_edit_rights:
            env_name = None
            kernel_obj.kernel_venv = env_name
            kernel_obj.save()
    return {'res': 1}


def sparta_02a5fbaa3e(json_data, user_obj) ->dict:
    """
    Export venv libraries to requirements.txt
    """
    logger.debug('json_data')
    logger.debug(json_data)
    dashboard_id = json_data['dashboardId']
    developer_id = json_data['developerId']
    notebook_id = json_data['notebookId']
    kernelManagerUUID = json_data['kernelManagerUUID']
    if str(dashboard_id) != '-1':
        return sparta_2b2713a125(json_data, user_obj)
    if str(developer_id) != '-1':
        return sparta_27998e5f6b(json_data, user_obj)
    if str(notebook_id) != '-1':
        return sparta_7d0c3618ec(json_data, user_obj)
    if str(kernelManagerUUID) != '-1':
        return sparta_efec6a8b14(json_data, user_obj)
    env_name = json_data['env_name']
    project_path = json_data['projectPath']
    if json_data['is_spartaqube_developer_mode']:
        project_path = os.path.join(project_path, 'backend')
    return sparta_942f7a24e3(env_name, project_path)


def sparta_2b2713a125(json_data, user_obj) ->dict:
    """
    Export venv libraries to requirements.txt (dashboard mode)
    """
    dashboard_id = json_data['dashboardId']
    env_name = json_data['env_name']
    project_path = json_data['projectPath']
    dashboard_set = Dashboard.objects.filter(dashboard_id__startswith=
        dashboard_id, is_delete=False).all()
    if dashboard_set.count() == 1:
        dashboard_obj = dashboard_set[dashboard_set.count() - 1]
        dashboard_id = dashboard_obj.dashboard_id
        user_groups = sparta_bcefba0d6f(user_obj)
        if len(user_groups) > 0:
            dashboard_shared_set = DashboardShared.objects.filter(Q(
                is_delete=0, user_group__in=user_groups,
                dashboard__is_delete=0, dashboard=dashboard_obj) | Q(
                is_delete=0, user=user_obj, dashboard__is_delete=0,
                dashboard=dashboard_obj))
        else:
            dashboard_shared_set = DashboardShared.objects.filter(is_delete
                =0, user=user_obj, dashboard__is_delete=0, dashboard=
                dashboard_obj)
        has_edit_rights = False
        if dashboard_shared_set.count() > 0:
            dashboard_shared_obj = dashboard_shared_set[0]
            share_rights_obj = dashboard_shared_obj.share_rights
            if share_rights_obj.is_admin or share_rights_obj.has_write_rights:
                has_edit_rights = True
        if has_edit_rights:
            return sparta_942f7a24e3(env_name, project_path)
    return {'res': 1}


def sparta_27998e5f6b(json_data, user_obj) ->dict:
    """
    Export venv libraries to requirements.txt (developer mode)
    """
    developer_id = json_data['developerId']
    env_name = json_data['env_name']
    project_path = json_data['projectPath']
    project_path = os.path.join(project_path, 'backend')
    developer_set = Developer.objects.filter(developer_id__startswith=
        developer_id, is_delete=False).all()
    if developer_set.count() == 1:
        developer_obj = developer_set[developer_set.count() - 1]
        developer_id = developer_obj.developer_id
        user_groups = sparta_bcefba0d6f(user_obj)
        if len(user_groups) > 0:
            developer_shared_set = DeveloperShared.objects.filter(Q(
                is_delete=0, user_group__in=user_groups,
                developer__is_delete=0, developer=developer_obj) | Q(
                is_delete=0, user=user_obj, developer__is_delete=0,
                developer=developer_obj))
        else:
            developer_shared_set = DeveloperShared.objects.filter(is_delete
                =0, user=user_obj, developer__is_delete=0, developer=
                developer_obj)
        has_edit_rights = False
        if developer_shared_set.count() > 0:
            developer_shared_obj = developer_shared_set[0]
            share_rights_obj = developer_shared_obj.share_rights
            if share_rights_obj.is_admin or share_rights_obj.has_write_rights:
                has_edit_rights = True
        if has_edit_rights:
            return sparta_942f7a24e3(env_name, project_path)
    return {'res': 1}


def sparta_7d0c3618ec(json_data, user_obj) ->dict:
    """
    Export venv libraries to requirements.txt (notebook mode)
    """
    notebook_id = json_data['notebookId']
    env_name = json_data['env_name']
    project_path = json_data['projectPath']
    notebook_set = Notebook.objects.filter(notebook_id__startswith=
        notebook_id, is_delete=False).all()
    if notebook_set.count() == 1:
        notebook_obj = notebook_set[notebook_set.count() - 1]
        notebook_id = notebook_obj.developer_id
        user_groups = sparta_bcefba0d6f(user_obj)
        if len(user_groups) > 0:
            notebook_shared_set = NotebookShared.objects.filter(Q(is_delete
                =0, user_group__in=user_groups, notebook__is_delete=0,
                notebook=notebook_obj) | Q(is_delete=0, user=user_obj,
                notebook__is_delete=0, notebook=notebook_obj))
        else:
            notebook_shared_set = NotebookShared.objects.filter(is_delete=0,
                user=user_obj, notebook__is_delete=0, notebook=notebook_obj)
        has_edit_rights = False
        if notebook_shared_set.count() > 0:
            notebook_shared_obj = notebook_shared_set[0]
            share_rights_obj = notebook_shared_obj.share_rights
            if share_rights_obj.is_admin or share_rights_obj.has_write_rights:
                has_edit_rights = True
        if has_edit_rights:
            return sparta_942f7a24e3(env_name, project_path)
    return {'res': 1}


def sparta_efec6a8b14(json_data, user_obj) ->dict:
    """
    Export venv libraries to requirements.txt (kernel notebook mode)
    """
    from project.sparta_8345d6a892.sparta_490625ab5b import qube_0c12c56358 as qube_0c12c56358
    kernel_manager_uuid = json_data['kernelManagerUUID']
    env_name = json_data['env_name']
    project_path = json_data['projectPath']
    kernel_process_obj = qube_0c12c56358.sparta_a5c947582d(user_obj,
        kernel_manager_uuid)
    if kernel_process_obj is None:
        return sparta_942f7a24e3(env_name, project_path)
    return {'res': 1}


def sparta_f768203fcc(json_data, user_obj) ->dict:
    """
    Open terminal with venv activated
    """
    logger.debug('json_data')
    logger.debug(json_data)
    env_name = json_data['env_name']
    venv_path = os.path.join(sparta_a4d67b84b5(), env_name)
    logger.debug('venv_path')
    logger.debug(venv_path)
    path = sparta_ad557db230(json_data['projectPath'])
    if json_data['is_spartaqube_developer_mode']:
        path = os.path.join(path, 'backend')
    if not os.path.isdir(path):
        return {'res': -1, 'errorMsg':
            f"The provided path '{path}' is not a valid directory."}
    system = platform.system()
    try:
        if system == 'Windows':
            os.system(
                f'start cmd /K "cd /d {path} && {venv_path}\\Scripts\\activate.bat"'
                )
        elif system == 'Linux':
            subprocess.run(['x-terminal-emulator', '-e',
                f'bash -c "cd {path} && source {venv_path}/bin/activate && exec bash"'
                ], check=True)
        elif system == 'Darwin':
            script = f"""
            tell application "Terminal"
                do script "cd {path} && source {venv_path}/bin/activate"
                activate
            end tell
            """
            subprocess.run(['osascript', '-e', script], check=True)
        else:
            return {'res': -1, 'errorMsg': 'Unsupported operating system.'}
    except Exception as e:
        return {'res': -1, 'errorMsg':
            f"Failed to open terminal and activate venv at '{path}': {e}"}
    return {'res': 1}

#END OF QUBE
