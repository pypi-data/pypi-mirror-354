_A='menuBar'
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
from project.sparta_8688631f3d.sparta_2a93ddec7a import qube_4aa09eb72d as qube_4aa09eb72d
from project.sparta_8688631f3d.sparta_9df5aeb023 import qube_4009e9a33a as qube_4009e9a33a
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_f0d228f17a import sparta_ca71f9cc05
@csrf_exempt
@sparta_70de70e39d
@login_required(redirect_field_name='login')
def sparta_86d29af3c4(request):A=request;B=qube_380ad6266d.sparta_f8c7f58a23(A);B[_A]=-1;C=qube_380ad6266d.sparta_9fb18a0f07(A.user);B.update(C);return render(A,'dist/project/homepage/homepage.html',B)
@csrf_exempt
@sparta_70de70e39d
@login_required(redirect_field_name='login')
def sparta_299e37118d(request,kernel_manager_uuid):
	D=kernel_manager_uuid;C=True;B=request;E=False
	if D is None:E=C
	else:
		F=qube_4aa09eb72d.sparta_1b457f9dcf(B.user,D)
		if F is None:E=C
	if E:return sparta_86d29af3c4(B)
	def H(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=C)
	K=sparta_ca71f9cc05();G=os.path.join(K,'kernel');H(G);I=os.path.join(G,D);H(I);J=os.path.join(I,'main.ipynb')
	if not os.path.exists(J):
		L=qube_4009e9a33a.sparta_4a275ac0ae()
		with open(J,'w')as M:M.write(json.dumps(L))
	A=qube_380ad6266d.sparta_f8c7f58a23(B);A['default_project_path']=G;A[_A]=-1;N=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(N);A['kernel_name']=F.name;A['kernelManagerUUID']=F.kernel_manager_uuid;A['bCodeMirror']=C;A['bPublicUser']=B.user.is_anonymous;return render(B,'dist/project/sqKernelNotebook/sqKernelNotebook.html',A)