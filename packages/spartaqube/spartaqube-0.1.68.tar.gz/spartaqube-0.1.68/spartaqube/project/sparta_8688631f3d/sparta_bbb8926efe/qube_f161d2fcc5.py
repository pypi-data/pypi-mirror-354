import re
import os
import json
import stat
import importlib
import io, sys
import subprocess
import platform
import base64
import traceback
import uuid
import shutil
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime, timedelta
import pytz
UTC = pytz.utc
from asgiref.sync import sync_to_async
from spartaqube_app.path_mapper_obf import sparta_bff35427ab
from project.models_spartaqube import Notebook, NotebookShared
from project.models import ShareRights
from project.sparta_8688631f3d.sparta_355a680bf7 import qube_1d2a59f054 as qube_1d2a59f054
from project.sparta_8688631f3d.sparta_5d2f5154f8 import qube_c71ace27e3 as qube_c71ace27e3
from project.sparta_8688631f3d.sparta_577b784581.qube_2949549c51 import Connector as Connector
from project.sparta_8688631f3d.sparta_97c9232dca import qube_de58073131 as qube_de58073131
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_8f0cad92aa import sparta_226d9606de
from project.sparta_8688631f3d.sparta_9df5aeb023 import qube_4009e9a33a as qube_4009e9a33a
from project.sparta_8688631f3d.sparta_9df5aeb023 import qube_49f539b4d6 as qube_49f539b4d6
from project.sparta_8688631f3d.sparta_5149e63dd6.qube_0a8e8bbdab import sparta_8c5bc8c8c4
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_cdd2396883 import sparta_99859b53bb, sparta_f8e322f1b3
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


def sparta_789af5133c(project_path, has_django_models=True) ->dict:
    """
    Create a new notebook project
    """
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    dest_folder = project_path
    src_folder = os.path.join(sparta_bff35427ab()['django_app_template'],
        'notebook', 'template')
    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder, item)
        dest_path = os.path.join(dest_folder, item)
        if os.path.isdir(src_path):
            last_folder_name = os.path.basename(src_path)
            if last_folder_name == 'app':
                if not has_django_models:
                    continue
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
        else:
            filename = os.path.basename(src_path)
            if filename in ['notebook_models.py', 'models_access_examples.py']:
                if not has_django_models:
                    continue
            shutil.copy2(src_path, dest_path)
    return {'project_path': project_path}


def sparta_9173aba28c(json_data, user_obj) ->dict:
    """
    Validate project path 
    A valid project path is a folder that does not exists yet (and is valid in terms of expression)
    """
    project_path = json_data['projectPath']
    project_path = sparta_226d9606de(project_path)
    notebook_set = Notebook.objects.filter(project_path=project_path).all()
    if notebook_set.count() > 0:
        notebook_obj = notebook_set[0]
        user_groups = sparta_09abdd9532(user_obj)
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
        if not has_edit_rights:
            return {'res': -1, 'errorMsg':
                'Chose another path. A project already exists at this location'
                }
    if not isinstance(project_path, str):
        return {'res': -1, 'errorMsg': 'Project path must be a string.'}
    logger.debug('project_path')
    logger.debug(project_path)
    try:
        project_path = os.path.abspath(project_path)
    except Exception as e:
        return {'res': -1, 'errorMsg': f'Invalid project path: {str(e)}'}
    try:
        if not os.path.exists(project_path):
            os.makedirs(project_path)
        has_django_models = json_data['hasDjangoModels']
        notebook_path_infos_dict = sparta_789af5133c(project_path,
            has_django_models)
        project_path = notebook_path_infos_dict['project_path']
        return {'res': 1, 'project_path': project_path}
    except Exception as e:
        return {'res': -1, 'errorMsg': f'Failed to create folder: {str(e)}'}


def sparta_e1028ef450(json_data, user_obj) ->dict:
    """
    Validate project path init git
    """
    json_data['bAddGitignore'] = True
    json_data['bAddReadme'] = True
    return qube_49f539b4d6.sparta_c717238807(json_data, user_obj)


