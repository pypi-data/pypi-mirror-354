import os
import json
import getpass
import platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
import project.sparta_312a90fa32.sparta_6696c7e57c.qube_52d8b82b2d as qube_52d8b82b2d
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_3b21db79ac
from project.sparta_8345d6a892.sparta_26ea98fb42 import qube_b61b0eabde as qube_b61b0eabde
from project.sparta_8345d6a892.sparta_0c79de9c55 import qube_2e0f0ad7f3 as qube_2e0f0ad7f3


def sparta_934007d073() ->str:
    system = platform.system()
    if system == 'Windows':
        return 'windows'
    elif system == 'Linux':
        return 'linux'
    elif system == 'Darwin':
        return 'mac'
    else:
        return None


@csrf_exempt
@sparta_3b21db79ac
@login_required(redirect_field_name='login')
def sparta_1087aed82f(request):
    """
    Developer examples main page
    """
    if not conf_settings.IS_DEV_VIEW_ENABLED:
        dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
        return render(request, 'dist/project/homepage/homepage.html', dict_var)
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 12
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True
    current_path = os.path.dirname(__file__)
    project_path = os.path.dirname(os.path.dirname(current_path))
    static_path = os.path.join(project_path, 'static')
    frontend_path = os.path.join(static_path, 'js', 'developer', 'template',
        'frontend')
    dict_var['frontend_path'] = frontend_path
    spartaqube_path = os.path.dirname(project_path)
    backend_path = os.path.join(spartaqube_path, 'django_app_template',
        'developer', 'template', 'backend')
    dict_var['backend_path'] = backend_path
    return render(request, 'dist/project/developer/developerExamples.html',
        dict_var)

#END OF QUBE
