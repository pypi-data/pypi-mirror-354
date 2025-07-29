from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_3b21db79ac
from project.sparta_8345d6a892.sparta_083d69b9eb import qube_267aa1e909 as qube_267aa1e909
from project.models import UserProfile
import project.sparta_312a90fa32.sparta_6696c7e57c.qube_52d8b82b2d as qube_52d8b82b2d


@sparta_3b21db79ac
@login_required(redirect_field_name='login')
def sparta_0d663b7c7a(request):
    """
        View help center
    """
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = -1
    user_infos_dict = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos_dict)
    dict_var['avatarImg'] = ''
    user_profile_set = UserProfile.objects.filter(user=request.user)
    if user_profile_set.count() > 0:
        user_profile_obj = user_profile_set[0]
        avatar_obj = user_profile_obj.avatar
        if avatar_obj is not None:
            image64 = user_profile_obj.avatar.image64
            dict_var['avatarImg'] = image64
    dict_var['bInvertIcon'] = 0
    return render(request, 'dist/project/helpCenter/helpCenter.html', dict_var)


@sparta_3b21db79ac
@login_required(redirect_field_name='login')
def sparta_27ed8cf767(request):
    """
    Click on the notification
    """
    user_profile_set = UserProfile.objects.filter(user=request.user)
    if user_profile_set.count() > 0:
        user_profile_obj = user_profile_set[0]
        user_profile_obj.has_open_tickets = False
        user_profile_obj.save()
    return sparta_0d663b7c7a(request)

#END OF QUBE