def sparta_c9cf4bc5fc(json_data, user_obj) ->dict:
    """
    Load notebook library: all my notebook view + the public (exposed) views
    """
    user_groups = sparta_09abdd9532(user_obj)
    if len(user_groups) > 0:
        notebook_shared_set = NotebookShared.objects.filter(Q(is_delete=0,
            user_group__in=user_groups, notebook__is_delete=0) | Q(
            is_delete=0, user=user_obj, notebook__is_delete=0) | Q(
            is_delete=0, notebook__is_delete=0,
            notebook__is_expose_notebook=True, notebook__is_public_notebook
            =True))
    else:
        notebook_shared_set = NotebookShared.objects.filter(Q(is_delete=0,
            user=user_obj, notebook__is_delete=0) | Q(is_delete=0,
            notebook__is_delete=0, notebook__is_expose_notebook=True,
            notebook__is_public_notebook=True))
    if notebook_shared_set.count() > 0:
        order_by_text = json_data.get('orderBy', 'Recently used')
        if order_by_text == 'Recently used':
            notebook_shared_set = notebook_shared_set.order_by(
                '-notebook__last_date_used')
        elif order_by_text == 'Date desc':
            notebook_shared_set = notebook_shared_set.order_by(
                '-notebook__last_update')
        elif order_by_text == 'Date asc':
            notebook_shared_set = notebook_shared_set.order_by(
                'notebook__last_update')
        elif order_by_text == 'Name desc':
            notebook_shared_set = notebook_shared_set.order_by(
                '-notebook__name')
        elif order_by_text == 'Name asc':
            notebook_shared_set = notebook_shared_set.order_by('notebook__name'
                )
    notebook_library_list = []
    for notebook_shared_obj in notebook_shared_set:
        notebook_obj = notebook_shared_obj.notebook
        share_rights_obj = notebook_shared_obj.share_rights
        last_update = None
        try:
            last_update = str(notebook_obj.last_update.strftime('%Y-%m-%d'))
        except:
            pass
        date_created = None
        try:
            date_created = str(notebook_obj.date_created.strftime('%Y-%m-%d'))
        except Exception as e:
            logger.debug(e)
        main_ipynb_fullpath = notebook_obj.main_ipynb_fullpath
        if main_ipynb_fullpath is None:
            main_ipynb_fullpath = os.path.join(notebook_obj.project_path,
                'main.ipynb')
        elif len(main_ipynb_fullpath) == 0:
            main_ipynb_fullpath = os.path.join(notebook_obj.project_path,
                'main.ipynb')
        notebook_library_list.append({'notebook_id': notebook_obj.notebook_id, 'name': notebook_obj.name, 'slug': notebook_obj.slug, 'description': notebook_obj.description,
            'is_expose_notebook': notebook_obj.is_expose_notebook,
            'has_password': notebook_obj.has_password,
            'main_ipynb_fullpath': main_ipynb_fullpath,
            'is_public_notebook': notebook_obj.is_public_notebook,
            'is_exec_code_display': notebook_obj.is_exec_code_display,
            'is_owner': notebook_shared_obj.is_owner, 'has_write_rights':
            share_rights_obj.has_write_rights, 'last_update': last_update,
            'date_created': date_created})
    return {'res': 1, 'notebook_library': notebook_library_list}


