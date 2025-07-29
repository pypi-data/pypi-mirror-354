import os
import json
import base64
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_e4b2f842b2 import qube_26d02053e2 as qube_26d02053e2
from project.sparta_8345d6a892.sparta_e4b2f842b2 import qube_1f969428d3 as qube_1f969428d3
from project.sparta_8345d6a892.sparta_e4b2f842b2 import qube_8ecd6dcb08 as qube_8ecd6dcb08
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832, sparta_36715732c5


@csrf_exempt
@sparta_f83f234832
def sparta_2d7c3c78db(request):
    """
    Clone a repo in a folder
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_8ecd6dcb08.sparta_2d7c3c78db(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_95f2a59d86(request):
    """
    Create a new local repository
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_8ecd6dcb08.sparta_95f2a59d86(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_c07cee739f(request):
    """
    Add remote origin
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    try:
        res = qube_8ecd6dcb08.sparta_c07cee739f(json_data, request.user)
    except Exception as e:
        res = {'res': -1, 'errorMsg': str(e)}
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_cfacadb7dc(request):
    """
    Update repo settings
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_8ecd6dcb08.sparta_cfacadb7dc(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_8dcb2da4ea(request):
    """
    Load available remote branches to track
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_8ecd6dcb08.sparta_8dcb2da4ea(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_8eeea64f46(request):
    """
    Change track remote
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    try:
        res = qube_8ecd6dcb08.sparta_8eeea64f46(json_data, request.user)
    except Exception as e:
        res = {'res': -1, 'errorMsg': str(e)}
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_61a32ef1ad(request):
    """
    Pull repo
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    try:
        res = qube_8ecd6dcb08.sparta_61a32ef1ad(json_data, request.user)
    except Exception as e:
        res = {'res': -1, 'errorMsg': str(e)}
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_317865cf5a(request):
    """
    Push to remote repository
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    try:
        res = qube_8ecd6dcb08.sparta_317865cf5a(json_data, request.user)
    except Exception as e:
        res = {'res': -1, 'errorMsg': str(e)}
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_18221e93ea(request):
    """
    Fetch repo
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    try:
        res = qube_8ecd6dcb08.sparta_18221e93ea(json_data, request.user)
    except Exception as e:
        res = {'res': -1, 'errorMsg': str(e)}
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_ef1a55f717(request):
    """
    Check if git repo created
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_8ecd6dcb08.sparta_ef1a55f717(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_02ad92acd1(request):
    """
    Load all commits
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_8ecd6dcb08.sparta_02ad92acd1(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_40e6ee6e8f(request):
    """
    Get list of changed files (local) that need to be push to remote
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_8ecd6dcb08.sparta_40e6ee6e8f(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_d40cb70f02(request):
    """
    Run commit
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_8ecd6dcb08.sparta_d40cb70f02(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_d6096c7033(request):
    """
    Delete repository
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_8ecd6dcb08.sparta_d6096c7033(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_3ac4ae3281(request):
    """
    Delete Remote
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_8ecd6dcb08.sparta_3ac4ae3281(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_82eb26384a(request):
    """
    Load all branches
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_8ecd6dcb08.sparta_82eb26384a(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_8df26e4912(request):
    """
    Create new branch
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_8ecd6dcb08.sparta_8df26e4912(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_e2a7a6d25b(request):
    """
    Checkout branch
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_8ecd6dcb08.sparta_e2a7a6d25b(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_4a50d341e1(request):
    """
    Merge branch
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_8ecd6dcb08.sparta_4a50d341e1(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_6159113fd3(request):
    """
    Delete branch
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_8ecd6dcb08.sparta_6159113fd3(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_04a31d26b0(request):
    """
    Load files diff
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_8ecd6dcb08.sparta_04a31d26b0(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
