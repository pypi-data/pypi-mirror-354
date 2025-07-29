import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_5ba00adfe7 import qube_abe0696d41 as qube_abe0696d41
from project.sparta_312a90fa32.sparta_6696c7e57c.qube_52d8b82b2d import sparta_3f690c3f81
from project.logger_config import logger


@csrf_exempt
def sparta_879014132f(request):
    """

    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    return qube_abe0696d41.sparta_879014132f(json_data)


@csrf_exempt
def sparta_41b1869bd1(request):
    """
    Logout user (useful for dockerCentral before redirecting into app container)
    """
    logout(request)
    res = {'res': 1}
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
def sparta_d40338aeb2(request):
    """

    """
    if request.user.is_authenticated:
        is_auth = 1
    else:
        is_auth = 0
    res = {'res': 1, 'isAuth': is_auth}
    resJson = json.dumps(res)
    return HttpResponse(resJson)


def sparta_9c9336ffa7(request):
    """
    Modal Authentication (save)
    """
    from django.contrib.auth import authenticate, login
    from django.contrib.auth.models import User
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    email = json_data['email']
    password = json_data['password']
    is_auth = 0
    try:
        user = User.objects.get(email=email)
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            is_auth = 1
    except User.DoesNotExist:
        pass
    res = {'res': 1, 'isAuth': is_auth}
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
