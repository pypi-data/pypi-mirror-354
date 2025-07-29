import json
import base64
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_e670621234 import qube_9fb9ed74d5 as qube_9fb9ed74d5
from project.sparta_8345d6a892.sparta_e670621234 import qube_c0d55cdffb as qube_c0d55cdffb
from project.sparta_8345d6a892.sparta_952c41e91e import qube_41685030f2 as qube_41685030f2
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832


@csrf_exempt
@sparta_f83f234832
def sparta_2e362c16a1(request):
    """
        Upload resources
    """
    json_data = request.POST.dict()
    requestFiles = request.FILES
    if 'files[]' in requestFiles:
        res = qube_9fb9ed74d5.sparta_482110f514(json_data, request.user,
            requestFiles['files[]'])
    else:
        res = {'res': 1}
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_c4a52076d3(request):
    """
        Create new resource (file or folder)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_9fb9ed74d5.sparta_5ec460944d(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_54353853be(request):
    """
        Move resource (file and/or folder)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_9fb9ed74d5.sparta_7dc019011e(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_aefbb1a65a(request):
    """
    OK Load notebook folder list
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_9fb9ed74d5.sparta_3499f54fac(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_d931fe2dd5(request):
    """
    Open resource (to preview)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_c0d55cdffb.sparta_40bb4676bf(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_ac941e3722(request):
    """
    OK Save (edit) a resource
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_9fb9ed74d5.sparta_ed41ad0d88(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_68ab0e127c(request):
    """
    OK Rename resource
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_9fb9ed74d5.sparta_f691ead76a(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_fbe00530ed(request):
    """
    OK Delete resource
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_9fb9ed74d5.sparta_792035baa8(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_0724898d24(request):
    """
    OK Delete multiple resources
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_9fb9ed74d5.sparta_8057525859(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_901ca5f97c(request):
    """
    OK Download resource
    """
    file_name = request.GET['fileName']
    file_path = request.GET['filePath']
    project_path = request.GET['projectPath']
    app_id = request.GET['appId']
    json_data = {'fileName': file_name, 'filePath': file_path, 'appId':
        app_id, 'projectPath': base64.b64decode(project_path).decode('utf-8')}
    res = qube_9fb9ed74d5.sparta_91e4c34830(json_data, request.user)
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
def sparta_b229113557(request):
    """
    Download folder
    """
    project_path = request.GET['projectPath']
    folderName = request.GET['folderName']
    json_data = {'projectPath': base64.b64decode(project_path).decode(
        'utf-8'), 'folderName': folderName}
    res = qube_9fb9ed74d5.sparta_2ae29b78a0(json_data, request.user)
    if res['res'] == 1:
        mf = res['zip']
        zipName = res['zipName']
        response = HttpResponse()
        response.write(mf.getvalue())
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            f'{zipName}.zip')
    else:
        response = HttpResponse()
        sourceCode = (
            f'Could not download the folder {folderName}, please try again')
        fileName = 'error.txt'
        response.write(sourceCode)
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            fileName)
    return response


@csrf_exempt
@sparta_f83f234832
def sparta_664268aa9a(request):
    """
    Download resource
    """
    app_id = request.GET['appId']
    project_path = request.GET['projectPath']
    json_data = {'appId': app_id, 'projectPath': base64.b64decode(
        project_path).decode('utf-8')}
    res = qube_9fb9ed74d5.sparta_e74173774a(json_data, request.user)
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

#END OF QUBE
