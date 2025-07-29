_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8688631f3d.sparta_227f7b5cfa import qube_bd5e6b73de as qube_bd5e6b73de
from project.sparta_ef90090f65.sparta_40861746d9.qube_380ad6266d import sparta_6ae4813892
from project.logger_config import logger
@csrf_exempt
def sparta_1d229e006b(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_bd5e6b73de.sparta_1d229e006b(B)
@csrf_exempt
def sparta_041968efb3(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_457cbe8b01(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_10a0ec2b12(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)