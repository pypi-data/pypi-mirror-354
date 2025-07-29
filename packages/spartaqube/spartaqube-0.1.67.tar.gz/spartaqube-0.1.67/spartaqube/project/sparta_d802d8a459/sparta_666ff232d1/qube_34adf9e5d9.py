import os
import json
import asyncio
import time
import base64
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_e8bd2ac893 import qube_0efb58479b as qube_0efb58479b
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832, sparta_36715732c5


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_9068c9e355(request):
    """
    Load a kernel notebook
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0efb58479b.sparta_9068c9e355(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_ac9d03f6ee(request):
    """
    Save kernel notebook
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0efb58479b.sparta_ac9d03f6ee(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_2f29f8d472(request):
    """
    Open kernel in vscode
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0efb58479b.sparta_2f29f8d472(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_3f5ee87df0(request):
    """
    Open kernel terminal
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0efb58479b.sparta_3f5ee87df0(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_744c975151(request):
    """
    Save lumino layout
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0efb58479b.sparta_744c975151(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_d2143dac3f(request):
    """
    Get kernel size
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0efb58479b.sparta_d2143dac3f(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_3ccd601826(request):
    """
    Delete all kernel managers
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0efb58479b.sparta_3ccd601826(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
