import os
import re
import json
import time
import base64
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_b5395e1261 import qube_a357901b33 as qube_a357901b33
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832, sparta_36715732c5


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_f1d932221c(request):
    """
    Validate project path
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.sparta_f1d932221c(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_ac79e38472(request):
    """
    Validate project init git
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.sparta_ac79e38472(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_6cbe29e36e(request):
    """
    Load notebook library
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.sparta_6cbe29e36e(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_36715732c5
def sparta_7f047bd795(request):
    """
    Load notebook (existing project)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.sparta_7f047bd795(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_fc86b92763(request):
    """
    Load notebook for edit (existing project)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.sparta_fc86b92763(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_70cc8f3968(request):
    """
    Save notebook
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.sparta_70cc8f3968(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_b2f5d9f90b(request):
    """
    Save lumino layout for notebook view
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.sparta_b2f5d9f90b(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_b8d3733e52(request):
    """
    Delete notebook view
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.sparta_b8d3733e52(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_e4bf083526(request):
    """
    Django init
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.sparta_e4bf083526(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_2261dacae8(request):
    """
    Django model status
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.sparta_2261dacae8(json_data, request.user
        )
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_cf1afa243a(request):
    """
    Django migrate models
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.sparta_cf1afa243a(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_9a731cd1f1(request):
    """
    Open in vscode
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.sparta_9a731cd1f1(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_6f03452699(request):
    """
    Open terminal
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.sparta_6f03452699(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_d4d50dd08e(request):
    """
    Check is nodeJS is already init in the user's project folder (frontend)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.load_node_setup(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_6f06788e86(request):
    """
    Init node npm project
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.init_node_npm_project(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_f8197b013f(request):
    """
    Init node npm project
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.node_list_libraries(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_af47cdeae9(request):
    """
    Init django models
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.init_django_models(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_70dd42288d(request):
    """
    Init venv project
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.sparta_70dd42288d(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_a0e0726d91(request):
    """
    Init git project
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.sparta_a0e0726d91(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_cf1f18a193(request):
    """
    Set notebook entrypoin
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_a357901b33.sparta_cf1f18a193(json_data, request.user
        )
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
