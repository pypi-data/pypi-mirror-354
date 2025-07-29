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
from project.sparta_8345d6a892.sparta_b5395e1261 import qube_a357901b33 as qube_a357901b33
from project.sparta_8345d6a892.sparta_952c41e91e.qube_ef9e4f9eb1 import sparta_9c89cfd808


@csrf_exempt
@sparta_3b21db79ac
@login_required(redirect_field_name='login')
def sparta_b03d5d0e2b(request):
    """
    Notebook main page
    """
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 13
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True

    def create_folder_if_not_exists(path):
        folder_path = Path(path)
        if not folder_path.exists():
            folder_path.mkdir(parents=True)
    spartaqube_volume_path = sparta_9c89cfd808()
    default_project_path = os.path.join(spartaqube_volume_path, 'notebook')
    create_folder_if_not_exists(default_project_path)
    dict_var['default_project_path'] = default_project_path
    return render(request, 'dist/project/notebook/notebook.html', dict_var)


@csrf_exempt
def sparta_105b35cd49(request, id):
    """
    Notebook app exec
    """
    if id is None:
        notebook_id = request.GET.get('id')
    else:
        notebook_id = id
    b_redirect_notebook_db = False
    if notebook_id is None:
        b_redirect_notebook_db = True
    else:
        notebook_access_dict = qube_a357901b33.sparta_23dd5f5513(notebook_id,
            request.user)
        res_access = notebook_access_dict['res']
        if res_access == -1:
            b_redirect_notebook_db = True
    if b_redirect_notebook_db:
        return sparta_b03d5d0e2b(request)
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 12
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True
    notebook_obj = notebook_access_dict['notebook_obj']
    dict_var['default_project_path'] = notebook_obj.project_path
    dict_var['b_require_password'] = 0 if notebook_access_dict['res'
        ] == 1 else 1
    dict_var['notebook_id'] = notebook_obj.notebook_id
    dict_var['notebook_name'] = notebook_obj.name
    dict_var['bPublicUser'] = request.user.is_anonymous
    return render(request, 'dist/project/notebook/notebookRun.html', dict_var)


@csrf_exempt
@sparta_3b21db79ac
@login_required(redirect_field_name='login')
def sparta_6d36709516(request, id):
    if id is None:
        notebook_id = request.GET.get('id')
    else:
        notebook_id = id
    b_redirect_notebook_db = False
    if notebook_id is None:
        b_redirect_notebook_db = True
    else:
        notebook_access_dict = qube_a357901b33.sparta_23dd5f5513(notebook_id,
            request.user)
        res_access = notebook_access_dict['res']
        if res_access == -1:
            b_redirect_notebook_db = True
    if b_redirect_notebook_db:
        return sparta_b03d5d0e2b(request)
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 12
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True
    notebook_obj = notebook_access_dict['notebook_obj']
    dict_var['default_project_path'] = notebook_obj.project_path
    dict_var['b_require_password'] = 0 if notebook_access_dict['res'
        ] == 1 else 1
    dict_var['notebook_id'] = notebook_obj.notebook_id
    dict_var['notebook_name'] = notebook_obj.name
    dict_var['bPublicUser'] = request.user.is_anonymous
    return render(request, 'dist/project/notebook/notebookDetached.html',
        dict_var)

#END OF QUBE
