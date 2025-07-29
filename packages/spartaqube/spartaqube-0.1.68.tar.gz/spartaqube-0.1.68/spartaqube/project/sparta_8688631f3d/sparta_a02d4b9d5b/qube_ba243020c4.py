import os, sys
import gc
import json
import base64
import shutil
import zipfile
import io
import uuid
import subprocess
import cloudpickle
import platform
import getpass
from django.conf import settings
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime, timedelta
from pathlib import Path
from dateutil import parser
import pytz
UTC = pytz.utc
from django.contrib.humanize.templatetags.humanize import naturalday
from project.sparta_8688631f3d.sparta_355a680bf7 import qube_1d2a59f054 as qube_1d2a59f054
from project.models_spartaqube import Kernel, KernelShared, ShareRights
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_8f0cad92aa import sparta_226d9606de, sparta_244cea0b2a
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_f0d228f17a import sparta_ca71f9cc05
from project.sparta_8688631f3d.sparta_34d32fb8c6.qube_cbe6ad2077 import sparta_4bb56d08cd, sparta_5fddc0f473, sparta_bed904ab12, sparta_fae256f2cf
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_cdd2396883 import sparta_99859b53bb, sparta_f8e322f1b3
from project.sparta_8688631f3d.sparta_5149e63dd6.qube_0a8e8bbdab import sparta_8c5bc8c8c4
from project.logger_config import logger


def sparta_d30ed822f7():
    spartaqube_volume_path = sparta_ca71f9cc05()
    default_project_path = os.path.join(spartaqube_volume_path, 'kernel')
    return default_project_path


def sparta_09abdd9532(user_obj) ->list:
    """
    
    """
    user_group_set = qube_1d2a59f054.sparta_1c22139619(user_obj)
    if len(user_group_set) > 0:
        user_groups = [this_obj.user_group for this_obj in user_group_set]
    else:
        user_groups = []
    return user_groups


def sparta_82334cb8e4(user_obj, kernel_manager_uuid) ->list:
    """
    This function returns the kernel cloudpickle + the list of not pickleable variables
    """
    from project.sparta_8688631f3d.sparta_2a93ddec7a import qube_4aa09eb72d as qube_4aa09eb72d
    kernel_process_obj = qube_4aa09eb72d.sparta_1b457f9dcf(user_obj,
        kernel_manager_uuid)
    res_dict = qube_4aa09eb72d.sparta_c31e868dba(
        kernel_process_obj)
    logger.debug('get_cloudpickle_kernel_variables res_dict')
    logger.debug(res_dict)
    kernel_cpkl_picklable = res_dict['picklable']
    logger.debug('kernel_cpkl_picklable')
    logger.debug(type(kernel_cpkl_picklable))
    logger.debug("res_dict['unpicklable']")
    logger.debug(type(res_dict['unpicklable']))
    kernel_cpkl_unpicklable = cloudpickle.loads(res_dict['unpicklable'])
    logger.debug('kernel_cpkl_unpicklable')
    logger.debug(type(kernel_cpkl_unpicklable))
    return kernel_cpkl_picklable, kernel_cpkl_unpicklable


def sparta_930a02b3af(user_obj) ->list:
    """
    Load kernels library (offline kernel)
    """
    default_kernel_path = sparta_d30ed822f7()
    user_groups = sparta_09abdd9532(user_obj)
    if len(user_groups) > 0:
        kernel_shared_set = KernelShared.objects.filter(Q(is_delete=0,
            user_group__in=user_groups, kernel__is_delete=0) | Q(is_delete=
            0, user=user_obj, kernel__is_delete=0))
    else:
        kernel_shared_set = KernelShared.objects.filter(Q(is_delete=0, user
            =user_obj, kernel__is_delete=0))
    if kernel_shared_set.count() > 0:
        kernel_shared_set = kernel_shared_set.order_by('-kernel__last_update')
    kernel_library_list = []
    for kernel_shared_obj in kernel_shared_set:
        kernel_obj = kernel_shared_obj.kernel
        share_rights_obj = kernel_shared_obj.share_rights
        last_update = None
        try:
            last_update = str(kernel_obj.last_update.strftime('%Y-%m-%d'))
        except:
            pass
        date_created = None
        try:
            date_created = str(kernel_obj.date_created.strftime('%Y-%m-%d'))
        except Exception as e:
            logger.debug(e)
        main_ipynb_fullpath = os.path.join(default_kernel_path, kernel_obj.kernel_manager_uuid, 'main.ipynb')
        kernel_library_list.append({'kernel_manager_uuid': kernel_obj.kernel_manager_uuid, 'name': kernel_obj.name, 'slug':
            kernel_obj.slug, 'description': kernel_obj.description,
            'main_ipynb_fullpath': main_ipynb_fullpath, 'kernel_size':
            kernel_obj.kernel_size, 'has_write_rights': share_rights_obj.has_write_rights, 'last_update': last_update, 'date_created':
            date_created})
    return kernel_library_list


