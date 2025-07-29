import json, base64
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_312a90fa32.sparta_6696c7e57c.qube_52d8b82b2d as qube_52d8b82b2d
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_3b21db79ac
from project.sparta_8345d6a892.sparta_26ea98fb42 import qube_b61b0eabde as qube_b61b0eabde
from project.sparta_8345d6a892.sparta_0c79de9c55 import qube_2e0f0ad7f3 as qube_2e0f0ad7f3


@csrf_exempt
@sparta_3b21db79ac
@login_required(redirect_field_name='login')
def sparta_e6b7b1300d(request):
    """
    Plot DB
    """
    edit_chart_id = request.GET.get('edit')
    if edit_chart_id is None:
        edit_chart_id = '-1'
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 7
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True
    dict_var['edit_chart_id'] = edit_chart_id
    return render(request, 'dist/project/plot-db/plotDB.html', dict_var)


@csrf_exempt
@sparta_3b21db79ac
@login_required(redirect_field_name='login')
def sparta_b7ee9d977f(request):
    """
    Connectors
    """
    edit_chart_id = request.GET.get('edit')
    if edit_chart_id is None:
        edit_chart_id = '-1'
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 10
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True
    dict_var['edit_chart_id'] = edit_chart_id
    return render(request, 'dist/project/plot-db/plotDB.html', dict_var)


@csrf_exempt
@sparta_3b21db79ac
@login_required(redirect_field_name='login')
def sparta_5d2620bafe(request):
    """
    Widgets
    """
    edit_chart_id = request.GET.get('edit')
    if edit_chart_id is None:
        edit_chart_id = '-1'
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 11
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True
    dict_var['edit_chart_id'] = edit_chart_id
    return render(request, 'dist/project/plot-db/plotDB.html', dict_var)


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
@login_required(redirect_field_name='login')
def sparta_7f1252ed6c(request):
    """
    DEPRECATED
    Plot Chart Full Screen
    """
    plot_chart_id = request.GET.get('id')
    b_redirect_plot_db = False
    if plot_chart_id is None:
        b_redirect_plot_db = True
    else:
        has_access_dict = qube_b61b0eabde.sparta_933c6bec3f(plot_chart_id,
            request.user)
        b_redirect_plot_db = not has_access_dict['has_access']
    if b_redirect_plot_db:
        return sparta_e6b7b1300d(request)
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 7
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True
    dict_var['plot_chart_id'] = plot_chart_id
    plot_db_chart_obj = has_access_dict['plot_db_chart_obj']
    dict_var['plot_name'] = plot_db_chart_obj.name
    return render(request, 'dist/project/plot-db/plotFull.html', dict_var)


@csrf_exempt
@sparta_3b21db79ac
def sparta_e4fae4da26(request, id, api_token_id=None):
    """
    Plot Widget
    Do not need to @sparta_3b21db79ac as we can query public widget. The method has_widget_access will test if 
    user has rights to access the widget 
    """
    if id is None:
        plot_chart_id = request.GET.get('id')
    else:
        plot_chart_id = id
    return plot_widget_func(request, plot_chart_id)


@csrf_exempt
@sparta_3b21db79ac
def sparta_225de7c9f4(request, dashboard_id, id, password):
    """
    Plot Widget
    Do not need to @sparta_3b21db79ac as we can query public widget. The method has_widget_access will test if 
    user has rights to access the widget 
    """
    if id is None:
        plot_chart_id = request.GET.get('id')
    else:
        plot_chart_id = id
    dashboard_password = base64.b64decode(password).decode()
    return plot_widget_func(request, plot_chart_id, dashboard_id=
        dashboard_id, dashboard_password=dashboard_password)


@csrf_exempt
@sparta_3b21db79ac
def sparta_a1613bd1ec(request, widget_id, session_id, api_token_id):
    """
    Plot Template Widget
    Do not need to @sparta_3b21db79ac as we can query public widget. The method has_widget_access will test if 
    user has rights to access the widget 
    """
    return plot_widget_func(request, widget_id, session_id)


