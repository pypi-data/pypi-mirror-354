from urllib.parse import urlparse, urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_312a90fa32.sparta_6696c7e57c.qube_52d8b82b2d as qube_52d8b82b2d
from project.models import UserProfile
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_3b21db79ac
from project.sparta_b16f09cf2c.sparta_d1706a9539.qube_2e517c0aa5 import sparta_7186cea0a2


@sparta_3b21db79ac
@login_required(redirect_field_name='login')
def sparta_70299acce0(request, idSection=1):
    """
    
    """
    user_profile_obj = UserProfile.objects.get(user=request.user)
    avatar_obj = user_profile_obj.avatar
    if avatar_obj is not None:
        avatar_obj = user_profile_obj.avatar.avatar
    url_terms = urlparse(conf_settings.URL_TERMS)
    if not url_terms.scheme:
        url_terms = urlunparse(url_terms._replace(scheme='http'))
    resDict = {'item': 1, 'idSection': idSection, 'userProfil':
        user_profile_obj, 'avatar': avatar_obj, 'url_terms': url_terms}
    dictVar = qube_52d8b82b2d.sparta_5c1489406e(request)
    dictVar.update(qube_52d8b82b2d.sparta_35c7890672(request.user))
    dictVar.update(resDict)
    accessKey = ''
    dictVar['accessKey'] = accessKey
    dictVar['menuBar'] = 4
    dictVar.update(sparta_7186cea0a2())
    return render(request, 'dist/project/auth/settings.html', dictVar)

#END OF QUBE
