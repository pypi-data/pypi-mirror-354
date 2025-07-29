import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832
from project.sparta_8345d6a892.sparta_e97ee25056 import qube_3792971c85 as qube_3792971c85


@csrf_exempt
@sparta_f83f234832
def sparta_3a4d831997(request):
    """
    Search members
    """
    query = request.body.decode('utf-8')
    query = request.POST.get('query')
    json_data = dict()
    json_data['query'] = query
    user_obj = request.user
    res = qube_3792971c85.sparta_3a4d831997(json_data, user_obj)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_f4807c62c5(request):
    """

    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    user_obj = request.user
    res = qube_3792971c85.sparta_f4807c62c5(json_data, user_obj)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_d5beec0a69(request):
    """

    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    user_obj = request.user
    res = qube_3792971c85.sparta_d5beec0a69(json_data, user_obj)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_3c044d5c30(request):
    """
    Load privileges for all users/groups
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    user_obj = request.user
    res = qube_3792971c85.sparta_3c044d5c30(json_data, user_obj)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_0c7ca8e326(request):
    """

    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    user_obj = request.user
    res = qube_3792971c85.sparta_0c7ca8e326(json_data, user_obj)
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
