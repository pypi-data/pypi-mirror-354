from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_ef90090f65.sparta_40861746d9.qube_380ad6266d as qube_380ad6266d
from project.models import UserProfile
from project.sparta_8688631f3d.sparta_227f7b5cfa.qube_bd5e6b73de import sparta_70de70e39d
from project.sparta_3ac03f635b.sparta_d55ffa7824.qube_a9b066fc0a import sparta_63f1298857
@sparta_70de70e39d
@login_required(redirect_field_name='login')
def sparta_a8852b9e80(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_380ad6266d.sparta_f8c7f58a23(B);A.update(qube_380ad6266d.sparta_9fb18a0f07(B.user));A.update(F);G='';A['accessKey']=G;A['menuBar']=4;A.update(sparta_63f1298857());return render(B,'dist/project/auth/settings.html',A)