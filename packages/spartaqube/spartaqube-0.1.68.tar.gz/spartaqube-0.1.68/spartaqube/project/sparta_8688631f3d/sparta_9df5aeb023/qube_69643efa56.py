import os
import json
import base64
import shutil
import zipfile
import io
import uuid
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime, timedelta
from pathlib import Path
import pytz
UTC = pytz.utc
from project.models_spartaqube import Dashboard, DashboardShared, Developer, DeveloperShared, Notebook, NotebookShared
from project.models import ShareRights
from project.sparta_8688631f3d.sparta_355a680bf7 import qube_1d2a59f054 as qube_1d2a59f054
from project.sparta_8688631f3d.sparta_97c9232dca import qube_de58073131 as qube_de58073131
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_8f0cad92aa import sparta_226d9606de, sparta_244cea0b2a
from project.sparta_8688631f3d.sparta_9df5aeb023 import qube_4009e9a33a as qube_4009e9a33a
from project.logger_config import logger


def sparta_09abdd9532(user_obj) ->list:
    """
    
    """
    user_group_set = qube_1d2a59f054.sparta_1c22139619(user_obj)
    if len(user_group_set) > 0:
        user_groups = [this_obj.user_group for this_obj in user_group_set]
    else:
        user_groups = []
    return user_groups


def sparta_a9cd3001f9(project_path) ->dict:
    """
    Create main_qube.ipynb file
    """
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    base_name = 'main_qube'
    file_name = f'{base_name}.ipynb'
    full_path = os.path.join(project_path, file_name)
    counter = 1
    while os.path.exists(full_path):
        file_name = f'{base_name}_{counter}.ipynb'
        full_path = os.path.join(project_path, file_name)
        counter += 1
    first_cell_code_empty_dashboard = """import pandas as pd
# There is two-way binding between the notebook and your dashboard components.
# Components linked to the notebook's variables can update their values
# Any changes made to the variables in the notebook will be immediately reflected on the dashboard, ensuring reactivity 

"""
    empty_notebook = qube_4009e9a33a.sparta_4a275ac0ae(
        first_cell_code_empty_dashboard)
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(empty_notebook, f, indent=4)
    logger.debug(f"Notebook '{file_name}' created successfully.")
    return {'file_name': file_name, 'file_path': project_path, 'full_path':
        full_path}


def sparta_8e228ce9df(json_data, user_obj) ->dict:
    """
    Validate project path 
    A valid project path is a folder that does not exists yet (and is valid in terms of expression)
    """
    project_path = json_data['projectPath']
    project_path = sparta_226d9606de(project_path)
    dashboard_set = Dashboard.objects.filter(project_path=project_path).all()
    if dashboard_set.count() > 0:
        dashboard_obj = dashboard_set[0]
        user_groups = sparta_09abdd9532(user_obj)
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
        if not has_edit_rights:
            return {'res': -1, 'errorMsg':
                'Chose another path. A dashboard already exists at this location'
                }
    if not isinstance(project_path, str):
        return {'res': -1, 'errorMsg': 'Project path must be a string.'}
    try:
        project_path = os.path.abspath(project_path)
    except Exception as e:
        return {'res': -1, 'errorMsg': f'Invalid project path: {str(e)}'}
    try:
        if not os.path.exists(project_path):
            os.makedirs(project_path)
        notebook_path_infos_dict = sparta_a9cd3001f9(project_path)
        main_ipynb_filename = notebook_path_infos_dict['file_name']
        main_ipynb_fullpath = notebook_path_infos_dict['full_path']
        return {'res': 1, 'main_ipynb_filename': main_ipynb_filename,
            'main_ipynb_fullpath': main_ipynb_fullpath}
    except Exception as e:
        return {'res': -1, 'errorMsg': f'Failed to create folder: {str(e)}'}


def sparta_c31124a4c6(json_data, user_obj) ->dict:
    """
    Dashboard list files and folders
    """
    project_path = json_data['path_to_explore']
    folder_structure = dict()
    folder_structure = {'___sq___folders___': [], '___sq___files___': [],
        '___sq___path___': project_path, '___sq___show___': 0}
    if os.path.exists(project_path):
        for entry in os.listdir(project_path):
            entry_path = os.path.join(project_path, entry)
            if os.path.isdir(entry_path):
                if not os.listdir(entry_path):
                    folder_structure['___sq___folders___'].append(entry)
                else:
                    folder_structure['___sq___folders___'].append(entry)
            elif os.path.isfile(entry_path):
                folder_structure['___sq___files___'].append(entry)
    res = {'res': 1, 'folderStructure': folder_structure}
    return res


def sparta_26fb7e83db(user_obj, json_data) ->dict:
    logger.debug('check_perform_project_explorer_action json_data')
    logger.debug(json_data)
    logger.debug(json_data.keys())
    project_path = json_data['projectPath']
    if 'dashboard_id' in json_data:
        return check_perform_project_explorer_action_dashboard(user_obj,
            json_data['dashboard_id'], project_path)
    if 'developer_id' in json_data:
        return check_perform_project_explorer_action_developer(user_obj,
            json_data['developer_id'], project_path)
    if 'notebook_id' in json_data:
        return check_perform_project_explorer_action_notebook(user_obj,
            json_data['notebook_id'], project_path)
    return {'res': 1}


def check_perform_project_explorer_action_dashboard(user_obj, dashboard_id,
    project_path) ->dict:
    """
    Check rights operations on resources (dashboard)
    """
    if len(dashboard_id) > 0:
        dashboard_set = Dashboard.objects.filter(dashboard_id__startswith=
            dashboard_id, is_delete=False).all()
        if dashboard_set.count() == 1:
            dashboard_obj = dashboard_set[dashboard_set.count() - 1]
            dashboard_id = dashboard_obj.dashboard_id
            user_groups = sparta_09abdd9532(user_obj)
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
                if (share_rights_obj.is_admin or share_rights_obj.has_write_rights):
                    has_edit_rights = True
            if has_edit_rights:
                return {'res': 1}
            else:
                return {'res': -1, 'errorMsg':
                    'You do not have the rights to perform this action'}
    return {'res': 1}


