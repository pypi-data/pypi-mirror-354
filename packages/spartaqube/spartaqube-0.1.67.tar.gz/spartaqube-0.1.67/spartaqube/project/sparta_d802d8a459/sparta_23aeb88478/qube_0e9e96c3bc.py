import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_87f32c6e97 import qube_93b4ab09a2 as qube_93b4ab09a2
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832


@csrf_exempt
@sparta_f83f234832
def sparta_d5db20e4c8(request):
    """
    Create a group (to share dataQuantDB, spartBtn or Dashboard)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_93b4ab09a2.sparta_d5db20e4c8(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_42fc3c808a(request):
    """
    Load group members (only for admin)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_93b4ab09a2.sparta_42fc3c808a(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_3779cedad5(request):
    """
    Load group members (only for admin)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_93b4ab09a2.sparta_3779cedad5(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_f7303817af(request):
    """
    Edit group (name, or add member)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_93b4ab09a2.sparta_f7303817af(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_97f4d0e5c0(request):
    """
    Give admin rights to a user
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_93b4ab09a2.sparta_97f4d0e5c0(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_1d6f3053e5(request):
    """
    Delete group (only for admin)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_93b4ab09a2.sparta_1d6f3053e5(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_55a0cf00e1(request):
    """
    Only for the creator of the group
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_93b4ab09a2.sparta_55a0cf00e1(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_0bdf5b0dad(request):
    """
    Leave a group
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_93b4ab09a2.sparta_0bdf5b0dad(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