def sparta_21300c2395(json_data, user_obj) ->dict:
    """
    Load existing project for edit
    """
    notebook_id = json_data['notebookId']
    notebook_set = Notebook.objects.filter(notebook_id__startswith=
        notebook_id, is_delete=False).all()
    if notebook_set.count() == 1:
        notebook_obj = notebook_set[notebook_set.count() - 1]
        notebook_id = notebook_obj.notebook_id
        user_groups = sparta_09abdd9532(user_obj)
        if len(user_groups) > 0:
            notebook_shared_set = NotebookShared.objects.filter(Q(is_delete
                =0, user_group__in=user_groups, notebook__is_delete=0,
                notebook=notebook_obj) | Q(is_delete=0, user=user_obj,
                notebook__is_delete=0, notebook=notebook_obj))
        else:
            notebook_shared_set = NotebookShared.objects.filter(is_delete=0,
                user=user_obj, notebook__is_delete=0, notebook=notebook_obj)
        if notebook_shared_set.count() == 0:
            return {'res': -1, 'errorMsg':
                'You do not have the rights to access this project'}
    else:
        return {'res': -1, 'errorMsg': 'Project not found...'}
    notebook_shared_set = NotebookShared.objects.filter(is_owner=True,
        notebook=notebook_obj, user=user_obj)
    if notebook_shared_set.count() > 0:
        date_now = datetime.now().astimezone(UTC)
        notebook_obj.last_date_used = date_now
        notebook_obj.save()
    main_ipynb_fullpath = notebook_obj.main_ipynb_fullpath
    if main_ipynb_fullpath is None:
        main_ipynb_fullpath = os.path.join(notebook_obj.project_path,
            'main.ipynb')
    elif len(main_ipynb_fullpath) == 0:
        main_ipynb_fullpath = os.path.join(notebook_obj.project_path,
            'main.ipynb')
    return {'res': 1, 'notebook': {'basic': {'notebook_id': notebook_obj.notebook_id, 'name': notebook_obj.name, 'slug': notebook_obj.slug,
        'description': notebook_obj.description, 'is_expose_notebook':
        notebook_obj.is_expose_notebook, 'is_public_notebook': notebook_obj.is_public_notebook, 'is_exec_code_display': notebook_obj.is_exec_code_display, 'main_ipynb_fullpath': main_ipynb_fullpath,
        'has_password': notebook_obj.has_password, 'notebook_venv':
        notebook_obj.notebook_venv, 'project_path': notebook_obj.project_path}, 'lumino': {'lumino_layout': notebook_obj.lumino_layout}}
        }


def sparta_4692f94d12(json_data, user_obj) ->dict:
    """
    Load existing project for run mode
    """
    notebook_id = json_data['notebookId']
    logger.debug('load_notebook DEBUG')
    logger.debug(notebook_id)
    if not user_obj.is_anonymous:
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
                    notebook=notebook_obj) | Q(is_delete=0,
                    notebook__is_delete=0, notebook__is_expose_notebook=
                    True, notebook__is_public_notebook=True))
            else:
                notebook_shared_set = NotebookShared.objects.filter(Q(
                    is_delete=0, user=user_obj, notebook__is_delete=0,
                    notebook=notebook_obj) | Q(is_delete=0,
                    notebook__is_delete=0, notebook__is_expose_notebook=
                    True, notebook__is_public_notebook=True))
            if notebook_shared_set.count() == 0:
                return {'res': -1, 'errorMsg':
                    'You do not have the rights to access this project'}
        else:
            return {'res': -1, 'errorMsg': 'Project not found...'}
    else:
        password_notebook = json_data.get('modalPassword', None)
        logger.debug(f'DEBUG DEVELOPER VIEW TEST >>> {password_notebook}')
        notebook_access_dict = sparta_a96c3cc42e(notebook_id, user_obj,
            password_notebook=password_notebook)
        logger.debug('MODAL DEBUG DEBUG DEBUG notebook_access_dict')
        logger.debug(notebook_access_dict)
        if notebook_access_dict['res'] != 1:
            return {'res': notebook_access_dict['res'], 'errorMsg':
                notebook_access_dict['errorMsg']}
        notebook_obj = notebook_access_dict['notebook_obj']
    if not user_obj.is_anonymous:
        notebook_shared_set = NotebookShared.objects.filter(is_owner=True,
            notebook=notebook_obj, user=user_obj)
        if notebook_shared_set.count() > 0:
            date_now = datetime.now().astimezone(UTC)
            notebook_obj.last_date_used = date_now
            notebook_obj.save()
    main_ipynb_fullpath = notebook_obj.main_ipynb_fullpath
    if main_ipynb_fullpath is None:
        main_ipynb_fullpath = os.path.join(notebook_obj.project_path,
            'main.ipynb')
    elif len(main_ipynb_fullpath) == 0:
        main_ipynb_fullpath = os.path.join(notebook_obj.project_path,
            'main.ipynb')
    return {'res': 1, 'notebook': {'basic': {'notebook_id': notebook_obj.notebook_id, 'name': notebook_obj.name, 'slug': notebook_obj.slug,
        'description': notebook_obj.description, 'is_expose_notebook':
        notebook_obj.is_expose_notebook, 'is_public_notebook': notebook_obj.is_public_notebook, 'is_exec_code_display': notebook_obj.is_exec_code_display, 'has_password': notebook_obj.has_password,
        'notebook_venv': notebook_obj.notebook_venv, 'project_path':
        notebook_obj.project_path, 'main_ipynb_fullpath':
        main_ipynb_fullpath}, 'lumino': {'lumino_layout': notebook_obj.lumino_layout}}}


