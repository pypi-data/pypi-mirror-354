import json
import base64
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_f1a366f59f import qube_137201374c as qube_137201374c
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832, sparta_18288591d7
from project.logger_config import logger


@csrf_exempt
@sparta_f83f234832
def sparta_ade4939e10(request):
    """
    Load API token
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_137201374c.sparta_ade4939e10(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_b1cf579c3c(request):
    """
    Generate API token
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_137201374c.sparta_b1cf579c3c(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
def sparta_001e0a1c14(request):
    """
    Get plot types
    """
    res = qube_137201374c.sparta_4410fb3e72()
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
def sparta_5c449a8ae7(request):
    """
    
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    try:
        res = qube_137201374c.sparta_5c449a8ae7(json_data)
    except Exception as e:
        logger.debug(e)
        res = {'res': -1}
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
def sparta_975e43bb22(request):
    """
    Execute api example user code
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_137201374c.sparta_975e43bb22(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_18288591d7
def sparta_a65a94aacc(request):
    """
    Api web service access
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_137201374c.sparta_a65a94aacc(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_6a85acfce6(request):
    """
    DEPRECATED
    Preparing data source from the session
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_137201374c.sparta_6a85acfce6(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
def sparta_4a2265c0f2(request):
    """
    Preparing data source from the session for API plot_template method
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_137201374c.sparta_4a2265c0f2(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
def sparta_bf768d875c(request):
    """
    API autocomplete suggestions
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_137201374c.sparta_bf768d875c(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
