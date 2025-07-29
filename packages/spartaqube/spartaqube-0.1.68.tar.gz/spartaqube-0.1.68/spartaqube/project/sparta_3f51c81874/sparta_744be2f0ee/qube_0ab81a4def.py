_E='Content-Disposition'
_D='utf-8'
_C='dashboardId'
_B='projectPath'
_A='jsonData'
import os,json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8688631f3d.sparta_9df5aeb023 import qube_69643efa56 as qube_69643efa56
from project.sparta_8688631f3d.sparta_9df5aeb023 import qube_2ee3065b9a as qube_2ee3065b9a
from project.sparta_8688631f3d.sparta_228d11d5fe import qube_225a21bdf6 as qube_225a21bdf6
from project.sparta_8688631f3d.sparta_227f7b5cfa.qube_bd5e6b73de import sparta_235494f98c,sparta_e7e32d3111
@csrf_exempt
def sparta_972a97df58(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_69643efa56.sparta_972a97df58(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_4fca1c890c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_69643efa56.sparta_4fca1c890c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_8c81f8dd3d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_69643efa56.sparta_8c81f8dd3d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_b176389378(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_69643efa56.sparta_b176389378(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
@sparta_e7e32d3111
def sparta_8e228ce9df(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_69643efa56.sparta_8e228ce9df(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_c31124a4c6(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_69643efa56.sparta_c31124a4c6(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_4a3bf7f1c2(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_69643efa56.sparta_4a3bf7f1c2(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_e1c56660b3(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_69643efa56.sparta_e1c56660b3(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_5ebd3cc888(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_69643efa56.sparta_5ebd3cc888(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_ff286b9290(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_69643efa56.sparta_ff286b9290(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_68623bf58b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_69643efa56.dashboard_project_explorer_delete_multiple_resources(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_492c1f66ea(request):A=request;B=A.POST.dict();C=A.FILES;D=qube_69643efa56.sparta_492c1f66ea(B,A.user,C['files[]']);E=json.dumps(D);return HttpResponse(E)
def sparta_deb8e914be(path):
	A=path;A=os.path.normpath(A)
	if os.path.isfile(A):A=os.path.dirname(A)
	return os.path.basename(A)
def sparta_ee129f8317(path):A=path;A=os.path.normpath(A);return os.path.basename(A)
@csrf_exempt
@sparta_235494f98c
def sparta_b334132de1(request):
	E='pathResource';A=request;B=A.GET[E];B=base64.b64decode(B).decode(_D);F=A.GET[_B];G=A.GET[_C];H=sparta_ee129f8317(B);I={E:B,_C:G,_B:base64.b64decode(F).decode(_D)};C=qube_69643efa56.sparta_ee39ec7777(I,A.user)
	if C['res']==1:
		try:
			with open(C['fullPath'],'rb')as J:D=HttpResponse(J.read(),content_type='application/force-download');D[_E]='attachment; filename='+str(H);return D
		except Exception as K:pass
	raise Http404
@csrf_exempt
@sparta_235494f98c
def sparta_038e980b66(request):
	D='attachment; filename={0}';B=request;E=B.GET[_C];F=B.GET[_B];G={_C:E,_B:base64.b64decode(F).decode(_D)};C=qube_69643efa56.sparta_51ac70b2a9(G,B.user)
	if C['res']==1:H=C['zip'];I=C['zipName'];A=HttpResponse();A.write(H.getvalue());A[_E]=D.format(f"{I}.zip")
	else:A=HttpResponse();J='Could not download the application, please try again';K='error.txt';A.write(J);A[_E]=D.format(K)
	return A
@csrf_exempt
@sparta_235494f98c
@sparta_e7e32d3111
def sparta_1c47602a7c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2ee3065b9a.sparta_1c47602a7c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
@sparta_e7e32d3111
def sparta_7c5ba0aab5(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2ee3065b9a.sparta_7c5ba0aab5(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
@sparta_e7e32d3111
def sparta_38b55686b5(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2ee3065b9a.sparta_38b55686b5(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
@sparta_e7e32d3111
def sparta_f29b5b201a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2ee3065b9a.sparta_f29b5b201a(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
@sparta_e7e32d3111
def sparta_cd94deb95d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2ee3065b9a.sparta_cd94deb95d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
@sparta_e7e32d3111
def sparta_60c8427df1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2ee3065b9a.sparta_60c8427df1(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
@sparta_e7e32d3111
def sparta_4a62382ea2(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2ee3065b9a.sparta_4a62382ea2(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
@sparta_e7e32d3111
def sparta_3d8862f77e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2ee3065b9a.sparta_3d8862f77e(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
@sparta_e7e32d3111
def sparta_984881fb99(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2ee3065b9a.sparta_984881fb99(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
@sparta_e7e32d3111
def sparta_0abc955a62(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2ee3065b9a.sparta_0abc955a62(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
@sparta_e7e32d3111
def sparta_99312812bc(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2ee3065b9a.sparta_99312812bc(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
@sparta_e7e32d3111
def sparta_f098c8d833(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2ee3065b9a.sparta_f098c8d833(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
@sparta_e7e32d3111
def sparta_e1a0528b33(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2ee3065b9a.sparta_e1a0528b33(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
@sparta_e7e32d3111
def sparta_a235d0af16(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2ee3065b9a.sparta_a235d0af16(C,A.user);E=json.dumps(D);return HttpResponse(E)