def sparta_1fd2210569(json_data, user_obj) ->dict:
    """
    Save notebook view
    """
    logger.debug('Save notebook')
    logger.debug(json_data)
    logger.debug(json_data.keys())
    is_new = json_data['isNew']
    if not is_new:
        return sparta_a15e77ffcd(json_data, user_obj)
    date_now = datetime.now().astimezone(UTC)
    notebook_id = str(uuid.uuid4())
    has_password = json_data['hasPassword']
    notebook_password = None
    if has_password:
        notebook_password = json_data['password']
        notebook_password = qube_c71ace27e3.sparta_b4548ea0cb(
            notebook_password)
    lumino_layout_dump = json_data['luminoLayout']
    notebook_name = json_data['name']
    notebook_description = json_data['description']
    project_path = json_data['projectPath']
    project_path = sparta_226d9606de(project_path)
    is_expose_notebook = json_data['isExpose']
    is_public_notebook = json_data['isPublic']
    has_password = json_data['hasPassword']
    is_exec_code_display = json_data['isExecCodeDisplay']
    notebook_venv = json_data.get('notebookVenv', None)
    slug = json_data['slug']
    if len(slug) == 0:
        slug = json_data['name']
    base_slug = slugify(slug)
    slug = base_slug
    counter = 1
    while Notebook.objects.filter(slug=slug).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1
    thumbnail_id = None
    image_data = json_data.get('previewImage', None)
    if image_data is not None:
        try:
            image_data = image_data.split(',')[1]
            image_binary = base64.b64decode(image_data)
            project_path = sparta_bff35427ab()['project']
            thumbnail_path = os.path.join(project_path, 'static',
                'thumbnail', 'notebook')
            os.makedirs(thumbnail_path, exist_ok=True)
            thumbnail_id = str(uuid.uuid4())
            file_path = os.path.join(thumbnail_path, f'{thumbnail_id}.png')
            with open(file_path, 'wb') as f:
                f.write(image_binary)
        except:
            pass
    notebook_obj = Notebook.objects.create(notebook_id=notebook_id, name=
        notebook_name, slug=slug, description=notebook_description,
        is_expose_notebook=is_expose_notebook, is_public_notebook=
        is_public_notebook, has_password=has_password, password_e=
        notebook_password, is_exec_code_display=is_exec_code_display,
        lumino_layout=lumino_layout_dump, project_path=project_path,
        notebook_venv=notebook_venv, thumbnail_path=thumbnail_id,
        date_created=date_now, last_update=date_now, last_date_used=
        date_now, spartaqube_version=sparta_8c5bc8c8c4())
    share_rights_obj = ShareRights.objects.create(is_admin=True,
        has_write_rights=True, has_reshare_rights=True, last_update=date_now)
    NotebookShared.objects.create(notebook=notebook_obj, user=user_obj,
        share_rights=share_rights_obj, is_owner=True, date_created=date_now)
    return {'res': 1, 'notebook_id': notebook_id}


