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
from project.sparta_8345d6a892.sparta_87f32c6e97 import qube_93b4ab09a2 as qube_93b4ab09a2
from project.models_spartaqube import Kernel, KernelShared, ShareRights
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import sparta_ad557db230, sparta_91bd932e94
from project.sparta_8345d6a892.sparta_952c41e91e.qube_ef9e4f9eb1 import sparta_9c89cfd808
from project.sparta_8345d6a892.sparta_f1a366f59f.qube_137201374c import sparta_8fe31d66cd, sparta_374e43cb4b, sparta_8c77512101, sparta_8c10b3eae6
from project.sparta_8345d6a892.sparta_952c41e91e.qube_7b0846f3f9 import sparta_e6a027bd1e, sparta_7d51b73540
from project.sparta_8345d6a892.sparta_707f379a9b.qube_43327fe104 import sparta_8d863c145d
from project.logger_config import logger


def sparta_9391dcc3d7():
    spartaqube_volume_path = sparta_9c89cfd808()
    default_project_path = os.path.join(spartaqube_volume_path, 'kernel')
    return default_project_path


def sparta_bcefba0d6f(user_obj) ->list:
    """
    
    """
    user_group_set = qube_93b4ab09a2.sparta_b0ee4cd292(user_obj)
    if len(user_group_set) > 0:
        user_groups = [this_obj.user_group for this_obj in user_group_set]
    else:
        user_groups = []
    return user_groups


def sparta_eb1f839cdd(user_obj, kernel_manager_uuid) ->list:
    """
    This function returns the kernel cloudpickle + the list of not pickleable variables
    """
    from project.sparta_8345d6a892.sparta_490625ab5b import qube_0c12c56358 as qube_0c12c56358
    kernel_process_obj = qube_0c12c56358.sparta_a5c947582d(user_obj,
        kernel_manager_uuid)
    res_dict = qube_0c12c56358.sparta_25e041278f(
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


def sparta_7ad66911af(user_obj) ->list:
    """
    Load kernels library (offline kernel)
    """
    default_kernel_path = sparta_9391dcc3d7()
    user_groups = sparta_bcefba0d6f(user_obj)
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


def sparta_43ea349d81(user_obj) ->list:
    """
    Get stored kernels
    """
    user_groups = sparta_bcefba0d6f(user_obj)
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


def sparta_3a64b1186a(user_obj, kernel_manager_uuid) ->Kernel:
    """
    Return kernel model
    """
    kernel_set = Kernel.objects.filter(kernel_manager_uuid=kernel_manager_uuid
        ).all()
    if kernel_set.count() > 0:
        kernel_obj = kernel_set[0]
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
            return kernel_obj
    return None


def sparta_9068c9e355(json_data, user_obj) ->dict:
    """
    Load kernel notebook
    """
    from project.sparta_8345d6a892.sparta_490625ab5b import qube_0c12c56358 as qube_0c12c56358
    kernel_manager_uuid = json_data['kernelManagerUUID']
    kernel_process_obj = qube_0c12c56358.sparta_a5c947582d(user_obj,
        kernel_manager_uuid)
    if kernel_process_obj is None:
        return {'res': -1, 'errorMsg': 'Kernel not found'}
    default_project_path = sparta_9391dcc3d7()
    ipynb_full_path = os.path.join(default_project_path,
        kernel_manager_uuid, 'main.ipynb')
    venv_name = kernel_process_obj.venv_name
    lumino_layout = None
    is_kernel_saved = False
    is_static_variables = False
    kernel_mode_obj = sparta_3a64b1186a(user_obj, kernel_manager_uuid)
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


def sparta_ac9d03f6ee(json_data, user_obj) ->dict:
    """
    Save kernel notebook
    """
    logger.debug('Save notebook')
    logger.debug(json_data)
    logger.debug(json_data.keys())
    is_kernel_saved = json_data['isKernelSaved']
    if is_kernel_saved:
        return sparta_4dfaa70bbd(json_data, user_obj)
    date_now = datetime.now().astimezone(UTC)
    kernel_manager_uuid = json_data['kernelManagerUUID']
    lumino_layout_dump = json_data['luminoLayout']
    kernel_name = json_data['name']
    kernel_description = json_data['description']
    project_path = sparta_9391dcc3d7()
    project_path = sparta_ad557db230(project_path)
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
            sparta_eb1f839cdd(user_obj, kernel_manager_uuid))
    kernel_obj = Kernel.objects.create(kernel_manager_uuid=
        kernel_manager_uuid, name=kernel_name, slug=slug, description=
        kernel_description, is_static_variables=is_static_variables,
        lumino_layout=lumino_layout_dump, project_path=project_path,
        kernel_venv=kernel_venv, kernel_variables=kernel_cpkl_picklable,
        kernel_size=kernel_size, date_created=date_now, last_update=
        date_now, last_date_used=date_now, spartaqube_version=
        sparta_8d863c145d())
    share_rights_obj = ShareRights.objects.create(is_admin=True,
        has_write_rights=True, has_reshare_rights=True, last_update=date_now)
    KernelShared.objects.create(kernel=kernel_obj, user=user_obj,
        share_rights=share_rights_obj, is_owner=True, date_created=date_now)
    logger.debug('kernel_cpkl_unpicklable')
    logger.debug(kernel_cpkl_unpicklable)
    return {'res': 1, 'unpicklable': kernel_cpkl_unpicklable}


