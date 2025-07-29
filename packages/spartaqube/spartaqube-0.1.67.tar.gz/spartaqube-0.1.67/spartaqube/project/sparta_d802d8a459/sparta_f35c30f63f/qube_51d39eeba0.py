import os
import json
import base64
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_e4b2f842b2 import qube_26d02053e2 as qube_26d02053e2
from project.sparta_8345d6a892.sparta_e4b2f842b2 import qube_1f969428d3 as qube_1f969428d3
from project.sparta_8345d6a892.sparta_0c79de9c55 import qube_2e0f0ad7f3 as qube_2e0f0ad7f3
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832, sparta_36715732c5


@csrf_exempt
def sparta_e11f66db92(request):
    """
    Load File Resource (Ipynb)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_26d02053e2.sparta_e11f66db92(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_53ef909ea5(request):
    """
    Load File Resource (Generique)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_26d02053e2.sparta_53ef909ea5(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_b17462e3c2(request):
    """
    Save file content of a generique resource
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_26d02053e2.sparta_b17462e3c2(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_015a48123c(request):
    """
    Save file content of an ipynb resource
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_26d02053e2.sparta_015a48123c(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_bf1e093bd7(request):
    """
    Validate project path
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_26d02053e2.sparta_bf1e093bd7(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_72f20a3ba5(request):
    """
    List file and folders
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_26d02053e2.sparta_72f20a3ba5(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_8ad485d094(request):
    """
    Create new resource (dashboard project explorer)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_26d02053e2.sparta_8ad485d094(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_2c7c2bcf76(request):
    """
    Rename resource (dashboard project explorer)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_26d02053e2.sparta_2c7c2bcf76(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_770d960d5d(request):
    """
    Move resources (drag & drop) (dashboard project explorer)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_26d02053e2.sparta_770d960d5d(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_5a1eefba3a(request):
    """
    Delete resource
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_26d02053e2.sparta_5a1eefba3a(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_c539cb215f(request):
    """
    Delete multiple resources
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_26d02053e2.dashboard_project_explorer_delete_multiple_resources(
        json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_d1dd25468c(request):
    """
    Upload resources
    """
    json_data = request.POST.dict()
    requestFiles = request.FILES
    res = qube_26d02053e2.sparta_d1dd25468c(json_data,
        request.user, requestFiles['files[]'])
    resJson = json.dumps(res)
    return HttpResponse(resJson)


def sparta_909e37ec15(path):
    path = os.path.normpath(path)
    if os.path.isfile(path):
        path = os.path.dirname(path)
    return os.path.basename(path)


def sparta_17aaa52867(path):
    path = os.path.normpath(path)
    return os.path.basename(path)


@csrf_exempt
@sparta_f83f234832
def sparta_164a1e8567(request):
    """
    OK Download resource
    """
    path_resource = request.GET['pathResource']
    path_resource = base64.b64decode(path_resource).decode('utf-8')
    project_path = request.GET['projectPath']
    dashboard_id = request.GET['dashboardId']
    file_name = sparta_17aaa52867(path_resource)
    json_data = {'pathResource': path_resource, 'dashboardId': dashboard_id,
        'projectPath': base64.b64decode(project_path).decode('utf-8')}
    res = qube_26d02053e2.sparta_91e4c34830(json_data, request.user)
    if res['res'] == 1:
        try:
            with open(res['fullPath'], 'rb') as fh:
                response = HttpResponse(fh.read(), content_type=
                    'application/force-download')
                response['Content-Disposition'
                    ] = 'attachment; filename=' + str(file_name)
                return response
        except Exception as e:
            pass
    raise Http404


@csrf_exempt
@sparta_f83f234832
def sparta_27fa11c44f(request):
    """
    Download resource
    """
    dashboard_id = request.GET['dashboardId']
    project_path = request.GET['projectPath']
    json_data = {'dashboardId': dashboard_id, 'projectPath': base64.b64decode(project_path).decode('utf-8')}
    res = qube_26d02053e2.sparta_e74173774a(json_data, request.user)
    if res['res'] == 1:
        mf = res['zip']
        zipName = res['zipName']
        response = HttpResponse()
        response.write(mf.getvalue())
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            f'{zipName}.zip')
    else:
        response = HttpResponse()
        sourceCode = 'Could not download the application, please try again'
        fileName = 'error.txt'
        response.write(sourceCode)
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            fileName)
    return response


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_5b9eccc11a(request):
    """
    This function returns the list of available venv 
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_1f969428d3.sparta_5b9eccc11a(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_bdff51a6c0(request):
    """
    This function creates a venv 
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_1f969428d3.sparta_bdff51a6c0(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_eba6095864(request):
    """
    This function set a specific venv to a dashboard project
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_1f969428d3.sparta_eba6095864(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_1a2cdc9101(request):
    """
    This function set a specific venv to a notebook project
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_1f969428d3.sparta_1a2cdc9101(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_72eae12b98(request):
    """
    Set a virtual environment in the kernel
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_1f969428d3.sparta_72eae12b98(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_aaaee63040(request):
    """
    This function set a specific venv to a developer project
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_1f969428d3.sparta_aaaee63040(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_00f869edca(request):
    """
    This function remove a virtual env from a dashboard project
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_1f969428d3.sparta_00f869edca(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_c8a25eb11d(request):
    """
    This function remove a virtual env from a notebook project
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_1f969428d3.sparta_c8a25eb11d(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_1c923c6ad7(request):
    """
    Set a virtual environment in the kernel
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_1f969428d3.sparta_1c923c6ad7(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_f39df83d4a(request):
    """
    This function remove a virtual env from a developer project
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_1f969428d3.sparta_f39df83d4a(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_05a22862ae(request):
    """
    This function deletes a venv 
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_1f969428d3.sparta_05a22862ae(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_5207f54fc3(request):
    """
    Get the output of pip list for a specific virtual environment
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_1f969428d3.sparta_5207f54fc3(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_02a5fbaa3e(request):
    """
    Export venv libraries to requirements.txt
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_1f969428d3.sparta_02a5fbaa3e(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_f768203fcc(request):
    """
    Open terminal with venv activated
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_1f969428d3.sparta_f768203fcc(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