def sparta_a15e77ffcd(json_data, user_obj) ->dict:
    """
    Update existing notebook
    """
    logger.debug('Save notebook update_notebook_view')
    logger.debug(json_data)
    logger.debug(json_data.keys())
    date_now = datetime.now().astimezone(UTC)
    notebook_id = json_data['notebookId']
    notebook_set = Notebook.objects.filter(notebook_id__startswith=
        notebook_id, is_delete=False).all()
    if notebook_set.count() == 1:
        notebook_obj = notebook_set[notebook_set.count() - 1]
        notebook_id = notebook_obj.notebook_id
        user_groups = sparta_09abdd9532(user_obj)
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
            lumino_layout_dump = json_data['luminoLayout']
            notebook_name = json_data['name']
            notebook_description = json_data['description']
            is_expose_notebook = json_data['isExpose']
            is_public_notebook = json_data['isPublic']
            has_password = json_data['hasPassword']
            is_exec_code_display = json_data['isExecCodeDisplay']
            slug = json_data['slug']
            if notebook_obj.slug != slug:
                if len(slug) == 0:
                    slug = json_data['name']
                base_slug = slugify(slug)
                slug = base_slug
                counter = 1
                while Notebook.objects.filter(slug=slug).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
            thumbnail_id = None
            image_data = json_data.get('previewImage', None)
            if image_data is not None:
                image_data = image_data.split(',')[1]
                image_binary = base64.b64decode(image_data)
                try:
                    project_path = sparta_bff35427ab()['project']
                    thumbnail_path = os.path.join(project_path, 'static',
                        'thumbnail', 'notebook')
                    os.makedirs(thumbnail_path, exist_ok=True)
                    if notebook_obj.thumbnail_path is None:
                        thumbnail_id = str(uuid.uuid4())
                    else:
                        thumbnail_id = notebook_obj.thumbnail_path
                    file_path = os.path.join(thumbnail_path,
                        f'{thumbnail_id}.png')
                    with open(file_path, 'wb') as f:
                        f.write(image_binary)
                except:
                    pass
            logger.debug('lumino_layout_dump')
            logger.debug(lumino_layout_dump)
            logger.debug(type(lumino_layout_dump))
            notebook_obj.name = notebook_name
            notebook_obj.description = notebook_description
            notebook_obj.slug = slug
            notebook_obj.is_expose_notebook = is_expose_notebook
            notebook_obj.is_public_notebook = is_public_notebook
            notebook_obj.is_exec_code_display = is_exec_code_display
            notebook_obj.thumbnail_path = thumbnail_id
            notebook_obj.lumino_layout = lumino_layout_dump
            notebook_obj.last_update = date_now
            notebook_obj.last_date_used = date_now
            if has_password:
                notebook_password = json_data['password']
                if len(notebook_password) > 0:
                    notebook_password = (qube_c71ace27e3.sparta_b4548ea0cb(notebook_password))
                    notebook_obj.password_e = notebook_password
                    notebook_obj.has_password = True
            else:
                notebook_obj.has_password = False
            notebook_obj.save()
    return {'res': 1, 'notebook_id': notebook_id}


def sparta_e76a04905d(json_data, user_obj) ->dict:
    """
    This function saves the lumino layout
    """
    notebook_id = json_data['notebookId']
    notebook_set = Notebook.objects.filter(notebook_id__startswith=
        notebook_id, is_delete=False).all()
    if notebook_set.count() == 1:
        notebook_obj = notebook_set[notebook_set.count() - 1]
        notebook_id = notebook_obj.notebook_id
        user_groups = sparta_09abdd9532(user_obj)
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
            lumino_layout_dump = json_data['luminoLayout']
            notebook_obj.lumino_layout = lumino_layout_dump
            notebook_obj.save()
    return {'res': 1}


def sparta_20b2b796b9(json_data, user_obj) ->dict:
    """
    Delete notebook
    """
    notebook_id = json_data['notebookId']
    notebook_set = Notebook.objects.filter(notebook_id=notebook_id,
        is_delete=False).all()
    if notebook_set.count() > 0:
        notebook_obj = notebook_set[notebook_set.count() - 1]
        user_groups = sparta_09abdd9532(user_obj)
        if len(user_groups) > 0:
            notebook_shared_set = NotebookShared.objects.filter(Q(is_delete
                =0, user_group__in=user_groups, notebook__is_delete=0,
                notebook=notebook_obj) | Q(is_delete=0, user=user_obj,
                notebook__is_delete=0, notebook=notebook_obj))
        else:
            notebook_shared_set = NotebookShared.objects.filter(is_delete=0,
                user=user_obj, notebook__is_delete=0, notebook=notebook_obj)
        if notebook_shared_set.count() > 0:
            notebook_shared_obj = notebook_shared_set[0]
            notebook_shared_obj.is_delete = True
            notebook_shared_obj.save()
    return {'res': 1}


