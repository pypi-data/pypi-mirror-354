import os
import json
import asyncio
import time
import base64
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_490625ab5b import qube_0c12c56358 as qube_0c12c56358
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832, sparta_36715732c5


@csrf_exempt
@sparta_36715732c5
def sparta_63e4e4ab5e(request):
    """
    Create a new kernel manager
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0c12c56358.sparta_63e4e4ab5e(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_411e5dc124(request):
    """
    Restart kernel
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0c12c56358.sparta_411e5dc124(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_b21ccc50f9(request):
    """
    Activate a virutal environment in the kernel manager
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0c12c56358.sparta_b21ccc50f9(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_227c1409fa(request):
    """
    Get kernel infos (like the name, size, uptime and workspace variables)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0c12c56358.sparta_227c1409fa(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_16c30373dc(request):
    """
    Get kernel variable
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0c12c56358.sparta_16c30373dc(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_36715732c5
def sparta_63ecd50876(request):
    """
    Update kernel infos (like the name of the kernel)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0c12c56358.sparta_63ecd50876(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_bf6b5f6b51(request):
    """
    List available kernels
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0c12c56358.sparta_bf6b5f6b51(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_ae0f523d3c(request):
    """
    List available kernels offline
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0c12c56358.sparta_ae0f523d3c(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_abe1d1a2a0(request):
    """
    Destroy existing kernel manager
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0c12c56358.sparta_abe1d1a2a0(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_47b2ba406d(request):
    """
    Destroy all kernel managers
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0c12c56358.sparta_47b2ba406d(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_01c73ff9df(request):
    """
    Destroy all kernel managers
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0c12c56358.sparta_01c73ff9df(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_85e0ed15b6(request):
    """
    Search variable across all active kernels
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_0c12c56358.sparta_85e0ed15b6(json_data, request.user
        )
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
