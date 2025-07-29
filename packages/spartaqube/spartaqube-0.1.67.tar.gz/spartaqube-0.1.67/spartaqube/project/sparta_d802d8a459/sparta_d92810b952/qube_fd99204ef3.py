import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832
from project.sparta_8345d6a892.sparta_083d69b9eb import qube_267aa1e909 as qube_267aa1e909


@csrf_exempt
@sparta_f83f234832
def sparta_546b498862(request):
    """
    Create new case
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_267aa1e909.sparta_546b498862(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_59ec168a6d(request):
    """
    Load my cases
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_267aa1e909.sparta_59ec168a6d(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_1fb24dbaf6(request):
    """
    Load conversation
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_267aa1e909.sparta_1fb24dbaf6(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_2cd5db5dc6(request):
    """
    Send new message in the chat
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_267aa1e909.sparta_2cd5db5dc6(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_1ab7ab78c2(request):
    """
    Close case
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_267aa1e909.sparta_1ab7ab78c2(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_5d8856400e(request):
    """
    Get number notifications
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_267aa1e909.sparta_5d8856400e(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