def sparta_a96c3cc42e(notebook_id, user_obj, password_notebook=None) ->dict:
    """
    Check if user can access develoepr view (read only).res: 
        1  Can access notebook view
        2  No access, require password (missing password)
        3  No access, wrong password
       -1  Not allowed, redirect to login   
    """
    logger.debug('notebook_id')
    logger.debug(notebook_id)
    notebook_set = Notebook.objects.filter(notebook_id__startswith=
        notebook_id, is_delete=False).all()
    b_found = False
    if notebook_set.count() == 1:
        b_found = True
    else:
        this_slug = notebook_id
        notebook_set = Notebook.objects.filter(slug__startswith=this_slug,
            is_delete=False).all()
        if notebook_set.count() == 1:
            b_found = True
    logger.debug('b_found')
    logger.debug(b_found)
    if b_found:
        notebook_obj = notebook_set[notebook_set.count() - 1]
        has_password = notebook_obj.has_password
        if notebook_obj.is_expose_notebook:
            logger.debug('is exposed')
            if notebook_obj.is_public_notebook:
                logger.debug('is public')
                if not has_password:
                    logger.debug('no password')
                    return {'res': 1, 'notebook_obj': notebook_obj}
                else:
                    logger.debug('hass password')
                    if password_notebook is None:
                        logger.debug('empty passord provided')
                        return {'res': 2, 'errorMsg': 'Require password',
                            'notebook_obj': notebook_obj}
                    else:
                        try:
                            if qube_c71ace27e3.sparta_5b66dfafff(
                                notebook_obj.password_e) == password_notebook:
                                return {'res': 1, 'notebook_obj': notebook_obj}
                            else:
                                return {'res': 3, 'errorMsg':
                                    'Invalid password', 'notebook_obj':
                                    notebook_obj}
                        except Exception as e:
                            return {'res': 3, 'errorMsg':
                                'Invalid password', 'notebook_obj':
                                notebook_obj}
            elif user_obj.is_authenticated:
                user_groups = sparta_09abdd9532(user_obj)
                if len(user_groups) > 0:
                    notebook_shared_set = NotebookShared.objects.filter(Q(
                        is_delete=0, user_group__in=user_groups,
                        notebook__is_delete=0, notebook=notebook_obj) | Q(
                        is_delete=0, user=user_obj, notebook__is_delete=0,
                        notebook=notebook_obj))
                else:
                    notebook_shared_set = NotebookShared.objects.filter(
                        is_delete=0, user=user_obj, notebook__is_delete=0,
                        notebook=notebook_obj)
                if notebook_shared_set.count() > 0:
                    return {'res': 1, 'notebook_obj': notebook_obj}
            else:
                return {'res': -1, 'debug': 1}
    return {'res': -1, 'debug': 2}


def sparta_7a4ac4f59b(json_data, user_obj) ->dict:
    """
    Open a folder in VSCode."""
    folder_path = sparta_226d9606de(json_data['projectPath'])
    return sparta_99859b53bb(folder_path)


def sparta_b932e17af7(json_data, user_obj) ->dict:
    """
    Open terminal 
    """
    path = sparta_226d9606de(json_data['projectPath'])
    return sparta_f8e322f1b3(path)


def sparta_5992183baf(json_data, user_obj) ->dict:
    """
    Change notebook entrypoint (ipynb)
    """
    logger.debug('notebook_ipynb_set_entrypoint json_data')
    logger.debug(json_data)
    notebook_id = json_data['notebookId']
    notebook_set = Notebook.objects.filter(notebook_id__startswith=
        notebook_id, is_delete=False).all()
    if notebook_set.count() == 1:
        notebook_obj = notebook_set[notebook_set.count() - 1]
        notebook_id = notebook_obj.notebook_id
        user_groups = sparta_09abdd9532(user_obj)
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
            main_ipynb_fullpath = sparta_226d9606de(json_data['fullPath'])
            notebook_obj.main_ipynb_fullpath = main_ipynb_fullpath
            notebook_obj.save()
    return {'res': 1}


