import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_d1c61d93fd import qube_92a7984018 as qube_92a7984018
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832, sparta_18288591d7


@csrf_exempt
@sparta_f83f234832
def sparta_2bb8a248b0(request):
    """
    Save param user reduce size plotDB
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_92a7984018.sparta_2bb8a248b0(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_c9ca6c556b(request):
    """
    Save param user reduce size API
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_92a7984018.sparta_c9ca6c556b(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
