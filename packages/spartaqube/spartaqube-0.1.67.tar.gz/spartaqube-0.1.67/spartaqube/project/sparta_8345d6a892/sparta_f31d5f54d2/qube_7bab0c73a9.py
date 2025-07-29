import os
import json
import base64
import subprocess
import pandas as pd
from datetime import datetime, timedelta
from dateutil import parser
import pytz
UTC = pytz.utc
from django.db.models import Q
from django.conf import settings as conf_settings
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturalday
from django.utils.text import Truncator
from django.db.models import CharField, TextField
from django.db.models.functions import Lower
CharField.register_lookup(Lower)
TextField.register_lookup(Lower)
from project.models import User, UserProfile, PlotDBChart, PlotDBChartShared, DashboardShared, Notebook, NotebookShared, DataFrameShared
from project.sparta_8345d6a892.sparta_87f32c6e97 import qube_93b4ab09a2 as qube_93b4ab09a2
from project.sparta_8345d6a892.sparta_370971529b import qube_da282a9e29 as qube_da282a9e29


def sparta_bcefba0d6f(user_obj) ->list:
    """
    
    """
    user_group_set = qube_93b4ab09a2.sparta_b0ee4cd292(user_obj)
    if len(user_group_set) > 0:
        user_groups = [this_obj.user_group for this_obj in user_group_set]
    else:
        user_groups = []
    return user_groups


