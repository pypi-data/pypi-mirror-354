_P='Please send valid data'
_O='dist/project/auth/resetPasswordChange.html'
_N='captcha'
_M='cypress_tests@gmail.com'
_L='password'
_K='POST'
_J=False
_I='login'
_H='error'
_G='form'
_F='email'
_E='res'
_D='home'
_C='manifest'
_B='errorMsg'
_A=True
import json,hashlib,uuid
from datetime import datetime
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.urls import reverse
import project.sparta_ef90090f65.sparta_40861746d9.qube_380ad6266d as qube_380ad6266d
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_8688631f3d.sparta_227f7b5cfa.qube_bd5e6b73de import sparta_70de70e39d
from project.sparta_8688631f3d.sparta_227f7b5cfa import qube_bd5e6b73de as qube_bd5e6b73de
from project.sparta_3f51c81874.sparta_670411547c import qube_ed5065b409 as qube_ed5065b409
from project.models import LoginLocation,UserProfile
from project.logger_config import logger
def sparta_63f1298857():return{'bHasCompanyEE':-1}
def sparta_f8fbb0bedc(request):B=request;A=qube_380ad6266d.sparta_f8c7f58a23(B);A[_C]=qube_380ad6266d.sparta_a193455a5d();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_70de70e39d
def sparta_5790c4242c(request):
	C=request;B='/';A=C.GET.get(_I)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_bf8af43d88(C,A)
def sparta_0ef734bb9d(request,redirectUrl):return sparta_bf8af43d88(request,redirectUrl)
def sparta_bf8af43d88(request,redirectUrl):
	E=redirectUrl;A=request;logger.debug('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_J;H='Email or password incorrect'
	if A.method==_K:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_bd5e6b73de.sparta_d0741c9bde(F):return sparta_f8fbb0bedc(A)
				login(A,F);K,L=qube_380ad6266d.sparta_1907700568();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_380ad6266d.sparta_f8c7f58a23(A);B.update(qube_380ad6266d.sparta_4ea1ca7fc0(A));B[_C]=qube_380ad6266d.sparta_a193455a5d();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_63f1298857());return render(A,'dist/project/auth/login.html',B)
def sparta_a217b7eab8(request):
	B='public@spartaqube.com';A=User.objects.filter(email=B).all()
	if A.count()>0:C=A[0];login(request,C)
	return redirect(_D)
@sparta_70de70e39d
def sparta_da4877d878(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_J;F=qube_bd5e6b73de.sparta_8c4ea22fa1()
	if A.method==_K:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_bd5e6b73de.sparta_1701bd6cdf(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_bd5e6b73de.sparta_1d229e006b(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_380ad6266d.sparta_f8c7f58a23(A);C.update(qube_380ad6266d.sparta_4ea1ca7fc0(A));C[_C]=qube_380ad6266d.sparta_a193455a5d();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_63f1298857());return render(A,'dist/project/auth/registration.html',C)
def sparta_3fc2405594(request):A=request;B=qube_380ad6266d.sparta_f8c7f58a23(A);B[_C]=qube_380ad6266d.sparta_a193455a5d();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_62428453f3(request,token):
	A=request;B=qube_bd5e6b73de.sparta_fd8778976b(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_380ad6266d.sparta_f8c7f58a23(A);D[_C]=qube_380ad6266d.sparta_a193455a5d();return redirect(_I)
def sparta_29e33b7851(request):logout(request);return redirect(_I)
def sparta_bd823579c5():
	from project.models import PlotDBChartShared as B,PlotDBChart,DashboardShared as C,NotebookShared as D,KernelShared as E,DBConnectorUserShared as F;A=_M;print('Destroy cypress user');G=B.objects.filter(user__email=A).all()
	for H in G:H.delete()
	I=C.objects.filter(user__email=A).all()
	for J in I:J.delete()
	K=D.objects.filter(user__email=A).all()
	for L in K:L.delete()
	M=E.objects.filter(user__email=A).all()
	for N in M:N.delete()
	O=F.objects.filter(user__email=A).all()
	for P in O:P.delete()
def sparta_77d64b0793(request):
	A=request;B=_M;sparta_bd823579c5();from project.sparta_8688631f3d.sparta_2a93ddec7a.qube_4aa09eb72d import sparta_ff2e12028b as C;C()
	if A.user.is_authenticated:
		if A.user.email==B:A.user.delete()
	logout(A);return redirect(_I)
def sparta_73e6ce4171(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_8980aad884(request):
	A=request;E='';F=_J
	if A.method==_K:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_N];G=qube_bd5e6b73de.sparta_8980aad884(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_380ad6266d.sparta_f8c7f58a23(A);C.update(qube_380ad6266d.sparta_4ea1ca7fc0(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_380ad6266d.sparta_a193455a5d();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_O,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:logger.debug('exception ');logger.debug(J);E='Could not send reset email, please try again';F=_A
		else:E=_P;F=_A
	else:B=ResetPasswordForm()
	D=qube_380ad6266d.sparta_f8c7f58a23(A);D.update(qube_380ad6266d.sparta_4ea1ca7fc0(A));D[_C]=qube_380ad6266d.sparta_a193455a5d();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_63f1298857());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_9ba81b2163(request):
	D=request;E='';B=_J
	if D.method==_K:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_N];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_bd5e6b73de.sparta_9ba81b2163(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_P;B=_A
	else:return redirect('reset-password')
	A=qube_380ad6266d.sparta_f8c7f58a23(D);A.update(qube_380ad6266d.sparta_4ea1ca7fc0(D));A[_C]=qube_380ad6266d.sparta_a193455a5d();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_63f1298857());return render(D,_O,A)