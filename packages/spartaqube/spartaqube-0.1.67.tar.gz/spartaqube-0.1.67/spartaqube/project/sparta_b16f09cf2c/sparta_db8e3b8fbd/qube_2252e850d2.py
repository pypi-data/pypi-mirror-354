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
from django.conf import settings as conf_settings
import project.sparta_312a90fa32.sparta_6696c7e57c.qube_52d8b82b2d as qube_52d8b82b2d
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_3b21db79ac
from project.sparta_8345d6a892.sparta_5d42e2bd55 import qube_3b271aaa00 as qube_3b271aaa00
from project.sparta_8345d6a892.sparta_952c41e91e.qube_ef9e4f9eb1 import sparta_9c89cfd808


@csrf_exempt
@sparta_3b21db79ac
@login_required(redirect_field_name='login')
def sparta_c6ce1898c9(request):
    """
    Developer main page
    """
    if not conf_settings.IS_DEV_VIEW_ENABLED:
        dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
        return render(request, 'dist/project/homepage/homepage.html', dict_var)
    qube_3b271aaa00.sparta_c538af9c98()
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 12
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True

    def create_folder_if_not_exists(path):
        folder_path = Path(path)
        if not folder_path.exists():
            folder_path.mkdir(parents=True)
    spartaqube_volume_path = sparta_9c89cfd808()
    default_project_path = os.path.join(spartaqube_volume_path, 'developer')
    create_folder_if_not_exists(default_project_path)
    dict_var['default_project_path'] = default_project_path
    return render(request, 'dist/project/developer/developer.html', dict_var)


@csrf_exempt
def sparta_85c6cabdde(request, id):
    """
    Developer app exec
    """
    if not conf_settings.IS_DEV_VIEW_ENABLED:
        dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
        return render(request, 'dist/project/homepage/homepage.html', dict_var)
    if id is None:
        developer_id = request.GET.get('id')
    else:
        developer_id = id
    b_redirect_developer_db = False
    if developer_id is None:
        b_redirect_developer_db = True
    else:
        developer_access_dict = qube_3b271aaa00.has_developer_access(
            developer_id, request.user)
        res_access = developer_access_dict['res']
        if res_access == -1:
            b_redirect_developer_db = True
    if b_redirect_developer_db:
        return sparta_c6ce1898c9(request)
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 12
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True
    developer_obj = developer_access_dict['developer_obj']
    dict_var['default_project_path'] = developer_obj.project_path
    dict_var['b_require_password'] = 0 if developer_access_dict['res'
        ] == 1 else 1
    dict_var['developer_id'] = developer_obj.developer_id
    dict_var['developer_name'] = developer_obj.name
    dict_var['bPublicUser'] = request.user.is_anonymous
    return render(request, 'dist/project/developer/developerRun.html', dict_var
        )


@csrf_exempt
@sparta_3b21db79ac
@login_required(redirect_field_name='login')
def sparta_c3450b9134(request, id):
    """
    
    """
    print('OPEN DEVELOPER DETACHED')
    if id is None:
        developer_id = request.GET.get('id')
    else:
        developer_id = id
    print('developer_id')
    print(developer_id)
    b_redirect_developer_db = False
    if developer_id is None:
        b_redirect_developer_db = True
    else:
        developer_access_dict = qube_3b271aaa00.has_developer_access(
            developer_id, request.user)
        res_access = developer_access_dict['res']
        if res_access == -1:
            b_redirect_developer_db = True
    print('b_redirect_developer_db')
    print(b_redirect_developer_db)
    if b_redirect_developer_db:
        return sparta_c6ce1898c9(request)
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 12
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True
    developer_obj = developer_access_dict['developer_obj']
    dict_var['default_project_path'] = developer_obj.project_path
    dict_var['b_require_password'] = 0 if developer_access_dict['res'
        ] == 1 else 1
    dict_var['developer_id'] = developer_obj.developer_id
    dict_var['developer_name'] = developer_obj.name
    dict_var['bPublicUser'] = request.user.is_anonymous
    return render(request, 'dist/project/developer/developerDetached.html',
        dict_var)


def sparta_7f61bbc2b8(request, project_path, file_name):
    """
    Server IFRAME mode (DEPRECATED)
    """
    project_path = unquote(project_path)
    return serve(request, file_name, document_root=project_path)

#END OF QUBE
