import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832
from project.sparta_8345d6a892.sparta_f31d5f54d2 import qube_7bab0c73a9 as qube_7bab0c73a9


@csrf_exempt
@sparta_f83f234832
def sparta_e29750b524(request):
    """

    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    user_obj = request.user
    res = qube_7bab0c73a9.sparta_e29750b524(json_data, user_obj)
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
