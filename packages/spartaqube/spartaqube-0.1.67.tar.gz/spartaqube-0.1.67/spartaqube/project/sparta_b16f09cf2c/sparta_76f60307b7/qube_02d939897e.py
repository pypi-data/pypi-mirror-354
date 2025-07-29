from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_312a90fa32.sparta_6696c7e57c.qube_52d8b82b2d as qube_52d8b82b2d
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_3b21db79ac


@csrf_exempt
@sparta_3b21db79ac
@login_required(redirect_field_name='login')
def sparta_3b351d15c1(request):
    """
    View Homepage Welcome back
    """
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = -1
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    return render(request, 'dist/project/homepage/homepage.html', dict_var)

#END OF QUBE