def check_perform_project_explorer_action_developer(user_obj, developer_id,
    project_path) ->dict:
    """
    Check rights operations on resources (developer)
    """
    if len(developer_id) > 0:
        developer_set = Developer.objects.filter(developer_id__startswith=
            developer_id, is_delete=False).all()
        if developer_set.count() == 1:
            developer_obj = developer_set[developer_set.count() - 1]
            developer_id = developer_obj.developer_id
            user_groups = sparta_09abdd9532(user_obj)
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
                if (share_rights_obj.is_admin or share_rights_obj.has_write_rights):
                    has_edit_rights = True
            if has_edit_rights:
                return {'res': 1}
            else:
                return {'res': -1, 'errorMsg':
                    'You do not have the rights to perform this action'}
    return {'res': 1}


def check_perform_project_explorer_action_notebook(user_obj, notebook_id,
    project_path) ->dict:
    """
    Check rights operations on resources (notebook)
    """
    if len(notebook_id) > 0:
        notebook_set = Notebook.objects.filter(notebook_id__startswith=
            notebook_id, is_delete=False).all()
        if notebook_set.count() == 1:
            notebook_obj = notebook_set[notebook_set.count() - 1]
            notebook_id = notebook_obj.notebook_id
            user_groups = sparta_09abdd9532(user_obj)
            if len(user_groups) > 0:
                notebook_shared_set = NotebookShared.objects.filter(Q(
                    is_delete=0, user_group__in=user_groups,
                    notebook__is_delete=0, notebook=notebook_obj) | Q(
                    is_delete=0, user=user_obj, notebook__is_delete=0,
                    notebook=notebook_obj))
            else:
                notebook_shared_set = NotebookShared.objects.filter(is_delete
                    =0, user=user_obj, notebook__is_delete=0, notebook=
                    notebook_obj)
            has_edit_rights = False
            if notebook_shared_set.count() > 0:
                notebook_shared_obj = notebook_shared_set[0]
                share_rights_obj = notebook_shared_obj.share_rights
                if (share_rights_obj.is_admin or share_rights_obj.has_write_rights):
                    has_edit_rights = True
            if has_edit_rights:
                return {'res': 1}
            else:
                return {'res': -1, 'errorMsg':
                    'You do not have the rights to perform this action'}
    return {'res': 1}


def sparta_0613c041f7(main_path: str, test_path: str) ->bool:
    main_path = Path(main_path).resolve()
    test_path = Path(test_path).resolve()
    return main_path in test_path.parents or main_path == test_path


def sparta_4a3bf7f1c2(json_data, user_obj) ->dict:
    """
    Create a new resource
    """
    logger.debug('Create resources')
    logger.debug(json_data)
    res_check_perform_actions_dict = sparta_26fb7e83db(
        user_obj, json_data)
    if res_check_perform_actions_dict['res'] == -1:
        return res_check_perform_actions_dict
    project_path = json_data['projectPath']
    project_path = sparta_226d9606de(project_path)
    resource_name = json_data['createResourceName']
    resource_type = json_data['createType']
    try:
        full_path = os.path.join(project_path, resource_name)
        if int(resource_type) == 1:
            path_resource = json_data['pathResource']
            path_resource_norm = sparta_226d9606de(path_resource)
            if len(path_resource) > 0:
                if not sparta_0613c041f7(project_path, path_resource_norm):
                    return {'res': -1, 'errorMsg': 'Invalid path'}
                full_path = os.path.join(path_resource_norm, resource_name)
            if not os.path.exists(full_path):
                os.makedirs(full_path)
        else:
            path_resource = json_data['pathResource']
            path_resource_norm = sparta_226d9606de(path_resource)
            if len(path_resource) > 0:
                if not sparta_0613c041f7(project_path, path_resource_norm):
                    return {'res': -1, 'errorMsg': 'Invalid path'}
                full_path = os.path.join(path_resource_norm, resource_name)
            if not os.path.exists(full_path):
                sparta_244cea0b2a(full_path)
            else:
                return {'res': -1, 'errorMsg':
                    'A file with this name already exists'}
    except Exception as e:
        logger.debug('Exception create new resource')
        logger.debug(e)
        return {'res': -1, 'errorMsg': str(e)}
    return {'res': 1}


def sparta_e1c56660b3(json_data, user_obj) ->dict:
    """
    Rename a resource
    """
    logger.debug('Rename resources')
    logger.debug(json_data)
    res_check_perform_actions_dict = sparta_26fb7e83db(
        user_obj, json_data)
    if res_check_perform_actions_dict['res'] == -1:
        return res_check_perform_actions_dict
    current_resource_path = json_data['pathResource']
    edit_name = json_data['editName']
    project_path = json_data['projectPath']
    project_path = sparta_226d9606de(project_path)
    rename_type = int(json_data['renameType'])
    if rename_type == 1:
        old_name = current_resource_path
        folder_up = os.path.dirname(current_resource_path)
        new_name = os.path.join(folder_up, edit_name)
        old_name = sparta_226d9606de(old_name)
        new_name = sparta_226d9606de(new_name)
        if project_path in new_name:
            try:
                os.rename(old_name, new_name)
            except Exception as e:
                return {'res': -1, 'errorMsg': str(e)}
    else:
        old_name = current_resource_path
        folder_up = os.path.dirname(current_resource_path)
        new_name = os.path.join(folder_up, edit_name)
        old_name = sparta_226d9606de(old_name)
        new_name = sparta_226d9606de(new_name)
        if project_path in new_name:
            try:
                os.rename(old_name, new_name)
            except Exception as e:
                return {'res': -1, 'errorMsg': str(e)}
    return {'res': 1}


