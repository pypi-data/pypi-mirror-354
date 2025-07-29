import os
import shutil
import zipfile
import io
import uuid
from distutils.dir_util import copy_tree
from project.sparta_8345d6a892.sparta_87f32c6e97 import qube_93b4ab09a2 as qube_93b4ab09a2
from project.sparta_8345d6a892.sparta_952c41e91e import qube_41685030f2 as qube_41685030f2
from project.sparta_8345d6a892.sparta_db87358646 import qube_af0123880b as qube_af0123880b
from project.logger_config import logger


def sparta_a4ba1220dd() ->str:
    return str(uuid.uuid4())


def sparta_17120ae264(app_id) ->str:
    """
    Create a new app folder
    """
    base_path_app_folder = coreApps.get_app_folder_default_path()
    app_folder_path = os.path.join(base_path_app_folder, app_id)
    if not os.path.exists(app_folder_path):
        os.makedirs(app_folder_path)
    return app_folder_path


def sparta_08dec8a2f2(project_path):
    """
    
    """
    try:
        if not os.path.exists(project_path):
            os.makedirs(project_path)
        return {'res': 1}
    except Exception as e:
        return {'res': -1, 'errorMsg': str(e)}


def sparta_91bd932e94(path):
    with open(path, 'a'):
        os.utime(path, None)


def sparta_5ec460944d(json_data, userObj):
    """
        Create resource (file or folder)
    """
    logger.debug('CREATE RESOURCE')
    logger.debug(json_data)
    project_path = json_data['projectPath']
    res_create_project_path = sparta_08dec8a2f2(project_path)
    if res_create_project_path['res'] == -1:
        return res_create_project_path
    resource_name = json_data['createResourceName']
    resource_type = json_data['createType']
    try:
        full_path = os.path.join(project_path, resource_name)
        if int(resource_type) == 1:
            if not os.path.exists(full_path):
                os.makedirs(full_path)
        elif not os.path.exists(full_path):
            sparta_91bd932e94(full_path)
        else:
            return {'res': -1, 'errorMsg':
                'A file with this name already exists'}
    except Exception as e:
        logger.debug('Exception create new resource')
        logger.debug(e)
        return {'res': -1, 'errorMsg': str(e)}
    return {'res': 1}


def sparta_7dc019011e(json_data, userObj):
    """
        Move resource (file and/or folder)
    """
    app_path_folder = json_data['projectPath']
    folder_location = json_data['folder_location']
    file_path_to_move_arr = json_data['filesPath2MoveArr']
    folder_path_to_move_arr = json_data['folderPath2MoveArr']
    for file_dict in file_path_to_move_arr:
        file_path = file_dict['path']
        file_name = file_dict['fileName']
        old_file_location = os.path.join(file_path, file_name)
        new_file_location = os.path.join(folder_location, file_name)
        if app_path_folder in new_file_location:
            try:
                logger.debug(
                    f'Move from\n{old_file_location}\nto\n{new_file_location}')
                shutil.move(old_file_location, new_file_location)
            except Exception as e:
                logger.debug('Exception move 1')
                logger.debug(e)
    for file_dict in folder_path_to_move_arr:
        folder_path = file_dict['path']
        if app_path_folder in folder_location:
            try:
                shutil.move(folder_path, folder_location)
            except:
                pass
    return {'res': 1}


def sparta_482110f514(json_data, user_obj, file_obj_to_upload):
    """
        Upload resources
        # TODO : File already exists (replace)
        # TODO : Folder already exists (replace all contents)
    """
    app_path_folder = json_data['projectPath']
    res_create_project_path = sparta_08dec8a2f2(app_path_folder)
    if res_create_project_path['res'] == -1:
        return res_create_project_path
    path_folder = json_data['path']
    dragover_elem = json_data['dragoverElem']
    logger.debug('dragover_elem ')
    logger.debug(dragover_elem)
    if len(dragover_elem) > 0:
        notebook_folder_path = dragover_elem
    if len(path_folder) > 0:
        app_path_folder = os.path.join(app_path_folder, path_folder)
        if not os.path.exists(app_path_folder):
            os.makedirs(app_path_folder)
    file_path = os.path.join(app_path_folder, file_obj_to_upload.name)
    with open(file_path, 'wb') as file1:
        file1.write(file_obj_to_upload.read())
    res = {'res': 1}
    return res