def plot_widget_func(request, plot_chart_id, session='-1', dashboard_id=
    '-1', token_permission='', dashboard_password=None):
    """
    
    """
    b_redirect_plot_db = False
    if plot_chart_id is None:
        b_redirect_plot_db = True
    else:
        widget_access_dict = qube_b61b0eabde.sparta_2901e6f78f(plot_chart_id,
            request.user)
        res_access = widget_access_dict['res']
        if res_access == -1:
            b_redirect_plot_db = True
    if b_redirect_plot_db:
        if dashboard_id != '-1':
            widget_access_dict = qube_2e0f0ad7f3.has_plot_db_access(
                dashboard_id, plot_chart_id, request.user, dashboard_password)
            res_access = widget_access_dict['res']
            if res_access == 1:
                token_permission = widget_access_dict['token_permission']
                b_redirect_plot_db = False
    if b_redirect_plot_db:
        if len(token_permission) > 0:
            widget_access_dict = (qube_b61b0eabde.sparta_9f46127e8e(token_permission))
            res_access = widget_access_dict['res']
            if res_access == 1:
                b_redirect_plot_db = False
    if b_redirect_plot_db:
        return sparta_e6b7b1300d(request)
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 7
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True
    plot_db_chart_obj = widget_access_dict['plot_db_chart_obj']
    dict_var['b_require_password'] = 0 if widget_access_dict['res'] == 1 else 1
    dict_var['plot_chart_id'] = plot_db_chart_obj.plot_chart_id
    dict_var['plot_name'] = plot_db_chart_obj.name
    dict_var['session'] = str(session)
    dict_var['is_dashboard_widget'] = 1 if dashboard_id != '-1' else 0
    dict_var['is_token'] = 1 if len(token_permission) > 0 else 0
    dict_var['token_permission'] = str(token_permission)
    return render(request, 'dist/project/plot-db/widgets.html', dict_var)


@csrf_exempt
def sparta_e0cbaf17d7(request, token):
    """
    Plot Widget using token (This is required for the internal API (or dashboard/notebook) when user runs get_widget('...')
    within the kernel). Why is it needed ?
    If the user share a notebook (public w/o password or to a user), the execution of the kernel code is done as the owner.But for the iframe, we must connect (logged) as the user owner which is problematic. Instead, we are using this token valid 
    for couple of minutes to access the widget."""
    return plot_widget_func(request, plot_chart_id=None, token_permission=token
        )


@csrf_exempt
@sparta_3b21db79ac
def sparta_f59e64a352(request):
    """
    Start new SpartaQube interactive plot session
    """
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 7
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True
    dict_var['serialized_data'] = request.POST.get('data')
    return render(request, 'dist/project/plot-db/plotGUI.html', dict_var)


@csrf_exempt
@sparta_3b21db79ac
@login_required(redirect_field_name='login')
def sparta_8b97b4427a(request, id):
    """
    Plot Widget
    """
    plot_chart_id = id
    b_redirect_plot_db = False
    if plot_chart_id is None:
        b_redirect_plot_db = True
    else:
        has_access_dict = qube_b61b0eabde.sparta_933c6bec3f(plot_chart_id,
            request.user)
        b_redirect_plot_db = not has_access_dict['has_access']
    if b_redirect_plot_db:
        return sparta_e6b7b1300d(request)
    inputs_dict: int = qube_b61b0eabde.sparta_2e67d0450d(
        has_access_dict['plot_db_chart_obj'])
    inputs_structure_cmd = ''
    cnt = 0
    for key, val in inputs_dict.items():
        if cnt > 0:
            inputs_structure_cmd += ',\n    '
        if val == 1:
            inputs_structure_cmd += f'{key}=input_{key}'
        else:
            list_elem = str(',\n    '.join([f'input_{key}_{elem}' for elem in
                range(val)]))
            inputs_structure_cmd += f'{key}=[{list_elem}]'
        cnt += 1
    plot_chart_id_with_quote = f"'{plot_chart_id}'"
    get_widget_input_text = f"""
    {plot_chart_id_with_quote}
"""
    plot_data_cmd = f'Spartaqube().get_widget({get_widget_input_text})'
    plot_input_text = f"""
    {plot_chart_id_with_quote},
    {inputs_structure_cmd}
"""
    plot_data_cmd_inputs = f'Spartaqube().plot({plot_input_text})'
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 7
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True
    dict_var['plot_chart_id'] = plot_chart_id
    plot_db_chart_obj = has_access_dict['plot_db_chart_obj']
    dict_var['plot_name'] = plot_db_chart_obj.name
    dict_var['plot_data_cmd'] = plot_data_cmd
    dict_var['plot_data_cmd_inputs'] = plot_data_cmd_inputs
    return render(request, 'dist/project/plot-db/plotGUISaved.html', dict_var)


@csrf_exempt
@sparta_3b21db79ac
def sparta_555994ac46(request, json_vars_html):
    """
    Plot API (iframe)
    """
    dict_var = qube_52d8b82b2d.sparta_5c1489406e(request)
    dict_var['menuBar'] = 7
    user_infos = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dict_var.update(user_infos)
    dict_var['bCodeMirror'] = True
    dict_var.update(json.loads(json_vars_html))
    dict_var['serialized_data'] = request.POST.get('data')
    return render(request, 'dist/project/plot-db/plotAPI.html', dict_var)


@csrf_exempt
@sparta_3b21db79ac
def sparta_4ce214ca34(request):
    """
    Luckysheet (iframe)
    """
    dict_var = {}
    return render(request,
        'dist/project/luckysheetIframe/luckysheet-frame.html', dict_var)

#END OF QUBE
