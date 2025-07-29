import json
import base64
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_c7a5b8be45 import qube_1565553d0d as qube_1565553d0d
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832, sparta_18288591d7


@csrf_exempt
@sparta_f83f234832
def sparta_1e60dc3dad(request):
    """
    Create launcher desktop icon
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_1565553d0d.sparta_1e60dc3dad(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