def sparta_4dfaa70bbd(json_data, user_obj) ->dict:
    """
    Update existing kernel
    """
    logger.debug('update_kernel_notebook')
    logger.debug(json_data)
    kernel_manager_uuid = json_data['kernelManagerUUID']
    kernel_mode_obj = sparta_3a64b1186a(user_obj, kernel_manager_uuid)
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
                sparta_eb1f839cdd(user_obj, kernel_manager_uuid))
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


def sparta_ba35ffeafc(json_data, user_obj) ->dict:
    """
    Save kernel notebook workspace
    """
    pass


def sparta_2f29f8d472(json_data, user_obj) ->dict:
    """
    Open a folder in VSCode."""
    folder_path = sparta_ad557db230(json_data['projectPath'])
    return sparta_e6a027bd1e(folder_path)


def sparta_3f5ee87df0(json_data, user_obj) ->dict:
    """
    Kernel open terminal
    """
    path = sparta_ad557db230(json_data['projectPath'])
    return sparta_7d51b73540(path)


def sparta_744c975151(json_data, user_obj) ->dict:
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
            lumino_layout_dump = json_data['luminoLayout']
            kernel_obj.lumino_layout = lumino_layout_dump
            kernel_obj.save()
    return {'res': 1}


def sparta_d2143dac3f(json_data, user_obj) ->dict:
    """
    Get kernel size
    """
    from project.sparta_8345d6a892.sparta_490625ab5b import qube_0c12c56358 as qube_0c12c56358
    kernel_manager_uuid = json_data['kernelManagerUUID']
    kernel_process_obj = qube_0c12c56358.sparta_a5c947582d(user_obj,
        kernel_manager_uuid)
    if kernel_process_obj is not None:
        kernel_size = qube_0c12c56358.sparta_1b0d2f97b7(kernel_process_obj)
        return {'res': 1, 'kernel_size': kernel_size}
    return {'res': -1}


def sparta_3ccd601826(json_data, user_obj) ->dict:
    """
    Delete kernel
    """
    kernel_manager_uuid = json_data['kernelManagerUUID']
    kernel_mode_obj = sparta_3a64b1186a(user_obj, kernel_manager_uuid)
    if kernel_mode_obj is not None:
        kernel_mode_obj.is_delete = True
        kernel_mode_obj.save()
    return {'res': 1}

#END OF QUBE