def sparta_8a4abdd59a(user_obj) ->list:
    """
    Get stored kernels
    """
    user_groups = sparta_09abdd9532(user_obj)
    if len(user_groups) > 0:
        kernel_shared_set = KernelShared.objects.filter(Q(is_delete=0,
            user_group__in=user_groups, kernel__is_delete=0) | Q(is_delete=
            0, user=user_obj, kernel__is_delete=0))
    else:
        kernel_shared_set = KernelShared.objects.filter(Q(is_delete=0, user
            =user_obj, kernel__is_delete=0))
    if kernel_shared_set.count() > 0:
        kernel_shared_set = kernel_shared_set.order_by('-kernel__last_update')
        return [kernel_shared_obj.kernel.kernel_manager_uuid for
            kernel_shared_obj in kernel_shared_set]
    return []


def sparta_5c59e02c10(user_obj, kernel_manager_uuid) ->Kernel:
    """
    Return kernel model
    """
    kernel_set = Kernel.objects.filter(kernel_manager_uuid=kernel_manager_uuid
        ).all()
    if kernel_set.count() > 0:
        kernel_obj = kernel_set[0]
        user_groups = sparta_09abdd9532(user_obj)
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
            return kernel_obj
    return None


def sparta_cac94c49bc(json_data, user_obj) ->dict:
    """
    Load kernel notebook
    """
    from project.sparta_8688631f3d.sparta_2a93ddec7a import qube_4aa09eb72d as qube_4aa09eb72d
    kernel_manager_uuid = json_data['kernelManagerUUID']
    kernel_process_obj = qube_4aa09eb72d.sparta_1b457f9dcf(user_obj,
        kernel_manager_uuid)
    if kernel_process_obj is None:
        return {'res': -1, 'errorMsg': 'Kernel not found'}
    default_project_path = sparta_d30ed822f7()
    ipynb_full_path = os.path.join(default_project_path,
        kernel_manager_uuid, 'main.ipynb')
    venv_name = kernel_process_obj.venv_name
    lumino_layout = None
    is_kernel_saved = False
    is_static_variables = False
    kernel_mode_obj = sparta_5c59e02c10(user_obj, kernel_manager_uuid)
    if kernel_mode_obj is not None:
        is_kernel_saved = True
        lumino_layout = kernel_mode_obj.lumino_layout
        is_static_variables = kernel_mode_obj.is_static_variables
    return {'res': 1, 'kernel': {'basic': {'is_kernel_saved':
        is_kernel_saved, 'is_static_variables': is_static_variables,
        'kernel_manager_uuid': kernel_manager_uuid, 'name':
        kernel_process_obj.name, 'kernel_venv': venv_name, 'kernel_type':
        kernel_process_obj.type, 'project_path': default_project_path,
        'main_ipynb_fullpath': ipynb_full_path}, 'lumino': {'lumino_layout':
        lumino_layout}}}


def sparta_5cb3e736bc(json_data, user_obj) ->dict:
    """
    Save kernel notebook
    """
    logger.debug('Save notebook')
    logger.debug(json_data)
    logger.debug(json_data.keys())
    is_kernel_saved = json_data['isKernelSaved']
    if is_kernel_saved:
        return sparta_f638552baa(json_data, user_obj)
    date_now = datetime.now().astimezone(UTC)
    kernel_manager_uuid = json_data['kernelManagerUUID']
    lumino_layout_dump = json_data['luminoLayout']
    kernel_name = json_data['name']
    kernel_description = json_data['description']
    project_path = sparta_d30ed822f7()
    project_path = sparta_226d9606de(project_path)
    is_static_variables = json_data['is_static_variables']
    kernel_venv = json_data.get('kernelVenv', None)
    kernel_size = json_data.get('kernelSize', 0)
    slug = json_data.get('slug', '')
    if len(slug) == 0:
        slug = json_data['name']
    base_slug = slugify(slug)
    slug = base_slug
    counter = 1
    while Kernel.objects.filter(slug=slug).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1
    kernel_cpkl_picklable = None
    kernel_cpkl_unpicklable = []
    if is_static_variables:
        kernel_cpkl_picklable, kernel_cpkl_unpicklable = (
            sparta_82334cb8e4(user_obj, kernel_manager_uuid))
    kernel_obj = Kernel.objects.create(kernel_manager_uuid=
        kernel_manager_uuid, name=kernel_name, slug=slug, description=
        kernel_description, is_static_variables=is_static_variables,
        lumino_layout=lumino_layout_dump, project_path=project_path,
        kernel_venv=kernel_venv, kernel_variables=kernel_cpkl_picklable,
        kernel_size=kernel_size, date_created=date_now, last_update=
        date_now, last_date_used=date_now, spartaqube_version=
        sparta_8c5bc8c8c4())
    share_rights_obj = ShareRights.objects.create(is_admin=True,
        has_write_rights=True, has_reshare_rights=True, last_update=date_now)
    KernelShared.objects.create(kernel=kernel_obj, user=user_obj,
        share_rights=share_rights_obj, is_owner=True, date_created=date_now)
    logger.debug('kernel_cpkl_unpicklable')
    logger.debug(kernel_cpkl_unpicklable)
    return {'res': 1, 'unpicklable': kernel_cpkl_unpicklable}


