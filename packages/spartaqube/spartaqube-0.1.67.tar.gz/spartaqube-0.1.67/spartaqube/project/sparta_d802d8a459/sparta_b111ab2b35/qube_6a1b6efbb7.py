import json
import base64
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_95feba8ea1 import qube_9db4644879 as qube_9db4644879
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832


@csrf_exempt
@sparta_f83f234832
def sparta_f588ea9f66(request):
    """

        """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_9db4644879.sparta_f588ea9f66(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_b721e42085(request):
    """

    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_9db4644879.sparta_b721e42085(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_13b5c7b88c(request):
    """

    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_9db4644879.sparta_13b5c7b88c(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
def sparta_8634196413(request):
    """
    Get default palette
    """
    default_palette: list = qube_9db4644879.sparta_8634196413(request.user)
    res = {'res': 1, 'default_palette': default_palette}
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_33746681b8(request):
    """

    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_9db4644879.sparta_33746681b8(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