def sparta_5ebd3cc888(json_data, user_obj) ->dict:
    """
    Move resources (drag & drop)
    """
    logger.debug('*' * 100)
    logger.debug('MOVE drag & drop resources')
    logger.debug(json_data)
    res_check_perform_actions_dict = sparta_26fb7e83db(
        user_obj, json_data)
    if res_check_perform_actions_dict['res'] == -1:
        return res_check_perform_actions_dict
    project_path = json_data['projectPath']
    project_path = sparta_226d9606de(project_path)
    folder_location = json_data['folderLocation']
    folder_location = sparta_226d9606de(folder_location)
    logger.debug('folder_location >>>>> ')
    logger.debug(folder_location)
    file_path_to_move_arr = json_data['filesPath2MoveArr']
    folder_path_to_move_arr = json_data['folderPath2MoveArr']
    for file_dict in file_path_to_move_arr:
        file_path = file_dict['path']
        file_name = file_dict['fileName']
        old_file_location = os.path.join(file_path, file_name)
        new_file_location = os.path.join(folder_location, file_name)
        old_file_location = sparta_226d9606de(old_file_location)
        new_file_location = sparta_226d9606de(new_file_location)
        if project_path in new_file_location:
            try:
                logger.debug(
                    f'Move from\n{old_file_location}\nto\n{new_file_location}')
                shutil.move(old_file_location, new_file_location)
            except Exception as e:
                logger.debug('Exception move 1')
                logger.debug(e)
    for folder_dict in folder_path_to_move_arr:
        folder_path = folder_dict['path']
        folder_path = sparta_226d9606de(folder_path)
        if project_path in folder_location:
            try:
                shutil.move(folder_path, folder_location)
            except:
                pass
    return {'res': 1}


def sparta_ff286b9290(json_data, user_obj) ->dict:
    """
    Delete one resource (either file or folder recursively)
    """
    logger.debug('Delete resource')
    logger.debug(json_data)
    res_check_perform_actions_dict = sparta_26fb7e83db(
        user_obj, json_data)
    if res_check_perform_actions_dict['res'] == -1:
        return res_check_perform_actions_dict
    project_path = json_data['projectPath']
    project_path = sparta_226d9606de(project_path)
    type_delete = int(json_data['typeDelete'])
    path_resource = json_data['pathResource']
    path_resource_norm = sparta_226d9606de(path_resource)
    if not sparta_0613c041f7(project_path, path_resource_norm):
        return {'res': -1, 'errorMsg': 'Invalid path'}
    if type_delete == 1:
        try:
            os.rmdir(path_resource_norm)
        except:
            try:
                os.system('rmdir /S /Q "{}"'.format(path_resource_norm))
            except:
                try:
                    shutil.rmtree(path_resource_norm)
                except Exception as e:
                    return {'res': -1, 'errorMsg': str(e)}
    else:
        try:
            os.remove(path_resource_norm)
        except Exception as e:
            return {'res': -1, 'errorMsg': str(e)}
    return {'res': 1}


def sparta_68623bf58b(json_data, user_obj
    ) ->dict:
    """
    Delete multiple resources (both files and folders)
    """
    logger.debug('Delete multiple resources')
    logger.debug(json_data)
    res_check_perform_actions_dict = sparta_26fb7e83db(
        user_obj, json_data)
    if res_check_perform_actions_dict['res'] == -1:
        return res_check_perform_actions_dict
    files_path_to_move_arr = json_data['filesPath2MoveArr']
    folder_path_to_move_arr = json_data['folderPath2MoveArr']
    project_path = json_data['projectPath']
    project_path = sparta_226d9606de(project_path)
    for file_dict in files_path_to_move_arr:
        this_file_name = file_dict['fileName']
        this_file_path = file_dict['path']
        file_path = os.path.join(this_file_path, this_file_name)
        file_path = sparta_226d9606de(file_path)
        if project_path in this_file_path:
            try:
                logger.debug(f'File to delete: {file_path}')
                os.remove(file_path)
            except Exception as e:
                return {'res': -1, 'errorMsg': str(e)}
    for file_dict in folder_path_to_move_arr:
        this_folder_path = file_dict['path']
        this_folder_path = sparta_226d9606de(this_folder_path)
        if project_path in this_folder_path:
            logger.debug(f'Delete folder {this_folder_path}')
            try:
                logger.debug(f'Folder to delete: {this_folder_path}')
                os.system('rmdir /S /Q "{}"'.format(this_folder_path))
            except:
                try:
                    logger.debug(f'Folder to delete: {this_folder_path}')
                    shutil.rmtree(this_folder_path)
                except Exception as e:
                    return {'res': -1, 'errorMsg': str(e)}
    return {'res': 1}


def sparta_ee39ec7777(json_data, user_obj):
    """
        Download resource
    """
    res_check_perform_actions_dict = sparta_26fb7e83db(
        user_obj, json_data)
    if res_check_perform_actions_dict['res'] == -1:
        return res_check_perform_actions_dict
    project_path = json_data['projectPath']
    path_resource = json_data['pathResource']
    path_resource_norm = sparta_226d9606de(path_resource)
    project_path = sparta_226d9606de(project_path)
    if project_path in path_resource_norm:
        return {'res': 1, 'fullPath': path_resource_norm}
    return {'res': -1}


def sparta_f81b92c030(json_data, user_obj):
    """
        Download resource
    """
    logger.debug('DOWNLOAD FOLDER DEBUG')
    logger.debug(json_data)
    app_path_folder = json_data['projectPath']
    zipName = json_data['folderName']

    def addFolderToZip(zf, folder):
        for file in os.listdir(folder):
            logger.debug('file > ' + str(file))
            full_path = os.path.join(folder, file)
            if os.path.isfile(full_path):
                zf.write(full_path, full_path.split(app_path_folder)[1])
            elif os.path.isdir(full_path):
                try:
                    addFolderToZip(zf, full_path)
                except Exception as e:
                    logger.debug('Except2')
                    logger.debug(e)
        return zf
    try:
        mf = io.BytesIO()
        with zipfile.ZipFile(mf, mode='w', compression=zipfile.ZIP_DEFLATED
            ) as zf:
            addFolderToZip(zf, app_path_folder)
        return {'res': 1, 'zip': mf, 'zipName': zipName}
    except Exception as e:
        logger.debug('Error Final')
        logger.debug(e)
    return {'res': -1}