async def notebook_permission_code_exec_DEPREC(json_data):
    """
    Check for readonly permission and make sure the user is not trying to execute a different code than 
    the notebook cell id
    """
    logger.debug('Callilng notebook_permission_code_exec')
    try:
        notebook_id = json_data['notebookId']
        notebook_set = Notebook.objects.filter(notebook_id__startswith=
            notebook_id, is_delete=False)
        if await notebook_set.acount() > 0:
            notebook_obj = await notebook_set.afirst()
            cell_id = json_data['cellId']
            full_path = notebook_obj.main_ipynb_fullpath
            if full_path is None:
                full_path = os.path.join(notebook_obj.project_path,
                    'main.ipynb')
            ipynb_dict = qube_4009e9a33a.sparta_1dbf0a0a23(full_path)
            cells = ipynb_dict['cells']
            for cell_dict in cells:
                sq_metadata = json.loads(cell_dict['metadata']['sqMetadata'])
                if sq_metadata['cellId'] == cell_id:
                    logger.debug('Found Cell Code')
                    logger.debug(cell_dict['source'][0])
                    return cell_dict['source'][0]
    except Exception as e:
        logger.debug('Except is:')
        logger.debug(e)
        return ''
    return ''


async def notebook_permission_code_exec(json_data):
    """
    Check for readonly permission and make sure the user is not trying to execute a different code than 
    the notebook cell id
    """
    logger.debug('Calling notebook_permission_code_exec')
    try:
        notebook_id = json_data['notebookId']
        notebook_set = await sync_to_async(lambda : list(Notebook.objects.filter(notebook_id__startswith=notebook_id, is_delete=False)),
            thread_sensitive=False)()
        if len(notebook_set) > 0:
            notebook_obj = notebook_set[0]
            cell_id = json_data['cellId']
            full_path = notebook_obj.main_ipynb_fullpath
            if full_path is None:
                full_path = os.path.join(notebook_obj.project_path,
                    'main.ipynb')
            ipynb_dict = qube_4009e9a33a.sparta_1dbf0a0a23(full_path)
            cells = ipynb_dict['cells']
            for cell_dict in cells:
                sq_metadata = json.loads(cell_dict['metadata']['sqMetadata'])
                if sq_metadata['cellId'] == cell_id:
                    logger.debug('Found Cell Code')
                    logger.debug(cell_dict['source'][0])
                    return cell_dict['source'][0]
    except Exception as e:
        logger.debug('Exception in notebook_permission_code_exec:')
        logger.debug(e)
        return ''
    return ''


def sparta_235752a8ff(json_data, user_obj) ->dict:
    """
    Copy template
    """


from django.core.management import call_command
from io import StringIO


def sparta_cc92b98ec1(project_path, python_executable='python'):
    """
    Checks for pending migrations by running the manage.py makemigrations command
    in a separate subprocess.Args:
        project_path (str): The path to the Django project directory.python_executable (str): The Python executable to use (default: "python").Returns:
        tuple: (bool, str)
            - bool: True if migrations are needed, False otherwise.- str: The combined stdout and stderr from the makemigrations command."""
    has_error = False
    try:
        manage_py_path = os.path.join(project_path, 'manage.py')
        if not os.path.exists(manage_py_path):
            has_error = True
            return (False, f'Error: manage.py not found in {project_path}',
                has_error)
        env = os.environ.copy()
        env['DJANGO_SETTINGS_MODULE'] = 'app.settings'
        python_executable = sys.executable
        command = [python_executable, 'manage.py', 'makemigrations',
            '--dry-run']
        result = subprocess.run(command, cwd=project_path, text=True,
            capture_output=True, env=env)
        if result.returncode != 0:
            has_error = True
            return False, f'Error: {result.stderr}', has_error
        stdout = result.stdout
        is_migration_needed = 'No changes detected' not in stdout
        return is_migration_needed, stdout, has_error
    except FileNotFoundError as e:
        has_error = True
        return (False,
            f'Error: {e}. Ensure the correct Python executable and project path.'
            , has_error)
    except Exception as e:
        has_error = True
        return False, str(e), has_error


def sparta_c93233a885():
    virtual_env = os.environ.get('VIRTUAL_ENV')
    if virtual_env:
        return virtual_env
    else:
        return sys.prefix


def sparta_9c21ea78db():
    """Gets the path to the pip executable in a platform-independent way."""
    env_path = sparta_c93233a885()
    if sys.platform == 'win32':
        pip_path = os.path.join(env_path, 'Scripts', 'pip.exe')
    else:
        pip_path = os.path.join(env_path, 'bin', 'pip')
    return pip_path


