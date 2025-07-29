from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8688631f3d.sparta_227f7b5cfa.qube_bd5e6b73de import sparta_70de70e39d
from project.sparta_8688631f3d.sparta_e898c07326 import qube_cc0a932d45 as qube_cc0a932d45
from project.models import UserProfile
import project.sparta_ef90090f65.sparta_40861746d9.qube_380ad6266d as qube_380ad6266d
@sparta_70de70e39d
@login_required(redirect_field_name='login')
def sparta_d2f6424ac1(request):
	E='avatarImg';B=request;A=qube_380ad6266d.sparta_f8c7f58a23(B);A['menuBar']=-1;F=qube_380ad6266d.sparta_9fb18a0f07(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_70de70e39d
@login_required(redirect_field_name='login')
def sparta_b3dda8a414(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_d2f6424ac1(A)