def sparta_f638552baa(json_data, user_obj) ->dict:
    """
    Update existing kernel
    """
    logger.debug('update_kernel_notebook')
    logger.debug(json_data)
    kernel_manager_uuid = json_data['kernelManagerUUID']
    kernel_mode_obj = sparta_5c59e02c10(user_obj, kernel_manager_uuid)
    if kernel_mode_obj is not None:
        date_now = datetime.now().astimezone(UTC)
        kernel_manager_uuid = json_data['kernelManagerUUID']
        lumino_layout_dump = json_data['luminoLayout']
        kernel_name = json_data['name']
        kernel_description = json_data['description']
        is_static_variables = json_data['is_static_variables']
        kernel_venv = json_data.get('kernelVenv', None)
        kernel_size = json_data.get('kernelSize', 0)
        slug = json_data.get('slug', '')
        if len(slug) == 0:
            slug = json_data['name']
        base_slug = slugify(slug)
        slug = base_slug
        counter = 1
        while Kernel.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        is_static_variables = json_data['is_static_variables']
        kernel_cpkl_picklable = None
        kernel_cpkl_unpicklable = []
        if is_static_variables:
            kernel_cpkl_picklable, kernel_cpkl_unpicklable = (
                sparta_82334cb8e4(user_obj, kernel_manager_uuid))
        kernel_mode_obj.name = kernel_name
        kernel_mode_obj.description = kernel_description
        kernel_mode_obj.slug = slug
        kernel_mode_obj.kernel_venv = kernel_venv
        kernel_mode_obj.kernel_size = kernel_size
        kernel_mode_obj.is_static_variables = is_static_variables
        kernel_mode_obj.kernel_variables = kernel_cpkl_picklable
        kernel_mode_obj.lumino_layout = lumino_layout_dump
        kernel_mode_obj.last_update = date_now
        kernel_mode_obj.save()
    return {'res': 1, 'unpicklable': kernel_cpkl_unpicklable}


def sparta_91ff29005f(json_data, user_obj) ->dict:
    """
    Save kernel notebook workspace
    """
    pass


def sparta_b14ac600f8(json_data, user_obj) ->dict:
    """
    Open a folder in VSCode."""
    folder_path = sparta_226d9606de(json_data['projectPath'])
    return sparta_99859b53bb(folder_path)


def sparta_d66b17f7e6(json_data, user_obj) ->dict:
    """
    Kernel open terminal
    """
    path = sparta_226d9606de(json_data['projectPath'])
    return sparta_f8e322f1b3(path)


def sparta_7c89830996(json_data, user_obj) ->dict:
    """
    Save lumino layout
    """
    logger.debug('SAVE LYUMINO LAYOUT KERNEL NOTEBOOK')
    logger.debug('json_data')
    logger.debug(json_data)
    kernel_manager_uuid = json_data['kernelManagerUUID']
    kernel_set = Kernel.objects.filter(kernel_manager_uuid=kernel_manager_uuid
        ).all()
    if kernel_set.count() > 0:
        kernel_obj = kernel_set[0]
        user_groups = sparta_09abdd9532(user_obj)
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
            lumino_layout_dump = json_data['luminoLayout']
            kernel_obj.lumino_layout = lumino_layout_dump
            kernel_obj.save()
    return {'res': 1}


def sparta_2eb7776c05(json_data, user_obj) ->dict:
    """
    Get kernel size
    """
    from project.sparta_8688631f3d.sparta_2a93ddec7a import qube_4aa09eb72d as qube_4aa09eb72d
    kernel_manager_uuid = json_data['kernelManagerUUID']
    kernel_process_obj = qube_4aa09eb72d.sparta_1b457f9dcf(user_obj,
        kernel_manager_uuid)
    if kernel_process_obj is not None:
        kernel_size = qube_4aa09eb72d.sparta_c4f6e3590c(kernel_process_obj)
        return {'res': 1, 'kernel_size': kernel_size}
    return {'res': -1}


def sparta_0c069090bb(json_data, user_obj) ->dict:
    """
    Delete kernel
    """
    kernel_manager_uuid = json_data['kernelManagerUUID']
    kernel_mode_obj = sparta_5c59e02c10(user_obj, kernel_manager_uuid)
    if kernel_mode_obj is not None:
        kernel_mode_obj.is_delete = True
        kernel_mode_obj.save()
    return {'res': 1}

#END OF QUBE
