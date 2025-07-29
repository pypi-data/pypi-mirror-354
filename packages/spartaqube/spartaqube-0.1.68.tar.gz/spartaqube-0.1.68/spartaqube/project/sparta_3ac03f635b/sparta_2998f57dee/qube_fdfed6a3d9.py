_E='bCodeMirror'
_D='menuBar'
_C=True
_B='-1'
_A=None
import json,base64
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_ef90090f65.sparta_40861746d9.qube_380ad6266d as qube_380ad6266d
from project.sparta_8688631f3d.sparta_227f7b5cfa.qube_bd5e6b73de import sparta_70de70e39d
from project.sparta_8688631f3d.sparta_5d2f5154f8 import qube_82ff246dc8 as qube_82ff246dc8
from project.sparta_8688631f3d.sparta_8c6a44fbc0 import qube_d70996b7fa as qube_d70996b7fa
from project.sparta_8688631f3d.sparta_228d11d5fe import qube_225a21bdf6 as qube_225a21bdf6
@csrf_exempt
@sparta_70de70e39d
@login_required(redirect_field_name='login')
def sparta_7926132032(request):
	B=request;C=B.GET.get('edit')
	if C is _A:C=_B
	A=qube_380ad6266d.sparta_f8c7f58a23(B);A[_D]=15;D=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(D);A[_E]=_C;A['edit_chart_id']=C;return render(B,'dist/project/plot-db/plotDB.html',A)
@csrf_exempt
@sparta_70de70e39d
def sparta_97ab9d0b41(request,id,api_token_id=_A):
	A=request
	if id is _A:B=A.GET.get('id')
	else:B=id
	return plot_widget_dataframes_func(A,B)
@csrf_exempt
@sparta_70de70e39d
def sparta_2942a97bfb(request,dashboard_id,id,password):
	A=request
	if id is _A:B=A.GET.get('id')
	else:B=id
	C=base64.b64decode(password).decode();print('plot widget dadshboard');return plot_widget_dataframes_func(A,B,dashboard_id=dashboard_id,dashboard_password=C)
def plot_widget_dataframes_func(request,slug,session=_B,dashboard_id=_B,token_permission='',dashboard_password=_A):
	L='token_permission';J=False;I=dashboard_id;H=slug;G='res';E=token_permission;D=request;C=J
	if H is _A:C=_C
	else:
		B=qube_d70996b7fa.sparta_b64f60322d(H,D.user);F=B[G]
		if F==-1:C=_C
	if C:
		if I!=_B:
			B=qube_225a21bdf6.has_dataframe_access(I,H,D.user,dashboard_password);F=B[G]
			if F==1:E=B[L];C=J
	if C:
		if len(E)>0:
			B=qube_d70996b7fa.sparta_b0d5903f1f(E);F=B[G]
			if F==1:C=J
	if C:return sparta_7926132032(D)
	A=qube_380ad6266d.sparta_f8c7f58a23(D);A[_D]=15;M=qube_380ad6266d.sparta_9fb18a0f07(D.user);A.update(M);A[_E]=_C;K=B['dataframe_model_obj'];A['b_require_password']=0 if B[G]==1 else 1;A['slug']=K.slug;A['dataframe_model_name']=K.table_name;A['session']=str(session);A['is_dashboard_widget']=1 if I!=_B else 0;A['is_token']=1 if len(E)>0 else 0;A[L]=str(E);return render(D,'dist/project/dataframes/dataframes.html',A)
@csrf_exempt
@sparta_70de70e39d
def sparta_2886ef55be(request,id,api_token_id=_A):
	A=request
	if id is _A:B=A.GET.get('id')
	else:B=id
	return plot_widget_dataframes_func(A,B)
@csrf_exempt
def sparta_a26bfe2bdd(request,token):return plot_widget_dataframes_func(request,slug=_A,token_permission=token)
@csrf_exempt
@sparta_70de70e39d
def sparta_cbe7fbc0d4(request):C='name';B=request;A=qube_380ad6266d.sparta_f8c7f58a23(B);A[_D]=7;D=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(D);A[_E]=_C;A['serialized_data']=B.POST.get('data');A[C]=B.POST.get(C);return render(B,'dist/project/dataframes/plotDataFramesGUI.html',A)