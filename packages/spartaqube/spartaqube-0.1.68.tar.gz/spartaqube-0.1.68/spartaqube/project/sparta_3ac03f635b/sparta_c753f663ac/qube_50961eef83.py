_C='bCodeMirror'
_B='menuBar'
_A=True
import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_ef90090f65.sparta_40861746d9.qube_380ad6266d as qube_380ad6266d
from project.sparta_8688631f3d.sparta_227f7b5cfa.qube_bd5e6b73de import sparta_70de70e39d
from project.sparta_8688631f3d.sparta_5d2f5154f8 import qube_82ff246dc8 as qube_82ff246dc8
from project.sparta_8688631f3d.sparta_228d11d5fe import qube_225a21bdf6 as qube_225a21bdf6
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_f0d228f17a import sparta_ca71f9cc05
@csrf_exempt
@sparta_70de70e39d
@login_required(redirect_field_name='login')
def sparta_fd7beacc39(request):
	B=request;C=B.GET.get('edit')
	if C is None:C='-1'
	A=qube_380ad6266d.sparta_f8c7f58a23(B);A[_B]=9;E=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(E);A[_C]=_A;A['edit_chart_id']=C
	def F(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	G=sparta_ca71f9cc05();D=os.path.join(G,'dashboard');F(D);A['default_project_path']=D;return render(B,'dist/project/dashboard/dashboard.html',A)
@csrf_exempt
def sparta_61c8e65bfb(request,id):
	A=request
	if id is None:B=A.GET.get('id')
	else:B=id
	return sparta_5d32337712(A,B)
def sparta_5d32337712(request,dashboard_id,session='-1'):
	G='res';E=dashboard_id;B=request;C=False
	if E is None:C=_A
	else:
		D=qube_225a21bdf6.has_dashboard_access(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_fd7beacc39(B)
	A=qube_380ad6266d.sparta_f8c7f58a23(B);A[_B]=9;I=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(I);A[_C]=_A;F=D['dashboard_obj'];A['b_require_password']=0 if D[G]==1 else 1;A['dashboard_id']=F.dashboard_id;A['dashboard_name']=F.name;A['bPublicUser']=B.user.is_anonymous;A['session']=str(session);return render(B,'dist/project/dashboard/dashboardRun.html',A)