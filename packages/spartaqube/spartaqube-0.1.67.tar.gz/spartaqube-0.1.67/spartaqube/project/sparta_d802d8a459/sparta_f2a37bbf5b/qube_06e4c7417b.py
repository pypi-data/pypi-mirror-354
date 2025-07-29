import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_8345d6a892.sparta_d13b024af3 import qube_01cf2709c5 as qube_01cf2709c5
from project.sparta_8345d6a892.sparta_083d69b9eb import qube_267aa1e909 as qube_267aa1e909
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832


@csrf_exempt
@sparta_f83f234832
def sparta_894a12f004(request):
    """
    Load notifications (shared, group added, alert trigger, software update)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    user_obj = request.user
    nb_notification_help_center = 0
    user_profile_set = UserProfile.objects.filter(user=user_obj)
    if user_profile_set.count() > 0:
        user_profile_obj = user_profile_set[0]
        if user_profile_obj.has_open_tickets:
            json_data['userId'] = user_profile_obj.user_profile_id
            res_help_center_notification_dict = (qube_267aa1e909.sparta_5d8856400e(user_obj))
            if res_help_center_notification_dict['res'] == 1:
                nb_notification_help_center = int(
                    res_help_center_notification_dict['nbNotifications'])
    res = qube_01cf2709c5.sparta_894a12f004(json_data, user_obj)
    res['nbNotificationsHelpCenter'] = nb_notification_help_center
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
def sparta_0da9584e65(request):
    """
    Set seen notification
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_01cf2709c5.sparta_4ac7a585b9(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
