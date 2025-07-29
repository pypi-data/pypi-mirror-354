import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
import project.sparta_ef90090f65.sparta_40861746d9.qube_380ad6266d as qube_380ad6266d
from project.sparta_8688631f3d.sparta_227f7b5cfa.qube_bd5e6b73de import sparta_70de70e39d
from project.sparta_8688631f3d.sparta_5d2f5154f8 import qube_82ff246dc8 as qube_82ff246dc8
from project.sparta_8688631f3d.sparta_228d11d5fe import qube_225a21bdf6 as qube_225a21bdf6
def sparta_af7fb9ae39():
	A=platform.system()
	if A=='Windows':return'windows'
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_70de70e39d
@login_required(redirect_field_name='login')
def sparta_aad96da05b(request):
	E='template';D='developer';B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_380ad6266d.sparta_f8c7f58a23(B);return render(B,'dist/project/homepage/homepage.html',A)
	A=qube_380ad6266d.sparta_f8c7f58a23(B);A['menuBar']=12;F=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(F);A['bCodeMirror']=True;G=os.path.dirname(__file__);C=os.path.dirname(os.path.dirname(G));H=os.path.join(C,'static');I=os.path.join(H,'js',D,E,'frontend');A['frontend_path']=I;J=os.path.dirname(C);K=os.path.join(J,'django_app_template',D,E,'backend');A['backend_path']=K;return render(B,'dist/project/developer/developerExamples.html',A)