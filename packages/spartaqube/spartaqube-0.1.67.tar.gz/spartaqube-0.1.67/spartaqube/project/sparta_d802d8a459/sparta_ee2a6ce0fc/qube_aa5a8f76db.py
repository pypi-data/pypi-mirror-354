import os
import re
import json
import time
import base64
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_5d42e2bd55 import qube_3b271aaa00 as qube_3b271aaa00
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832, sparta_36715732c5
from project.logger_config import logger


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_f6cc1be105(request):
    """
    Validate project path
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_f6cc1be105(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_6c5feac91f(request):
    """
    Validate project init git
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_6c5feac91f(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_c6e444c67d(request):
    """
    Validate project path init npm
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_c6e444c67d(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_fac2977bb3(request):
    """
    Load developer library
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_fac2977bb3(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_36715732c5
def sparta_5b2a15f224(request):
    """
    Load developer (existing project)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_5b2a15f224(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_0f83af1bfc(request):
    """
    Load developer for edit (existing project)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_0f83af1bfc(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_d1517de602(request):
    """
    Save developer
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_d1517de602(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_9d4e12471f(request):
    """
    Save lumino layout for developer view
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_9d4e12471f(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_2eef0c41eb(request):
    """
    Delete developer view
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_2eef0c41eb(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_108619635e(request):
    """
    Open in vscode
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_108619635e(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_f150d68275(request):
    """
    Open terminal
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_f150d68275(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_d4d50dd08e(request):
    """
    Check is nodeJS is already init in the user's project folder (frontend)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_d4d50dd08e(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_6f06788e86(request):
    """
    Init node npm project
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_6f06788e86(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_f8197b013f(request):
    """
    Init node npm project
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_f8197b013f(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_af47cdeae9(request):
    """
    Init django models
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_af47cdeae9(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_70dd42288d(request):
    """
    Init venv project
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_70dd42288d(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_a0e0726d91(request):
    """
    Init git project
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.init_git_project(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_11d3572bc5(request):
    """
    Hot reload preview
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_11d3572bc5(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_7f44f999f2(request):
    """
    Django models status
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_7f44f999f2(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_89038f975e(request):
    """
    Django models migrate
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_89038f975e(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_36715732c5
def sparta_3e97eb0c46(request):
    """
    Developer App Preview
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    project_path = json_data['projectPathVar']
    origin = json_data['origin']
    encoded_project_path = json_data['encodedProjectPath']
    identifier = json_data['identifier']
    dist_main_path = os.path.join(project_path, 'dist', 'main.js')
    with open(dist_main_path, 'r', encoding='utf-8') as f:
        js_code = f.read()

    def replacer(match):
        full_match = match.group(0)
        var_name = re.match('([a-zA-Z0-9_$]+)\\.kernelManagerUUID', full_match
            ).group(1)
        return (
            f'{var_name}.kernelManagerUUID=$("#{identifier}").data("kernel_manager_uuid"),'
            )
    pattern = '[a-zA-Z0-9_$]+\\.kernelManagerUUID\\s*=\\s*.*?,'
    new_js_code = re.sub(pattern, replacer, js_code)
    with open(dist_main_path, 'w', encoding='utf-8') as f:
        f.write(new_js_code)
    new_url = f'{origin}/user-project/{encoded_project_path}/'
    file_name = 'index.html'
    file_path = os.path.join(project_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    base_tag_pattern = '<base\\s+href=["\\\'].*?["\\\']>'
    if re.search(base_tag_pattern, html_content):
        html_content = re.sub(base_tag_pattern, f'<base href="{new_url}">',
            html_content)
    else:
        head_tag_pattern = '<head>'
        html_content = re.sub(head_tag_pattern,
            f'<head>\n<base href="{new_url}">', html_content)
    return HttpResponse(html_content, content_type='text/html')


@csrf_exempt
@sparta_36715732c5
def sparta_3651628d96(request):
    """
    API Developer Webservices
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_3b271aaa00.sparta_3651628d96(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