def sparta_2e9e01f9ce(json_data, user_obj) ->dict:
    """
    Init django (case where Django is not installed at the creation of the project but after using the button the right panel section)
    """
    project_path = sparta_226d9606de(json_data['projectPath'])
    dest_path = project_path
    src_path = os.path.join(sparta_bff35427ab()['django_app_template'],
        'notebook', 'template')
    dest_app_path = os.path.join(dest_path, 'app')
    if not os.path.exists(dest_app_path):
        os.makedirs(dest_app_path)
    shutil.copytree(os.path.join(src_path, 'app'), dest_app_path,
        dirs_exist_ok=True)
    logger.debug(f'Folder copied from {src_path} to {dest_path}')
    shutil.copy2(os.path.join(src_path, 'notebook_models.py'), dest_path)
    shutil.copy2(os.path.join(src_path, 'models_access_examples.py'), dest_path
        )
    return {'res': 1}


def sparta_45a0b50ce9(json_data, user_obj) ->dict:
    """
    Return if there are pending model migrations
    """
    path = sparta_226d9606de(json_data['projectPath'])
    path = os.path.join(path, 'app')
    is_migration_needed, stdout, has_error = sparta_cc92b98ec1(path)
    has_django_init = True
    res = 1
    error_msg = ''
    if has_error:
        res = -1
        error_msg = stdout
        has_django_init
        manage_py_path = os.path.join(path, 'manage.py')
        if not os.path.exists(manage_py_path):
            has_django_init = False
    res_dict = {'res': res, 'has_error': has_error,
        'has_pending_migrations': is_migration_needed, 'stdout': stdout,
        'errorMsg': error_msg, 'has_django_init': has_django_init}
    return res_dict


def sparta_10401142d3(project_path, python_executable='python'):
    """
    Makes and applies migrations in a Django project by running the manage.py makemigrations
    and migrate commands in subprocesses.Args:
        project_path (str): Path to the target Django project directory.settings_module (str): The settings module for the target Django project.python_executable (str): Path to the Python executable for the target project.Returns:
        tuple: (bool, str)
            - bool: True if migrations were made and applied successfully, False otherwise.- str: The combined stdout and stderr from the commands."""
    try:
        manage_py_path = os.path.join(project_path, 'manage.py')
        if not os.path.exists(manage_py_path):
            return False, f'Error: manage.py not found in {project_path}'
        env = os.environ.copy()
        env['DJANGO_SETTINGS_MODULE'] = 'app.settings'
        python_executable = sys.executable
        commands = [[python_executable, 'manage.py', 'makemigrations'], [
            python_executable, 'manage.py', 'migrate']]
        output = []
        for command in commands:
            result = subprocess.run(command, cwd=project_path, text=True,
                capture_output=True, env=env)
            if result.stdout is not None:
                if len(str(result.stdout)) > 0:
                    output.append(result.stdout)
            if result.stderr is not None:
                if len(str(result.stderr)) > 0:
                    output.append(
                        f"<span style='color:red'>Stderr:\n{result.stderr}</span>"
                        )
            if result.returncode != 0:
                return False, '\n'.join(output)
        return True, '\n'.join(output)
    except FileNotFoundError as e:
        return (False,
            f'Error: {e}. Ensure the correct Python executable and project path.'
            )
    except Exception as e:
        return False, str(e)


def sparta_359bdb818f(json_data, user_obj) ->dict:
    """
    Migrate (apply makemigrations and migrate) django migrations
    """
    path = sparta_226d9606de(json_data['projectPath'])
    path = os.path.join(path, 'app')
    res_migration, stdout = sparta_10401142d3(path)
    res = 1
    errorMsg = ''
    if not res_migration:
        res = -1
        errorMsg = stdout
    return {'res': res, 'res_migration': res_migration, 'stdout': stdout,
        'errorMsg': errorMsg}


def sparta_b62a2ecf07(json_data, user_obj) ->dict:
    """
    
    """
    return {'res': 1}


def sparta_e657caef2c(json_data, user_obj) ->dict:
    """
    
    """
    return {'res': 1}

#END OF QUBE
