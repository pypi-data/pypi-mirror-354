import json, base64
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_312a90fa32.sparta_6696c7e57c.qube_52d8b82b2d as qube_52d8b82b2d
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_3b21db79ac
from project.sparta_8345d6a892.sparta_26ea98fb42 import qube_b61b0eabde as qube_b61b0eabde
from project.sparta_8345d6a892.sparta_950a603163 import qube_2ab426de66 as qube_2ab426de66
from project.sparta_8345d6a892.sparta_0c79de9c55 import qube_2e0f0ad7f3 as qube_2e0f0ad7f3


@csrf_exempt
@sparta_3b21db79ac
@login_required(redirect_field_name='login')
def sparta_d363d742a7(request):
    """
    DataFrames
    """
    edit_chart_id = request.GET.get('edit')
    if edit_chart_id is None:
        edit_chart_id = '-1'
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 15
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True
    dict_var['edit_chart_id'] = edit_chart_id
    return render(request, 'dist/project/plot-db/plotDB.html', dict_var)


@csrf_exempt
@sparta_3b21db79ac
def sparta_c24ffe1d26(request, id, api_token_id=None):
    """
    Plot Widget
    Do not need to @sparta_3b21db79ac as we can query public widget. The method has_widget_access will test if 
    user has rights to access the widget 
    """
    if id is None:
        slug = request.GET.get('id')
    else:
        slug = id
    return plot_widget_dataframes_func(request, slug)


@csrf_exempt
@sparta_3b21db79ac
def sparta_225de7c9f4(request, dashboard_id, id, password):
    """
    DataFrame Widget
    Do not need to @sparta_3b21db79ac as we can query public widget. The method has_widget_access will test if 
    user has rights to access the widget 
    """
    if id is None:
        slug = request.GET.get('id')
    else:
        slug = id
    dashboard_password = base64.b64decode(password).decode()
    print('plot widget dadshboard')
    return plot_widget_dataframes_func(request, slug, dashboard_id=
        dashboard_id, dashboard_password=dashboard_password)


def plot_widget_dataframes_func(request, slug, session='-1', dashboard_id=
    '-1', token_permission='', dashboard_password=None):
    """
    
    """
    b_redirect_plot_db_dataframe = False
    if slug is None:
        b_redirect_plot_db_dataframe = True
    else:
        widget_access_dict = qube_2ab426de66.sparta_2901e6f78f(slug,
            request.user)
        res_access = widget_access_dict['res']
        if res_access == -1:
            b_redirect_plot_db_dataframe = True
    if b_redirect_plot_db_dataframe:
        if dashboard_id != '-1':
            widget_access_dict = qube_2e0f0ad7f3.has_dataframe_access(
                dashboard_id, slug, request.user, dashboard_password)
            res_access = widget_access_dict['res']
            if res_access == 1:
                token_permission = widget_access_dict['token_permission']
                b_redirect_plot_db_dataframe = False
    if b_redirect_plot_db_dataframe:
        if len(token_permission) > 0:
            widget_access_dict = (qube_2ab426de66.sparta_9f46127e8e(token_permission))
            res_access = widget_access_dict['res']
            if res_access == 1:
                b_redirect_plot_db_dataframe = False
    if b_redirect_plot_db_dataframe:
        return sparta_d363d742a7(request)
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 15
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True
    dataframe_model_obj = widget_access_dict['dataframe_model_obj']
    dict_var['b_require_password'] = 0 if widget_access_dict['res'] == 1 else 1
    dict_var['slug'] = dataframe_model_obj.slug
    dict_var['dataframe_model_name'] = dataframe_model_obj.table_name
    dict_var['session'] = str(session)
    dict_var['is_dashboard_widget'] = 1 if dashboard_id != '-1' else 0
    dict_var['is_token'] = 1 if len(token_permission) > 0 else 0
    dict_var['token_permission'] = str(token_permission)
    return render(request, 'dist/project/dataframes/dataframes.html', dict_var)


@csrf_exempt
@sparta_3b21db79ac
def sparta_8294d71010(request, id, api_token_id=None):
    """
    Plot Widget
    Do not need to @sparta_3b21db79ac as we can query public widget. The method has_widget_access will test if 
    user has rights to access the widget 
    """
    if id is None:
        slug = request.GET.get('id')
    else:
        slug = id
    return plot_widget_dataframes_func(request, slug)


@csrf_exempt
def sparta_241009e073(request, token):
    """
    Plot Widget using token (This is required for the internal API (or dashboard/notebook) when user runs get_widget('...')
    within the kernel). Why is it needed ?
    If the user share a notebook (public w/o password or to a user), the execution of the kernel code is done as the owner.But for the iframe, we must connect (logged) as the user owner which is problematic. Instead, we are using this token valid 
    for couple of minutes to access the widget."""
    return plot_widget_dataframes_func(request, slug=None, token_permission
        =token)


@csrf_exempt
@sparta_3b21db79ac
def sparta_628d5405c5(request):
    """
    Start new SpartaQube interactive plot session for DataFrame
    """
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 7
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True
    dict_var['serialized_data'] = request.POST.get('data')
    dict_var['name'] = request.POST.get('name')
    return render(request, 'dist/project/dataframes/plotDataFramesGUI.html',
        dict_var)

#END OF QUBE
