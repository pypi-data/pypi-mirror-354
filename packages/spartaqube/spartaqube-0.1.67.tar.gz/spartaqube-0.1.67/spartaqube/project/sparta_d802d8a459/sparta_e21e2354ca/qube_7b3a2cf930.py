import json
import inspect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from project.sparta_8345d6a892.sparta_642565b7d1 import qube_671b123277 as qube_671b123277
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832


def sparta_37260c209d(request):
    res = {'res': 1}
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_62083cb1c2(request):
    """
    Send an email and contact SpartaQuant helpdesk
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_671b123277.sparta_62083cb1c2(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_209aecbdb6(request):
    """
    Update the password
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    userObjIni = request.user
    res = qube_671b123277.sparta_209aecbdb6(json_data, userObjIni)
    if res['res'] == 1:
        if 'userObj' in list(res.keys()):
            login(request, res['userObj'])
            res.pop('userObj', None)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_6947ac81d3(request):
    """
    Update spartaqube code (code to create an account)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    user_obj = request.user
    res = qube_671b123277.sparta_6947ac81d3(json_data, user_obj)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_ec50080fbb(request):
    """
    Update the profile picture of the user
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_671b123277.sparta_ec50080fbb(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_d2c8e67a6e(request):
    """
    Change dark/light theme
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_671b123277.sparta_d2c8e67a6e(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_c77b866ea1(request):
    """
    Change code editor theme
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_671b123277.sparta_c77b866ea1(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
def sparta_17639a5206(request):
    """
    Generate reset token code
    This is executed on the WORKER node (reset password html page)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_671b123277.token_reset_password_worker(json_data)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_6e40520650(request):
    """
    This is executed on the MASTER node (network-password vue js component)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_671b123277.network_master_reset_password(json_data, request.user
        )
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
def sparta_571569f541(request):
    """
    RESET PASSWORD USING ADMIN PASSWORD FOR LOCAL APPLICATION (PIP)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_671b123277.sparta_571569f541(json_data)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
def sparta_6652d81233(request):
    """
    This is executed on the MASTER node
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_671b123277.sparta_6652d81233(request, json_data)
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
