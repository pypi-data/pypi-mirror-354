import os
import json
import getpass
import platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_312a90fa32.sparta_6696c7e57c.qube_52d8b82b2d as qube_52d8b82b2d
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_3b21db79ac
from project.sparta_8345d6a892.sparta_26ea98fb42 import qube_b61b0eabde as qube_b61b0eabde
from project.sparta_8345d6a892.sparta_0c79de9c55 import qube_2e0f0ad7f3 as qube_2e0f0ad7f3
from project.sparta_8345d6a892.sparta_952c41e91e.qube_ef9e4f9eb1 import sparta_9c89cfd808


@csrf_exempt
@sparta_3b21db79ac
@login_required(redirect_field_name='login')
def sparta_432ac08c61(request):
    """
    Dashboard main page
    """
    edit_chart_id = request.GET.get('edit')
    if edit_chart_id is None:
        edit_chart_id = '-1'
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 9
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True
    dict_var['edit_chart_id'] = edit_chart_id

    def create_folder_if_not_exists(path):
        folder_path = Path(path)
        if not folder_path.exists():
            folder_path.mkdir(parents=True)
    spartaqube_volume_path = sparta_9c89cfd808()
    default_project_path = os.path.join(spartaqube_volume_path, 'dashboard')
    create_folder_if_not_exists(default_project_path)
    dict_var['default_project_path'] = default_project_path
    return render(request, 'dist/project/dashboard/dashboard.html', dict_var)


@csrf_exempt
def sparta_1e12530ba4(request, id):
    """
    Dashboard Run Mode
    """
    if id is None:
        dashboard_id = request.GET.get('id')
    else:
        dashboard_id = id
    return sparta_7a38fa3e75(request, dashboard_id)


def sparta_7a38fa3e75(request, dashboard_id, session='-1'):
    """
    
    """
    b_redirect_dashboard_db = False
    if dashboard_id is None:
        b_redirect_dashboard_db = True
    else:
        dashboard_access_dict = qube_2e0f0ad7f3.has_dashboard_access(
            dashboard_id, request.user)
        res_access = dashboard_access_dict['res']
        if res_access == -1:
            b_redirect_dashboard_db = True
    if b_redirect_dashboard_db:
        return sparta_432ac08c61(request)
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 9
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True
    dashboard_obj = dashboard_access_dict['dashboard_obj']
    dict_var['b_require_password'] = 0 if dashboard_access_dict['res'
        ] == 1 else 1
    dict_var['dashboard_id'] = dashboard_obj.dashboard_id
    dict_var['dashboard_name'] = dashboard_obj.name
    dict_var['bPublicUser'] = request.user.is_anonymous
    dict_var['session'] = str(session)
    return render(request, 'dist/project/dashboard/dashboardRun.html', dict_var
        )

#END OF QUBE
