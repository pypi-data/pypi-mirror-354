_A='jsonData'
import json,inspect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from project.sparta_8688631f3d.sparta_fc43b5961f import qube_cd0a3435e4 as qube_cd0a3435e4
from project.sparta_8688631f3d.sparta_227f7b5cfa.qube_bd5e6b73de import sparta_235494f98c
def sparta_8c09375d8e(request):A={'res':1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
@sparta_235494f98c
def sparta_aed4a1d8ba(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_cd0a3435e4.sparta_aed4a1d8ba(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_3e080a6378(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_cd0a3435e4.sparta_3e080a6378(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_235494f98c
def sparta_6be0e12d94(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_cd0a3435e4.sparta_6be0e12d94(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_235494f98c
def sparta_dab3f1afab(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_cd0a3435e4.sparta_dab3f1afab(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_83812ae9b4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_cd0a3435e4.sparta_83812ae9b4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_235494f98c
def sparta_bc0154ba4c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_cd0a3435e4.sparta_bc0154ba4c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_4a027b64df(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_cd0a3435e4.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_235494f98c
def sparta_c0bc2c4511(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_cd0a3435e4.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_37cc11c58c(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_cd0a3435e4.sparta_37cc11c58c(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_62a725473d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_cd0a3435e4.sparta_62a725473d(A,C);E=json.dumps(D);return HttpResponse(E)