def sparta_51ac70b2a9(json_data, user_obj):
    """
    Download all resources
    TODO: Change zipName with project's name
    """
    project_path = json_data['projectPath']
    res_check_perform_actions_dict = sparta_26fb7e83db(
        user_obj, json_data)
    if res_check_perform_actions_dict['res'] == -1:
        return res_check_perform_actions_dict
    zipName = 'app'

    def add_folder_to_zip(zf, folder):
        for file in os.listdir(folder):
            logger.debug('file > ' + str(file))
            full_path = os.path.join(folder, file)
            if os.path.isfile(full_path):
                zf.write(full_path, full_path.split(project_path)[1])
            elif os.path.isdir(full_path):
                try:
                    add_folder_to_zip(zf, full_path)
                except Exception as e:
                    logger.debug('Except2')
                    logger.debug(e)
        return zf
    try:
        mf = io.BytesIO()
        with zipfile.ZipFile(mf, mode='w', compression=zipfile.ZIP_DEFLATED
            ) as zf:
            add_folder_to_zip(zf, project_path)
        return {'res': 1, 'zip': mf, 'zipName': zipName}
    except Exception as e:
        logger.debug('Error Final')
        logger.debug(e)
    return {'res': -1}


def sparta_492c1f66ea(json_data, user_obj, file_obj):
    """
        Upload resources
    """
    logger.debug('**********************************')
    logger.debug('upload_resource')
    logger.debug(json_data)
    project_path = json_data['projectPath']
    res_check_perform_actions_dict = sparta_26fb7e83db(
        user_obj, json_data)
    if res_check_perform_actions_dict['res'] == -1:
        return res_check_perform_actions_dict
    path_resource = json_data['pathResource']
    project_path = sparta_226d9606de(project_path)
    if len(path_resource) == 0:
        path_resource = project_path
    else:
        path_resource = sparta_226d9606de(path_resource)
    path_folder = json_data['path']
    logger.debug(f'path_folder >> {path_folder}')
    if len(path_folder) > 0:
        folder_upload_path = os.path.join(path_resource, path_folder)
        folder_upload_path = sparta_226d9606de(folder_upload_path)
        if not os.path.exists(folder_upload_path):
            os.makedirs(folder_upload_path)
    else:
        folder_upload_path = os.path.join(path_resource, path_folder)
        folder_upload_path = sparta_226d9606de(folder_upload_path)
        if not os.path.exists(folder_upload_path):
            os.makedirs(folder_upload_path)
    file_path = os.path.join(folder_upload_path, file_obj.name)
    logger.debug(f'file_path > {file_path}')
    with open(file_path, 'wb') as file1:
        file1.write(file_obj.read())
    res = {'res': 1}
    return res


def sparta_da78a6b143(fileName) ->bool:
    """
    Return boolean if file type is handled by the preview manager or not
    """
    HANDLED_TYPES = ['pdf', 'png', 'jpg', 'jpeg']
    extension = fileName.split('.')[-1].lower()
    if extension in HANDLED_TYPES:
        return True
    return False


def sparta_5b5b9310b4(full_path) ->dict:
    """
    For specific file type, we need to load data as base64
    """
    res_dict = dict()
    extension = full_path.split('.')[-1].lower()
    if extension in ['pdf', 'png', 'jpg', 'jpeg']:
        with open(full_path, 'rb') as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read()).decode()
            res_dict['data'] = encoded_string
    return res_dict


def sparta_972a97df58(json_data, user_obj) ->dict:
    """
    Load File Resource (Ipynb)
    """
    project_path = json_data['projectPath']
    res_check_perform_actions_dict = sparta_26fb7e83db(
        user_obj, json_data)
    if res_check_perform_actions_dict['res'] == -1:
        return res_check_perform_actions_dict
    full_path = sparta_226d9606de(json_data['fullPath'])
    ipynb_dict = qube_4009e9a33a.sparta_1dbf0a0a23(full_path)
    return {'res': 1, 'ipynb_dict': json.dumps(ipynb_dict)}


def sparta_4fca1c890c(json_data, user_obj) ->dict:
    """
    Load File Resource (Generique)
    """
    file_name = json_data['fileName']
    full_path = json_data['fullPath']
    full_path = sparta_226d9606de(full_path)
    project_path = json_data['projectPath']
    project_path = sparta_226d9606de(project_path)
    res_check_perform_actions_dict = sparta_26fb7e83db(
        user_obj, json_data)
    if res_check_perform_actions_dict['res'] == -1:
        return res_check_perform_actions_dict
    is_previewable = False
    is_handled = False
    cm_mode = ''
    file_content = ''
    file_extension = file_name.split('.')[-1].lower()
    code_mirror_types_list = sparta_a4859bf493()
    for this_elem_dict in code_mirror_types_list:
        try:
            if file_extension in this_elem_dict['ext']:
                is_previewable = True
                cm_mode = this_elem_dict['mode']
        except:
            pass
    if is_previewable:
        try:
            with open(full_path) as f:
                file_content = json.dumps(f.read())
        except Exception as e:
            return {'res': 1, 'is_handled': is_handled, 'is_previewable': 
                False, 'cm_mode': cm_mode, 'file_content': file_content,
                'file_extension': file_extension, 'errorMsg': str(e)}
    else:
        if sparta_da78a6b143(full_path):
            file_extension = full_path.split('.')[-1]
            resource_dict = sparta_5b5b9310b4(full_path)
            return {'res': 1, 'is_handled': True, 'is_previewable':
                is_previewable, 'cm_mode': cm_mode, 'file_content':
                file_content, 'file_extension': file_extension, 'resource':
                resource_dict}
        file_extension = full_path.split('.')[-1]
        if file_extension == 'ipynb':
            logger.debug('JUPYTER NOTEBOOK')
            with open(full_path) as f:
                file_content = f.read()
            file_content = json.loads(file_content)
            cells = file_content['cells']
            cells_source_arr = [thisObj['source'] for thisObj in cells]
            return {'res': 1, 'is_handled': True, 'is_previewable': False,
                'cm_mode': 'ipynb', 'file_content': file_content,
                'file_extension': 'ipynb', 'cells': cells_source_arr}
    return {'res': 1, 'is_handled': is_handled, 'is_previewable':
        is_previewable, 'cm_mode': cm_mode, 'file_content': file_content,
        'file_extension': file_extension}


