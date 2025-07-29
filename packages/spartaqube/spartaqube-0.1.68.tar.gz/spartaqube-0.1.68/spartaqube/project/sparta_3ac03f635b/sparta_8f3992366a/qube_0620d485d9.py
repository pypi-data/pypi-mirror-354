_K='bPublicUser'
_J='notebook_name'
_I='notebook_id'
_H='b_require_password'
_G='notebook_obj'
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
import project.sparta_ef90090f65.sparta_40861746d9.qube_380ad6266d as qube_380ad6266d
from project.sparta_8688631f3d.sparta_227f7b5cfa.qube_bd5e6b73de import sparta_70de70e39d
from project.sparta_8688631f3d.sparta_bbb8926efe import qube_f161d2fcc5 as qube_f161d2fcc5
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_f0d228f17a import sparta_ca71f9cc05
@csrf_exempt
@sparta_70de70e39d
@login_required(redirect_field_name='login')
def sparta_7c6fcf0603(request):
	B=request;A=qube_380ad6266d.sparta_f8c7f58a23(B);A[_D]=13;D=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(D);A[_E]=_A
	def E(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	F=sparta_ca71f9cc05();C=os.path.join(F,'notebook');E(C);A[_F]=C;return render(B,'dist/project/notebook/notebook.html',A)
@csrf_exempt
def sparta_79512b3caa(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_f161d2fcc5.sparta_a96c3cc42e(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_7c6fcf0603(B)
	A=qube_380ad6266d.sparta_f8c7f58a23(B);A[_D]=12;H=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(H);A[_E]=_A;F=E[_G];A[_F]=F.project_path;A[_H]=0 if E[_C]==1 else 1;A[_I]=F.notebook_id;A[_J]=F.name;A[_K]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookRun.html',A)
@csrf_exempt
@sparta_70de70e39d
@login_required(redirect_field_name='login')
def sparta_cfe52c9c10(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_f161d2fcc5.sparta_a96c3cc42e(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_7c6fcf0603(B)
	A=qube_380ad6266d.sparta_f8c7f58a23(B);A[_D]=12;H=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(H);A[_E]=_A;F=E[_G];A[_F]=F.project_path;A[_H]=0 if E[_C]==1 else 1;A[_I]=F.notebook_id;A[_J]=F.name;A[_K]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookDetached.html',A)