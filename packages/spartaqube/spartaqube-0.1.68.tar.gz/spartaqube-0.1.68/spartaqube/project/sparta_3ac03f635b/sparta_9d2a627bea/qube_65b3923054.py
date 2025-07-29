_L='bPublicUser'
_K='developer_name'
_J='b_require_password'
_I='developer_obj'
_H='dist/project/homepage/homepage.html'
_G='developer_id'
_F='default_project_path'
_E='bCodeMirror'
_D='menuBar'
_C='res'
_B=None
_A=True
import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from django.http import FileResponse,Http404
from urllib.parse import unquote
from django.conf import settings as conf_settings
import project.sparta_ef90090f65.sparta_40861746d9.qube_380ad6266d as qube_380ad6266d
from project.sparta_8688631f3d.sparta_227f7b5cfa.qube_bd5e6b73de import sparta_70de70e39d
from project.sparta_8688631f3d.sparta_68bfd7a828 import qube_d1459513cb as qube_d1459513cb
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_f0d228f17a import sparta_ca71f9cc05
@csrf_exempt
@sparta_70de70e39d
@login_required(redirect_field_name='login')
def sparta_cd8a30b91f(request):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_380ad6266d.sparta_f8c7f58a23(B);return render(B,_H,A)
	qube_d1459513cb.sparta_291c67af3a();A=qube_380ad6266d.sparta_f8c7f58a23(B);A[_D]=12;D=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(D);A[_E]=_A
	def E(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	F=sparta_ca71f9cc05();C=os.path.join(F,'developer');E(C);A[_F]=C;return render(B,'dist/project/developer/developer.html',A)
@csrf_exempt
def sparta_46740e73bf(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_380ad6266d.sparta_f8c7f58a23(B);return render(B,_H,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_d1459513cb.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_cd8a30b91f(B)
	A=qube_380ad6266d.sparta_f8c7f58a23(B);A[_D]=12;H=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(H);A[_E]=_A;F=E[_I];A[_F]=F.project_path;A[_J]=0 if E[_C]==1 else 1;A[_G]=F.developer_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/developer/developerRun.html',A)
@csrf_exempt
@sparta_70de70e39d
@login_required(redirect_field_name='login')
def sparta_326e8a91f8(request,id):
	B=request;print('OPEN DEVELOPER DETACHED')
	if id is _B:C=B.GET.get('id')
	else:C=id
	print(_G);print(C);D=False
	if C is _B:D=_A
	else:
		E=qube_d1459513cb.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	print('b_redirect_developer_db');print(D)
	if D:return sparta_cd8a30b91f(B)
	A=qube_380ad6266d.sparta_f8c7f58a23(B);A[_D]=12;H=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(H);A[_E]=_A;F=E[_I];A[_F]=F.project_path;A[_J]=0 if E[_C]==1 else 1;A[_G]=F.developer_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/developer/developerDetached.html',A)
def sparta_37a08c73d9(request,project_path,file_name):A=project_path;A=unquote(A);return serve(request,file_name,document_root=A)