def sparta_8c81f8dd3d(json_data, user_obj) ->dict:
    """
    Save file content of a generique resource
    """
    source_code = json_data['sourceCode']
    full_path = json_data['fullPath']
    full_path = sparta_226d9606de(full_path)
    project_path = json_data['projectPath']
    project_path = sparta_226d9606de(project_path)
    res_check_perform_actions_dict = sparta_26fb7e83db(
        user_obj, json_data)
    if res_check_perform_actions_dict['res'] == -1:
        return res_check_perform_actions_dict
    with open(full_path, 'w') as file:
        file.write(source_code)
    return {'res': 1}


def sparta_a4859bf493() ->list:
    CODE_MIRROR_TYPE_ARR = [{'name': 'APL', 'mime': 'text/apl', 'mode':
        'apl', 'ext': ['dyalog', 'apl']}, {'name': 'PGP', 'mimes': [
        'application/pgp', 'application/pgp-encrypted',
        'application/pgp-keys', 'application/pgp-signature'], 'mode':
        'asciiarmor', 'ext': ['asc', 'pgp', 'sig']}, {'name': 'ASN.1',
        'mime': 'text/x-ttcn-asn', 'mode': 'asn.1', 'ext': ['asn', 'asn1']},
        {'name': 'Asterisk', 'mime': 'text/x-asterisk', 'mode': 'asterisk',
        'file': '/^extensions\\.conf$/i'}, {'name': 'Brainfuck', 'mime':
        'text/x-brainfuck', 'mode': 'brainfuck', 'ext': ['b', 'bf']}, {
        'name': 'C', 'mime': 'text/x-csrc', 'mode': 'clike', 'ext': ['c',
        'h', 'ino']}, {'name': 'C++', 'mime': 'text/x-c++src', 'mode':
        'clike', 'ext': ['cpp', 'c++', 'cc', 'cxx', 'hpp', 'h++', 'hh',
        'hxx'], 'alias': ['cpp']}, {'name': 'Cobol', 'mime': 'text/x-cobol',
        'mode': 'cobol', 'ext': ['cob', 'cpy']}, {'name': 'C#', 'mime':
        'text/x-csharp', 'mode': 'clike', 'ext': ['cs'], 'alias': ['csharp'
        ]}, {'name': 'Clojure', 'mime': 'text/x-clojure', 'mode': 'clojure',
        'ext': ['clj', 'cljc', 'cljx']}, {'name': 'ClojureScript', 'mime':
        'text/x-clojurescript', 'mode': 'clojure', 'ext': ['cljs']}, {
        'name': 'Closure Stylesheets (GSS)', 'mime': 'text/x-gss', 'mode':
        'css', 'ext': ['gss']}, {'name': 'CMake', 'mime': 'text/x-cmake',
        'mode': 'cmake', 'ext': ['cmake', 'cmake.in'], 'file':
        '/^CMakeLists.txt$/'}, {'name': 'CoffeeScript', 'mimes': [
        'application/vnd.coffeescript', 'text/coffeescript',
        'text/x-coffeescript'], 'mode': 'coffeescript', 'ext': ['coffee'],
        'alias': ['coffee', 'coffee-script']}, {'name': 'Common Lisp',
        'mime': 'text/x-common-lisp', 'mode': 'commonlisp', 'ext': ['cl',
        'lisp', 'el'], 'alias': ['lisp']}, {'name': 'Cypher', 'mime':
        'application/x-cypher-query', 'mode': 'cypher', 'ext': ['cyp',
        'cypher']}, {'name': 'Cython', 'mime': 'text/x-cython', 'mode':
        'python', 'ext': ['pyx', 'pxd', 'pxi']}, {'name': 'Crystal', 'mime':
        'text/x-crystal', 'mode': 'crystal', 'ext': ['cr']}, {'name': 'CSS',
        'mime': 'text/css', 'mode': 'css', 'ext': ['css']}, {'name': 'CQL',
        'mime': 'text/x-cassandra', 'mode': 'sql', 'ext': ['cql']}, {'name':
        'D', 'mime': 'text/x-d', 'mode': 'd', 'ext': ['d']}, {'name':
        'Dart', 'mimes': ['application/dart', 'text/x-dart'], 'mode':
        'dart', 'ext': ['dart']}, {'name': 'diff', 'mime': 'text/x-diff',
        'mode': 'diff', 'ext': ['diff', 'patch']}, {'name': 'Django',
        'mime': 'text/x-django', 'mode': 'django'}, {'name': 'Dockerfile',
        'mime': 'text/x-dockerfile', 'mode': 'dockerfile', 'file':
        '/^Dockerfile$/'}, {'name': 'DTD', 'mime': 'application/xml-dtd',
        'mode': 'dtd', 'ext': ['dtd']}, {'name': 'Dylan', 'mime':
        'text/x-dylan', 'mode': 'dylan', 'ext': ['dylan', 'dyl', 'intr']},
        {'name': 'EBNF', 'mime': 'text/x-ebnf', 'mode': 'ebnf'}, {'name':
        'ECL', 'mime': 'text/x-ecl', 'mode': 'ecl', 'ext': ['ecl']}, {
        'name': 'edn', 'mime': 'application/edn', 'mode': 'clojure', 'ext':
        ['edn']}, {'name': 'Eiffel', 'mime': 'text/x-eiffel', 'mode':
        'eiffel', 'ext': ['e']}, {'name': 'Elm', 'mime': 'text/x-elm',
        'mode': 'elm', 'ext': ['elm']}, {'name': 'Embedded Javascript',
        'mime': 'application/x-ejs', 'mode': 'htmlembedded', 'ext': ['ejs']
        }, {'name': 'Embedded Ruby', 'mime': 'application/x-erb', 'mode':
        'htmlembedded', 'ext': ['erb']}, {'name': 'Erlang', 'mime':
        'text/x-erlang', 'mode': 'erlang', 'ext': ['erl']}, {'name':
        'Esper', 'mime': 'text/x-esper', 'mode': 'sql'}, {'name': 'Factor',
        'mime': 'text/x-factor', 'mode': 'factor', 'ext': ['factor']}, {
        'name': 'FCL', 'mime': 'text/x-fcl', 'mode': 'fcl'}, {'name':
        'Forth', 'mime': 'text/x-forth', 'mode': 'forth', 'ext': ['forth',
        'fth', '4th']}, {'name': 'Fortran', 'mime': 'text/x-fortran',
        'mode': 'fortran', 'ext': ['f', 'for', 'f77', 'f90']}, {'name':
        'F#', 'mime': 'text/x-fsharp', 'mode': 'mllike', 'ext': ['fs'],
        'alias': ['fsharp']}, {'name': 'Gas', 'mime': 'text/x-gas', 'mode':
        'gas', 'ext': ['s']}, {'name': 'Gherkin', 'mime': 'text/x-feature',
        'mode': 'gherkin', 'ext': ['feature']}, {'name':
        'GitHub Flavored Markdown', 'mime': 'text/x-gfm', 'mode': 'gfm',
        'file': '/^(readme|contributing|history).md$/i'}, {'name': 'Go',
        'mime': 'text/x-go', 'mode': 'go', 'ext': ['go']}, {'name':
        'Groovy', 'mime': 'text/x-groovy', 'mode': 'groovy', 'ext': [
        'groovy', 'gradle'], 'file': '/^Jenkinsfile$/'}, {'name': 'HAML',
        'mime': 'text/x-haml', 'mode': 'haml', 'ext': ['haml']}, {'name':
        'Haskell', 'mime': 'text/x-haskell', 'mode': 'haskell', 'ext': [
        'hs']}, {'name': 'Haskell (Literate)', 'mime':
        'text/x-literate-haskell', 'mode': 'haskell-literate', 'ext': [
        'lhs']}, {'name': 'Haxe', 'mime': 'text/x-haxe', 'mode': 'haxe',
        'ext': ['hx']}, {'name': 'HXML', 'mime': 'text/x-hxml', 'mode':
        'haxe', 'ext': ['hxml']}, {'name': 'ASP.NET', 'mime':
        'application/x-aspx', 'mode': 'htmlembedded', 'ext': ['aspx'],
        'alias': ['asp', 'aspx']}, {'name': 'HTML', 'mime': 'text/html',
        'mode': 'htmlmixed', 'ext': ['html', 'htm', 'handlebars', 'hbs'],
        'alias': ['xhtml']}, {'name': 'HTTP', 'mime': 'message/http',
        'mode': 'http'}, {'name': 'IDL', 'mime': 'text/x-idl', 'mode':
        'idl', 'ext': ['pro']}, {'name': 'Pug', 'mime': 'text/x-pug',
        'mode': 'pug', 'ext': ['jade', 'pug'], 'alias': ['jade']}, {'name':
        'Java', 'mime': 'text/x-java', 'mode': 'clike', 'ext': ['java']}, {
        'name': 'Java Server Pages', 'mime': 'application/x-jsp', 'mode':
        'htmlembedded', 'ext': ['jsp'], 'alias': ['jsp']}, {'name':
        'JavaScript', 'mimes': ['text/javascript', 'text/ecmascript',
        'application/javascript', 'application/x-javascript',
        'application/ecmascript'], 'mode': 'javascript', 'ext': ['js'],
        'alias': ['ecmascript', 'js', 'node']}, {'name': 'JSON', 'mimes': [
        'application/json', 'application/x-json'], 'mode': 'javascript',
        'ext': ['json', 'map'], 'alias': ['json5']}, {'name': 'JSON-LD',
        'mime': 'application/ld+json', 'mode': 'javascript', 'ext': [
        'jsonld'], 'alias': ['jsonld']}, {'name': 'JSX', 'mime': 'text/jsx',
        'mode': 'jsx', 'ext': ['jsx']}, {'name': 'Jinja2', 'mime': 'null',
        'mode': 'jinja2', 'ext': ['j2', 'jinja', 'jinja2']}, {'name':
        'Julia', 'mime': 'text/x-julia', 'mode': 'julia', 'ext': ['jl']}, {
        'name': 'Kotlin', 'mime': 'text/x-kotlin', 'mode': 'clike', 'ext':
        ['kt']}, {'name': 'LESS', 'mime': 'text/x-less', 'mode': 'css',
        'ext': ['less']}, {'name': 'LiveScript', 'mime':
        'text/x-livescript', 'mode': 'livescript', 'ext': ['ls'], 'alias':
        ['ls']}, {'name': 'Lua', 'mime': 'text/x-lua', 'mode': 'lua', 'ext':
        ['lua']}, {'name': 'Markdown', 'mime': 'text/x-markdown', 'mode':
        'markdown', 'ext': ['markdown', 'md', 'mkd']}, {'name': 'mIRC',
        'mime': 'text/mirc', 'mode': 'mirc'}, {'name': 'MariaDB SQL',
        'mime': 'text/x-mariadb', 'mode': 'sql'}, {'name': 'Mathematica',
        'mime': 'text/x-mathematica', 'mode': 'mathematica', 'ext': ['m',
        'nb']}, {'name': 'Modelica', 'mime': 'text/x-modelica', 'mode':
        'modelica', 'ext': ['mo']}, {'name': 'MUMPS', 'mime':
        'text/x-mumps', 'mode': 'mumps', 'ext': ['mps']}, {'name': 'MS SQL',
        'mime': 'text/x-mssql', 'mode': 'sql'}, {'name': 'mbox', 'mime':
        'application/mbox', 'mode': 'mbox', 'ext': ['mbox']}, {'name':
        'MySQL', 'mime': 'text/x-mysql', 'mode': 'sql'}, {'name': 'Nginx',
        'mime': 'text/x-nginx-conf', 'mode': 'nginx', 'file':
        '/nginx.*\\.conf$/i'}, {'name': 'NSIS', 'mime': 'text/x-nsis',
        'mode': 'nsis', 'ext': ['nsh', 'nsi']}, {'name': 'NTriples',
        'mimes': ['application/n-triples', 'application/n-quads',
        'text/n-triples'], 'mode': 'ntriples', 'ext': ['nt', 'nq']}, {
        'name': 'Objective-C', 'mime': 'text/x-objectivec', 'mode': 'clike',
        'ext': ['m', 'mm'], 'alias': ['objective-c', 'objc']}, {'name':
        'OCaml', 'mime': 'text/x-ocaml', 'mode': 'mllike', 'ext': ['ml',
        'mli', 'mll', 'mly']}, {'name': 'Octave', 'mime': 'text/x-octave',
        'mode': 'octave', 'ext': ['m']}, {'name': 'Oz', 'mime': 'text/x-oz',
        'mode': 'oz', 'ext': ['oz']}, {'name': 'Pascal', 'mime':
        'text/x-pascal', 'mode': 'pascal', 'ext': ['p', 'pas']}, {'name':
        'PEG.js', 'mime': 'null', 'mode': 'pegjs', 'ext': ['jsonld']}, {
        'name': 'Perl', 'mime': 'text/x-perl', 'mode': 'perl', 'ext': ['pl',
        'pm']}, {'name': 'PHP', 'mimes': ['text/x-php',
        'application/x-httpd-php', 'application/x-httpd-php-open'], 'mode':
        'php', 'ext': ['php', 'php3', 'php4', 'php5', 'php7', 'phtml']}, {
        'name': 'Pig', 'mime': 'text/x-pig', 'mode': 'pig', 'ext': ['pig']},
        {'name': 'Plain Text', 'mime': 'text/plain', 'mode': 'htmlmixed',
        'ext': ['txt', 'text', 'conf', 'def', 'list', 'log']}, {'name':
        'PLSQL', 'mime': 'text/x-plsql', 'mode': 'sql', 'ext': ['pls']}, {
        'name': 'PowerShell', 'mime': 'application/x-powershell', 'mode':
        'powershell', 'ext': ['ps1', 'psd1', 'psm1']}, {'name':
        'Properties files', 'mime': 'text/x-properties', 'mode':
        'properties', 'ext': ['properties', 'ini', 'in'], 'alias': ['ini',
        'properties']}, {'name': 'ProtoBuf', 'mime': 'text/x-protobuf',
        'mode': 'protobuf', 'ext': ['proto']}, {'name': 'Python', 'mime':
        'text/x-python', 'mode': 'python', 'ext': ['BUILD', 'bzl', 'py',
        'pyw'], 'file': '/^(BUCK|BUILD)$/'}, {'name': 'Puppet', 'mime':
        'text/x-puppet', 'mode': 'puppet', 'ext': ['pp']}, {'name': 'Q',
        'mime': 'text/x-q', 'mode': 'q', 'ext': ['q']}, {'name': 'R',
        'mime': 'text/x-rsrc', 'mode': 'r', 'ext': ['r', 'R'], 'alias': [
        'rscript']}, {'name': 'reStructuredText', 'mime': 'text/x-rst',
        'mode': 'rst', 'ext': ['rst'], 'alias': ['rst']}, {'name':
        'RPM Changes', 'mime': 'text/x-rpm-changes', 'mode': 'rpm'}, {
        'name': 'RPM Spec', 'mime': 'text/x-rpm-spec', 'mode': 'rpm', 'ext':
        ['spec']}, {'name': 'Ruby', 'mime': 'text/x-ruby', 'mode': 'ruby',
        'ext': ['rb'], 'alias': ['jruby', 'macruby', 'rake', 'rb', 'rbx']},
        {'name': 'Rust', 'mime': 'text/x-rustsrc', 'mode': 'rust', 'ext': [
        'rs']}, {'name': 'SAS', 'mime': 'text/x-sas', 'mode': 'sas', 'ext':
        ['sas']}, {'name': 'Sass', 'mime': 'text/x-sass', 'mode': 'sass',
        'ext': ['sass']}, {'name': 'Scala', 'mime': 'text/x-scala', 'mode':
        'clike', 'ext': ['scala']}, {'name': 'Scheme', 'mime':
        'text/x-scheme', 'mode': 'scheme', 'ext': ['scm', 'ss']}, {'name':
        'SCSS', 'mime': 'text/x-scss', 'mode': 'css', 'ext': ['scss']}, {
        'name': 'Shell', 'mimes': ['text/x-sh', 'application/x-sh'], 'mode':
        'shell', 'ext': ['sh', 'ksh', 'bash', 'bat'], 'alias': ['bash',
        'sh', 'zsh', 'bat'], 'file': '/^PKGBUILD$/'}, {'name': 'Sieve',
        'mime': 'application/sieve', 'mode': 'sieve', 'ext': ['siv',
        'sieve']}, {'name': 'Slim', 'mimes': ['text/x-slim',
        'application/x-slim'], 'mode': 'slim', 'ext': ['slim']}, {'name':
        'Smalltalk', 'mime': 'text/x-stsrc', 'mode': 'smalltalk', 'ext': [
        'st']}, {'name': 'Smarty', 'mime': 'text/x-smarty', 'mode':
        'smarty', 'ext': ['tpl']}, {'name': 'Solr', 'mime': 'text/x-solr',
        'mode': 'solr'}, {'name': 'SML', 'mime': 'text/x-sml', 'mode':
        'mllike', 'ext': ['sml', 'sig', 'fun', 'smackspec']}, {'name':
        'Soy', 'mime': 'text/x-soy', 'mode': 'soy', 'ext': ['soy'], 'alias':
        ['closure template']}, {'name': 'SPARQL', 'mime':
        'application/sparql-query', 'mode': 'sparql', 'ext': ['rq',
        'sparql'], 'alias': ['sparul']}, {'name': 'Spreadsheet', 'mime':
        'text/x-spreadsheet', 'mode': 'spreadsheet', 'alias': ['excel',
        'formula']}, {'name': 'SQL', 'mime': 'text/x-sql', 'mode': 'sql',
        'ext': ['sql']}, {'name': 'SQLite', 'mime': 'text/x-sqlite', 'mode':
        'sql'}, {'name': 'Squirrel', 'mime': 'text/x-squirrel', 'mode':
        'clike', 'ext': ['nut']}, {'name': 'Stylus', 'mime': 'text/x-styl',
        'mode': 'stylus', 'ext': ['styl']}, {'name': 'Swift', 'mime':
        'text/x-swift', 'mode': 'swift', 'ext': ['swift']}, {'name': 'sTeX',
        'mime': 'text/x-stex', 'mode': 'stex'}, {'name': 'LaTeX', 'mime':
        'text/x-latex', 'mode': 'stex', 'ext': ['text', 'ltx', 'tex'],
        'alias': ['tex']}, {'name': 'SystemVerilog', 'mime':
        'text/x-systemverilog', 'mode': 'verilog', 'ext': ['v', 'sv', 'svh'
        ]}, {'name': 'Tcl', 'mime': 'text/x-tcl', 'mode': 'tcl', 'ext': [
        'tcl']}, {'name': 'Textile', 'mime': 'text/x-textile', 'mode':
        'textile', 'ext': ['textile']}, {'name': 'TiddlyWiki ', 'mime':
        'text/x-tiddlywiki', 'mode': 'tiddlywiki'}, {'name': 'Tiki wiki',
        'mime': 'text/tiki', 'mode': 'tiki'}, {'name': 'TOML', 'mime':
        'text/x-toml', 'mode': 'toml', 'ext': ['toml']}, {'name': 'Tornado',
        'mime': 'text/x-tornado', 'mode': 'tornado'}, {'name': 'troff',
        'mime': 'text/troff', 'mode': 'troff', 'ext': ['1', '2', '3', '4',
        '5', '6', '7', '8', '9']}, {'name': 'TTCN', 'mime': 'text/x-ttcn',
        'mode': 'ttcn', 'ext': ['ttcn', 'ttcn3', 'ttcnpp']}, {'name':
        'TTCN_CFG', 'mime': 'text/x-ttcn-cfg', 'mode': 'ttcn-cfg', 'ext': [
        'cfg']}, {'name': 'Turtle', 'mime': 'text/turtle', 'mode': 'turtle',
        'ext': ['ttl']}, {'name': 'TypeScript', 'mime':
        'application/typescript', 'mode': 'javascript', 'ext': ['ts'],
        'alias': ['ts']}, {'name': 'TypeScript-JSX', 'mime':
        'text/typescript-jsx', 'mode': 'jsx', 'ext': ['tsx'], 'alias': [
        'tsx']}, {'name': 'Twig', 'mime': 'text/x-twig', 'mode': 'twig'}, {
        'name': 'Web IDL', 'mime': 'text/x-webidl', 'mode': 'webidl', 'ext':
        ['webidl']}, {'name': 'VB.NET', 'mime': 'text/x-vb', 'mode': 'vb',
        'ext': ['vb']}, {'name': 'VBScript', 'mime': 'text/vbscript',
        'mode': 'vbscript', 'ext': ['vbs']}, {'name': 'Velocity', 'mime':
        'text/velocity', 'mode': 'velocity', 'ext': ['vtl']}, {'name':
        'Verilog', 'mime': 'text/x-verilog', 'mode': 'verilog', 'ext': ['v'
        ]}, {'name': 'VHDL', 'mime': 'text/x-vhdl', 'mode': 'vhdl', 'ext':
        ['vhd', 'vhdl']}, {'name': 'Vue.js Component', 'mimes': [
        'script/x-vue', 'text/x-vue'], 'mode': 'vue', 'ext': ['vue']}, {
        'name': 'XML', 'mimes': ['application/xml', 'text/xml'], 'mode':
        'xml', 'ext': ['xml', 'xsl', 'xsd', 'svg'], 'alias': ['rss', 'wsdl',
        'xsd']}, {'name': 'XQuery', 'mime': 'application/xquery', 'mode':
        'xquery', 'ext': ['xy', 'xquery']}, {'name': 'Yacas', 'mime':
        'text/x-yacas', 'mode': 'yacas', 'ext': ['ys']}, {'name': 'YAML',
        'mimes': ['text/x-yaml', 'text/yaml'], 'mode': 'yaml', 'ext': [
        'yaml', 'yml'], 'alias': ['yml']}, {'name': 'Z80', 'mime':
        'text/x-z80', 'mode': 'z80', 'ext': ['z80']}, {'name': 'mscgen',
        'mime': 'text/x-mscgen', 'mode': 'mscgen', 'ext': ['mscgen',
        'mscin', 'msc']}, {'name': 'xu', 'mime': 'text/x-xu', 'mode':
        'mscgen', 'ext': ['xu']}, {'name': 'msgenny', 'mime':
        'text/x-msgenny', 'mode': 'mscgen', 'ext': ['msgenny']}, {'name':
        '.gitignore', 'mime': 'text/plain', 'mode': 'htmlmixed', 'file':
        '/^\\.gitignore$/', 'ext': ['gitignore']}]
    return CODE_MIRROR_TYPE_ARR


def sparta_b176389378(json_data, user_obj) ->dict:
    """
    Save file content of an ipynb resource
    """
    full_path = json_data['fullPath']
    full_path = sparta_226d9606de(full_path)
    project_path = json_data['projectPath']
    project_path = sparta_226d9606de(project_path)
    dashboard_id = json_data['dashboardId']
    res_check_perform_actions_dict = sparta_26fb7e83db(
        user_obj, json_data)
    if res_check_perform_actions_dict['res'] == -1:
        return res_check_perform_actions_dict
    logger.debug('*=' * 100)
    logger.debug('ide_save_ipynb_resource json_data')
    logger.debug(json_data)
    logger.debug(json_data.keys())
    full_path = sparta_226d9606de(full_path)
    notebook_cells_arr: list = json_data['notebookCellsArr']
    res_saved_ipynb_raw_file_dict = (qube_4009e9a33a.save_ipnyb_from_notebook_cells(notebook_cells_arr, full_path,
        dashboard_id))
    return res_saved_ipynb_raw_file_dict

#END OF QUBE
