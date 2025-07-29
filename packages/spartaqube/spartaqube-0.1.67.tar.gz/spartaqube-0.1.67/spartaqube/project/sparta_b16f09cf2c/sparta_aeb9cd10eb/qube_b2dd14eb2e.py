import os
import json
import getpass
import platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from django.http import FileResponse, Http404
from urllib.parse import unquote
import project.sparta_312a90fa32.sparta_6696c7e57c.qube_52d8b82b2d as qube_52d8b82b2d
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_3b21db79ac
from project.sparta_8345d6a892.sparta_490625ab5b import qube_0c12c56358 as qube_0c12c56358
from project.sparta_8345d6a892.sparta_e4b2f842b2 import qube_9bc385c03d as qube_9bc385c03d
from project.sparta_8345d6a892.sparta_952c41e91e.qube_ef9e4f9eb1 import sparta_9c89cfd808


@csrf_exempt
@sparta_3b21db79ac
@login_required(redirect_field_name='login')
def sparta_3b351d15c1(request):
    """
    View Homepage Welcome back
    """
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = -1
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    return render(request, 'dist/project/homepage/homepage.html', dict_var)


@csrf_exempt
@sparta_3b21db79ac
@login_required(redirect_field_name='login')
def sparta_ac40e9ccf2(request, kernel_manager_uuid):
    b_redirect_homepage = False
    if kernel_manager_uuid is None:
        b_redirect_homepage = True
    else:
        kernel_process_obj = qube_0c12c56358.sparta_a5c947582d(request.user, kernel_manager_uuid)
        if kernel_process_obj is None:
            b_redirect_homepage = True
    if b_redirect_homepage:
        return sparta_3b351d15c1(request)

    def create_folder_if_not_exists(path):
        folder_path = Path(path)
        if not folder_path.exists():
            folder_path.mkdir(parents=True)
    spartaqube_volume_path = sparta_9c89cfd808()
    default_project_path = os.path.join(spartaqube_volume_path, 'kernel')
    create_folder_if_not_exists(default_project_path)
    kernel_path = os.path.join(default_project_path, kernel_manager_uuid)
    create_folder_if_not_exists(kernel_path)
    filename = os.path.join(kernel_path, 'main.ipynb')
    if not os.path.exists(filename):
        empty_notebook_dict = qube_9bc385c03d.sparta_cb4948e954()
        with open(filename, 'w') as file:
            file.write(json.dumps(empty_notebook_dict))
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['default_project_path'] = default_project_path
    dict_var['menuBar'] = -1
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['kernel_name'] = kernel_process_obj.name
    dict_var['kernelManagerUUID'] = kernel_process_obj.kernel_manager_uuid
    dict_var['bCodeMirror'] = True
    dict_var['bPublicUser'] = request.user.is_anonymous
    return render(request,
        'dist/project/sqKernelNotebook/sqKernelNotebook.html', dict_var)

#END OF QUBE
