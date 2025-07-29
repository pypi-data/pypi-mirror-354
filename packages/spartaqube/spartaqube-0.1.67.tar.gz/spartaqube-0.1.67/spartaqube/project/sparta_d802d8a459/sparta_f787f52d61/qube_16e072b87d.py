import json
import base64
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_a539e6e3c7 import qube_da52878e3d as qube_da52878e3d
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832


@csrf_exempt
@sparta_f83f234832
def sparta_3e4a62a2a0(request):
    """
    Call autocomplete API
    """
    key = request.body.decode('utf-8')
    key = request.POST.get('key')
    api_func = request.body.decode('utf-8')
    api_func = request.POST.get('api_func')
    json_data = dict()
    json_data['key'] = key
    json_data['api_func'] = api_func
    res = qube_da52878e3d.sparta_3e4a62a2a0(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
