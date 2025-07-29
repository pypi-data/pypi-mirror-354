from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings as conf_settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import hashlib
import project.sparta_312a90fa32.sparta_6696c7e57c.qube_52d8b82b2d as qube_52d8b82b2d
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_3b21db79ac


@csrf_exempt
def sparta_7e6881bbe4(request):
    """
    View API
    """
    dictVar = qube_52d8b82b2d.sparta_5c1489406e(request)
    dictVar['menuBar'] = 8
    dictVar['bCodeMirror'] = True
    userKeyDict = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dictVar.update(userKeyDict)
    return render(request, 'dist/project/api/api.html', dictVar)

#END OF QUBE