def sparta_3499f54fac(json_data, userObj):
    """
    Load files and folder structure to display in the GUI
    """
    project_path = json_data['projectPath']
    folder_structure = (qube_af0123880b.get_folder_and_files_recursively_from_path(project_path))
    res = {'res': 1, 'folderStructure': folder_structure}
    return res


def sparta_ed41ad0d88(json_data, userObj):
    """
        Save the content of a file (like the source code)
    """
    try:
        app_path_folder = json_data['projectPath']
        file_name = json_data['fileName']
        file_path = json_data['filePath']
        source_code = json_data['sourceCode']
        if app_path_folder in file_path:
            file_path = os.path.join(file_path, file_name)
            with open(file_path, 'w') as file:
                file.write(source_code)
        return {'res': 1}
    except Exception as e:
        return {'res': -1, 'errorMsg': str(e)}


def sparta_f691ead76a(json_data, userObj):
    """
        Rename resource
    """
    app_path_folder = json_data['projectPath']
    file_name = json_data['fileName']
    file_path = json_data['filePath']
    edit_name = json_data['editName']
    rename_type = int(json_data['renameType'])
    if app_path_folder in file_path:
        if rename_type == 1:
            folder_up = os.path.dirname(file_path)
            old_name = os.path.join(folder_up, file_name)
            new_name = os.path.join(folder_up, edit_name)
            try:
                os.rename(old_name, new_name)
            except Exception as e:
                return {'res': -1, 'errorMsg': str(e)}
        else:
            old_name = os.path.join(file_path, file_name)
            new_name = os.path.join(file_path, edit_name)
            try:
                os.rename(old_name, new_name)
            except Exception as e:
                return {'res': -1, 'errorMsg': str(e)}
    return {'res': 1}


def sparta_792035baa8(json_data, userObj):
    """
        Delete resource
    """
    app_path_folder = json_data['projectPath']
    file_name = json_data['fileName']
    file_path = json_data['filePath']
    typeDelete = int(json_data['typeDelete'])
    if app_path_folder in file_path:
        if typeDelete == 1:
            try:
                os.rmdir(file_path)
            except:
                try:
                    os.system('rmdir /S /Q "{}"'.format(file_path))
                except:
                    try:
                        shutil.rmtree(file_path)
                    except Exception as e:
                        return {'res': -1, 'errorMsg': str(e)}
        else:
            file_path = os.path.join(file_path, file_name)
            try:
                os.remove(file_path)
            except Exception as e:
                return {'res': -1, 'errorMsg': str(e)}
    return {'res': 1}


def sparta_8057525859(json_data, userObj):
    """
        Delete multiple resources
    """
    files_path_to_move_arr = json_data['filesPath2MoveArr']
    folder_path_to_move_arr = json_data['folderPath2MoveArr']
    app_path_folder = json_data['projectPath']
    for file_dict in files_path_to_move_arr:
        this_file_name = file_dict['fileName']
        this_file_path = file_dict['path']
        if app_path_folder in this_file_path:
            file_path = os.path.join(this_file_path, this_file_name)
            try:
                os.remove(file_path)
            except Exception as e:
                return {'res': -1, 'errorMsg': str(e)}
    for file_dict in folder_path_to_move_arr:
        this_folder_path = file_dict['path']
        logger.debug(f'Delete folder {this_folder_path}')
        try:
            os.system('rmdir /S /Q "{}"'.format(this_folder_path))
        except:
            try:
                shutil.rmtree(this_folder_path)
            except Exception as e:
                return {'res': -1, 'errorMsg': str(e)}
    return {'res': 1}


def sparta_91e4c34830(json_data, userObj):
    """
        Download resource
    """
    app_path_folder = json_data['projectPath']
    file_name = json_data['fileName']
    file_path = json_data['filePath']
    if app_path_folder in file_path:
        full_path = os.path.join(file_path, file_name)
        return {'res': 1, 'fullPath': full_path}
    return {'res': -1}


def sparta_2ae29b78a0(json_data, userObj):
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


def sparta_e74173774a(json_data, userObj):
    """
    Download all resources
    TODO: Change zipName with project's name
    """
    app_path_folder = json_data['projectPath']
    zipName = 'app'

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

#END OF QUBE