def sparta_e29750b524(json_data, user_obj):
    """

    """
    keyword = json_data['keyword'].lower()
    trunc_number = 120
    user_groups = sparta_bcefba0d6f(user_obj)
    if len(user_groups) > 0:
        plot_db_chart_shared_set = PlotDBChartShared.objects.filter(Q(
            is_delete=0, user_group__in=user_groups,
            plot_db_chart__is_delete=0,
            plot_db_chart__name__lower__icontains=keyword) | Q(is_delete=0,
            user=user_obj, plot_db_chart__is_delete=0,
            plot_db_chart__name__lower__icontains=keyword))
    else:
        plot_db_chart_shared_set = PlotDBChartShared.objects.filter(is_delete
            =0, user=user_obj, plot_db_chart__is_delete=0,
            plot_db_chart__name__lower__icontains=keyword)
    cnt_widget = plot_db_chart_shared_set.count()
    plot_library_list = []
    for plot_db_shared_obj in plot_db_chart_shared_set[:5]:
        plot_db_chart_obj = plot_db_shared_obj.plot_db_chart
        plot_library_list.append({'plot_chart_id': plot_db_chart_obj.plot_chart_id, 'type_chart': plot_db_chart_obj.type_chart,
            'name': plot_db_chart_obj.name, 'name_trunc': Truncator(
            plot_db_chart_obj.name).chars(trunc_number), 'description':
            plot_db_chart_obj.description, 'description_trunc': Truncator(
            plot_db_chart_obj.description).chars(trunc_number)})
    plot_db_id_list = sorted(set([elem['plot_chart_id'] for elem in
        plot_library_list]))
    dashboard_list = []
    dashboard_ids_list = []
    cnt_dashboard = 0
    if len(user_groups) > 0:
        dashboard_shared_set = DashboardShared.objects.filter(Q(is_delete=0,
            user_group__in=user_groups, dashboard__is_delete=0) | Q(
            is_delete=0, user=user_obj, dashboard__is_delete=0,
            dashboard__name__lower__icontains=keyword))
    else:
        dashboard_shared_set = DashboardShared.objects.filter(is_delete=0,
            user=user_obj, dashboard__is_delete=0,
            dashboard__name__lower__icontains=keyword)
    cnt_dashboard = dashboard_shared_set.count()
    for dashboard_shared_obj in dashboard_shared_set[:5]:
        b_add_dashboard = False
        dashboard_obj = dashboard_shared_obj.dashboard
        if keyword in dashboard_obj.name.lower():
            b_add_dashboard = True
        else:
            plot_db_dependencies_list = dashboard_obj.plot_db_dependencies
            if plot_db_dependencies_list is not None:
                plot_db_dependencies_list = json.loads(
                    plot_db_dependencies_list)
                for elem in plot_db_dependencies_list:
                    if elem in plot_db_id_list:
                        b_add_dashboard = True
                        break
        if b_add_dashboard:
            if dashboard_obj.dashboard_id not in dashboard_ids_list:
                dashboard_ids_list.append(dashboard_obj.dashboard_id)
                dashboard_list.append({'dashboard_id': dashboard_obj.dashboard_id, 'name': dashboard_obj.name, 'name_trunc':
                    Truncator(dashboard_obj.name).chars(trunc_number),
                    'description': dashboard_obj.description,
                    'description_trunc': Truncator(dashboard_obj.description).chars(trunc_number)})
    notebook_list = []
    notebook_ids_list = []
    cnt_notebook = 0
    if len(user_groups) > 0:
        notebook_shared_set = NotebookShared.objects.filter(Q(is_delete=0,
            user_group__in=user_groups, notebook__is_delete=0) | Q(
            is_delete=0, user=user_obj, notebook__is_delete=0,
            notebook__name__lower__icontains=keyword))
    else:
        notebook_shared_set = NotebookShared.objects.filter(is_delete=0,
            user=user_obj, notebook__is_delete=0,
            notebook__name__lower__icontains=keyword)
    cnt_notebook = notebook_shared_set.count()
    for notebook_shared_obj in notebook_shared_set:
        if len(notebook_list) >= 5:
            break
        b_add_notebook = False
        notebook_obj = notebook_shared_obj.notebook
        if keyword in notebook_obj.name.lower():
            b_add_notebook = True
        if b_add_notebook:
            if notebook_obj.notebook_id not in notebook_ids_list:
                notebook_ids_list.append(notebook_obj.notebook_id)
                notebook_list.append({'notebook_id': notebook_obj.notebook_id, 'name': notebook_obj.name, 'name_trunc':
                    Truncator(notebook_obj.name).chars(trunc_number),
                    'description': notebook_obj.description,
                    'description_trunc': Truncator(notebook_obj.description
                    ).chars(trunc_number)})
    dataframe_list = []
    dataframe_ids_list = []
    cnt_dataframe = 0
    if len(user_groups) > 0:
        dataframe_shared_set = DataFrameShared.objects.filter(Q(is_delete=0,
            user_group__in=user_groups, dataframe_model__is_delete=0) | Q(
            is_delete=0, user=user_obj, dataframe_model__is_delete=0,
            dataframe_model__table_name__lower__icontains=keyword))
    else:
        dataframe_shared_set = DataFrameShared.objects.filter(is_delete=0,
            user=user_obj, dataframe_model__is_delete=0,
            dataframe_model__table_name__lower__icontains=keyword)
    cnt_dataframe = dataframe_shared_set.count()
    for dataframe_shared_obj in dataframe_shared_set:
        if len(dataframe_list) >= 5:
            break
        b_add_dataframe = False
        dataframe_model_obj = dataframe_shared_obj.dataframe_model
        if keyword in dataframe_model_obj.table_name.lower():
            b_add_dataframe = True
        if b_add_dataframe:
            if dataframe_model_obj.slug not in dataframe_ids_list:
                dataframe_ids_list.append(dataframe_model_obj.slug)
                dataframe_list.append({'dataframe_id': dataframe_model_obj.slug, 'name': dataframe_model_obj.table_name,
                    'name_trunc': Truncator(dataframe_model_obj.table_name).chars(trunc_number), 'description':
                    dataframe_model_obj.description, 'description_trunc':
                    Truncator(dataframe_model_obj.description).chars(
                    trunc_number)})
    cnt_total = 0
    counter_dict = {'widgets': cnt_widget, 'dashboards': cnt_dashboard,
        'notebooks': cnt_notebook, 'dataframes': cnt_dataframe}
    for _, val in counter_dict.items():
        cnt_total += val
    return {'res': 1, 'widgets': plot_library_list, 'dashboards':
        dashboard_list, 'notebooks': notebook_list, 'dataframes':
        dataframe_list, 'cntTotal': cnt_total, 'counter_dict': counter_dict}

#END OF QUBE
