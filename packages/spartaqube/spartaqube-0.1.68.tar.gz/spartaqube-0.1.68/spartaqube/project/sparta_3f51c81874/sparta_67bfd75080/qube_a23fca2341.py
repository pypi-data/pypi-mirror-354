_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_8688631f3d.sparta_3a8c9165e9 import qube_66f961b03e as qube_66f961b03e
from project.sparta_8688631f3d.sparta_e898c07326 import qube_cc0a932d45 as qube_cc0a932d45
from project.sparta_8688631f3d.sparta_227f7b5cfa.qube_bd5e6b73de import sparta_235494f98c
@csrf_exempt
@sparta_235494f98c
def sparta_be9291e3eb(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_cc0a932d45.sparta_7c45ca35f6(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_66f961b03e.sparta_be9291e3eb(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_235494f98c
def sparta_d567909fd7(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_66f961b03e.sparta_ab5840d0ad(C,A.user);E=json.dumps(D);return HttpResponse(E)