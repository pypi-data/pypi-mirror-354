_O='serialized_data'
_N='has_access'
_M='plot_name'
_L='plot_chart_id'
_K='plot_db_chart_obj'
_J='dist/project/plot-db/plotDB.html'
_I='edit_chart_id'
_H='edit'
_G=False
_F='login'
_E='-1'
_D='bCodeMirror'
_C='menuBar'
_B=None
_A=True
import json,base64
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_ef90090f65.sparta_40861746d9.qube_380ad6266d as qube_380ad6266d
from project.sparta_8688631f3d.sparta_227f7b5cfa.qube_bd5e6b73de import sparta_70de70e39d
from project.sparta_8688631f3d.sparta_5d2f5154f8 import qube_82ff246dc8 as qube_82ff246dc8
from project.sparta_8688631f3d.sparta_228d11d5fe import qube_225a21bdf6 as qube_225a21bdf6
@csrf_exempt
@sparta_70de70e39d
@login_required(redirect_field_name=_F)
def sparta_67eb6e1149(request):
	B=request;C=B.GET.get(_H)
	if C is _B:C=_E
	A=qube_380ad6266d.sparta_f8c7f58a23(B);A[_C]=7;D=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(D);A[_D]=_A;A[_I]=C;return render(B,_J,A)
@csrf_exempt
@sparta_70de70e39d
@login_required(redirect_field_name=_F)
def sparta_eea402fbe5(request):
	B=request;C=B.GET.get(_H)
	if C is _B:C=_E
	A=qube_380ad6266d.sparta_f8c7f58a23(B);A[_C]=10;D=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(D);A[_D]=_A;A[_I]=C;return render(B,_J,A)
@csrf_exempt
@sparta_70de70e39d
@login_required(redirect_field_name=_F)
def sparta_24d413734b(request):
	B=request;C=B.GET.get(_H)
	if C is _B:C=_E
	A=qube_380ad6266d.sparta_f8c7f58a23(B);A[_C]=11;D=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(D);A[_D]=_A;A[_I]=C;return render(B,_J,A)
@csrf_exempt
@sparta_70de70e39d
@login_required(redirect_field_name=_F)
def sparta_7926132032(request):
	B=request;C=B.GET.get(_H)
	if C is _B:C=_E
	A=qube_380ad6266d.sparta_f8c7f58a23(B);A[_C]=15;D=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(D);A[_D]=_A;A[_I]=C;return render(B,_J,A)
@csrf_exempt
@sparta_70de70e39d
@login_required(redirect_field_name=_F)
def sparta_0d13619b2c(request):
	A=request;C=A.GET.get('id');D=_G
	if C is _B:D=_A
	else:E=qube_82ff246dc8.sparta_e21c76d7c7(C,A.user);D=not E[_N]
	if D:return sparta_67eb6e1149(A)
	B=qube_380ad6266d.sparta_f8c7f58a23(A);B[_C]=7;F=qube_380ad6266d.sparta_9fb18a0f07(A.user);B.update(F);B[_D]=_A;B[_L]=C;G=E[_K];B[_M]=G.name;return render(A,'dist/project/plot-db/plotFull.html',B)
@csrf_exempt
@sparta_70de70e39d
def sparta_01aacb9cb9(request,id,api_token_id=_B):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	return plot_widget_func(A,B)
@csrf_exempt
@sparta_70de70e39d
def sparta_2942a97bfb(request,dashboard_id,id,password):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	C=base64.b64decode(password).decode();return plot_widget_func(A,B,dashboard_id=dashboard_id,dashboard_password=C)
@csrf_exempt
@sparta_70de70e39d
def sparta_81b9088cd2(request,widget_id,session_id,api_token_id):return plot_widget_func(request,widget_id,session_id)
def plot_widget_func(request,plot_chart_id,session=_E,dashboard_id=_E,token_permission='',dashboard_password=_B):
	K='token_permission';I=dashboard_id;H=plot_chart_id;G='res';E=token_permission;D=request;C=_G
	if H is _B:C=_A
	else:
		B=qube_82ff246dc8.sparta_b64f60322d(H,D.user);F=B[G]
		if F==-1:C=_A
	if C:
		if I!=_E:
			B=qube_225a21bdf6.has_plot_db_access(I,H,D.user,dashboard_password);F=B[G]
			if F==1:E=B[K];C=_G
	if C:
		if len(E)>0:
			B=qube_82ff246dc8.sparta_b0d5903f1f(E);F=B[G]
			if F==1:C=_G
	if C:return sparta_67eb6e1149(D)
	A=qube_380ad6266d.sparta_f8c7f58a23(D);A[_C]=7;L=qube_380ad6266d.sparta_9fb18a0f07(D.user);A.update(L);A[_D]=_A;J=B[_K];A['b_require_password']=0 if B[G]==1 else 1;A[_L]=J.plot_chart_id;A[_M]=J.name;A['session']=str(session);A['is_dashboard_widget']=1 if I!=_E else 0;A['is_token']=1 if len(E)>0 else 0;A[K]=str(E);return render(D,'dist/project/plot-db/widgets.html',A)
@csrf_exempt
def sparta_6764852f6c(request,token):return plot_widget_func(request,plot_chart_id=_B,token_permission=token)
@csrf_exempt
@sparta_70de70e39d
def sparta_d22d987f79(request):B=request;A=qube_380ad6266d.sparta_f8c7f58a23(B);A[_C]=7;C=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(C);A[_D]=_A;A[_O]=B.POST.get('data');return render(B,'dist/project/plot-db/plotGUI.html',A)
@csrf_exempt
@sparta_70de70e39d
@login_required(redirect_field_name=_F)
def sparta_96258675e9(request,id):
	K=',\n    ';B=request;C=id;F=_G
	if C is _B:F=_A
	else:G=qube_82ff246dc8.sparta_e21c76d7c7(C,B.user);F=not G[_N]
	if F:return sparta_67eb6e1149(B)
	L=qube_82ff246dc8.sparta_26622c30d7(G[_K]);D='';H=0
	for(E,I)in L.items():
		if H>0:D+=K
		if I==1:D+=f"{E}=input_{E}"
		else:M=str(K.join([f"input_{E}_{A}"for A in range(I)]));D+=f"{E}=[{M}]"
		H+=1
	J=f"'{C}'";N=f"\n    {J}\n";O=f"Spartaqube().get_widget({N})";P=f"\n    {J},\n    {D}\n";Q=f"Spartaqube().plot({P})";A=qube_380ad6266d.sparta_f8c7f58a23(B);A[_C]=7;R=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(R);A[_D]=_A;A[_L]=C;S=G[_K];A[_M]=S.name;A['plot_data_cmd']=O;A['plot_data_cmd_inputs']=Q;return render(B,'dist/project/plot-db/plotGUISaved.html',A)
@csrf_exempt
@sparta_70de70e39d
def sparta_adb3609f25(request,json_vars_html):B=request;A=qube_380ad6266d.sparta_f8c7f58a23(B);A[_C]=7;C=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(C);A[_D]=_A;A.update(json.loads(json_vars_html));A[_O]=B.POST.get('data');return render(B,'dist/project/plot-db/plotAPI.html',A)
@csrf_exempt
@sparta_70de70e39d
def sparta_07b1205ab5(request):A={};return render(request,'dist/project/luckysheetIframe/luckysheet-frame.html',A)