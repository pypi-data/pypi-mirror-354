import json
import base64
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_315890656a import qube_84226eecde as qube_84226eecde
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832, sparta_36715732c5


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_1bf011fae2(request):
    """
    Load plotDB Developer Library
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_84226eecde.sparta_1bf011fae2(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_739916762c(request):
    """
    Get default plotDB developer default path
    """
    res = qube_84226eecde.sparta_739916762c()
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
