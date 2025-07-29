_I='error.txt'
_H='zipName'
_G='utf-8'
_F='attachment; filename={0}'
_E='appId'
_D='res'
_C='Content-Disposition'
_B='projectPath'
_A='jsonData'
import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8688631f3d.sparta_052047303e import qube_ece8a50f88 as qube_ece8a50f88
from project.sparta_8688631f3d.sparta_052047303e import qube_81c5c91c22 as qube_81c5c91c22
from project.sparta_8688631f3d.sparta_c77f2d3c37 import qube_8f0cad92aa as qube_8f0cad92aa
from project.sparta_8688631f3d.sparta_227f7b5cfa.qube_bd5e6b73de import sparta_235494f98c
@csrf_exempt
@sparta_235494f98c
def sparta_c1b3936773(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_ece8a50f88.sparta_0f6b0c20d4(E,A.user,B[D])
	else:C={_D:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_235494f98c
def sparta_49db4b1369(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ece8a50f88.sparta_04e906053c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_f670a97eed(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ece8a50f88.sparta_094b8ea9d6(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_4d6368b1e9(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ece8a50f88.sparta_7a34606202(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_45c3daa823(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_81c5c91c22.sparta_f5215bb051(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_2a6c853b4d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ece8a50f88.sparta_3dfc538588(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_e2bde9df84(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ece8a50f88.sparta_b8ebce9d04(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_6658aa2c56(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ece8a50f88.sparta_fa11e67a1d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_f94f2f8c68(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ece8a50f88.sparta_b5d7b678a5(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_1f5fe29af4(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_ece8a50f88.sparta_ee39ec7777(J,A.user)
	if C[_D]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_C]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_235494f98c
def sparta_ce90df6d4f(request):
	E='folderName';B=request;F=B.GET[_B];D=B.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};C=qube_ece8a50f88.sparta_f81b92c030(G,B.user)
	if C[_D]==1:H=C['zip'];I=C[_H];A=HttpResponse();A.write(H.getvalue());A[_C]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_C]=_F.format(K)
	return A
@csrf_exempt
@sparta_235494f98c
def sparta_3ded67e0fd(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_ece8a50f88.sparta_51ac70b2a9(F,B.user)
	if C[_D]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_C]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_C]=_F.format(J)
	return A