import traceback
import subprocess
import sys
import json
import math
import pickle
import base64
import pandas as pd
from datetime import datetime, timedelta
import pytz
UTC = pytz.utc
from django.db.models import Q
from django.utils.text import slugify
from project.models_spartaqube import DataFrameHistory, DataFrameShared, DataFrameModel, DataFramePermission
from project.models import ShareRights
from project.sparta_8688631f3d.sparta_355a680bf7 import qube_1d2a59f054 as qube_1d2a59f054
from project.sparta_8688631f3d.sparta_5d2f5154f8 import qube_c71ace27e3 as qube_c71ace27e3
from project.logger_config import logger
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_8f0cad92aa import process_dataframe_components


def sparta_09abdd9532(user_obj) ->list:
    """
    
    """
    user_group_set = qube_1d2a59f054.sparta_1c22139619(user_obj)
    if len(user_group_set) > 0:
        user_groups = [this_obj.user_group for this_obj in user_group_set]
    else:
        user_groups = []
    return user_groups


def sparta_126dfbb816(dispo) ->str:
    return pickle.loads(base64.b64decode(dispo.encode('utf-8')))


def sparta_8b8da00f6d(json_data, user_obj) ->dict:
    """
    Insert dataframe
    """
    encoded_blob = json_data['df']
    blob_df = base64.b64decode(encoded_blob.encode('utf-8'))
    table_name = json_data['table_name']
    dispo = json_data.get('dispo', None)
    if dispo is not None:
        dispo = sparta_126dfbb816(dispo)
    mode = json_data.get('mode', 'append')
    date_now = datetime.now().astimezone(UTC)
    dataframe_user_shared_obj = None
    user_groups = sparta_09abdd9532(user_obj)
    if len(user_groups) > 0:
        dataframe_user_shared_set = DataFrameShared.objects.filter(Q(
            is_delete=0, user_group__in=user_groups,
            dataframe_model__table_name=table_name) | Q(is_delete=0, user=
            user_obj, dataframe_model__table_name=table_name))
    else:
        dataframe_user_shared_set = DataFrameShared.objects.filter(is_delete
            =0, user=user_obj, dataframe_model__table_name=table_name)
    dataframe_user_shared_count = dataframe_user_shared_set.count()
    if dataframe_user_shared_count == 0:
        base_slug = slugify(table_name)
        slug = base_slug
        counter = 1
        while DataFrameModel.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        dataframe_model_obj = DataFrameModel.objects.create(table_name=
            table_name, slug=slug, date_created=date_now, last_update=date_now)
        share_rights_obj = ShareRights.objects.create(is_admin=True,
            has_write_rights=True, has_reshare_rights=True, last_update=
            date_now)
        dataframe_user_shared_obj = DataFrameShared.objects.create(
            dataframe_model=dataframe_model_obj, user=user_obj,
            date_created=date_now, share_rights=share_rights_obj, is_owner=True
            )
    elif dataframe_user_shared_count == 1:
        dataframe_user_shared_obj = dataframe_user_shared_set[0]
        slug = dataframe_user_shared_obj.dataframe_model.slug
    else:
        if slug is None:
            return {'res': -1, 'errorMsg': 'Missing slug'}
        if len(user_groups) > 0:
            dataframe_user_shared_set = DataFrameShared.objects.filter(Q(
                is_delete=0, user_group__in=user_groups,
                dataframe_model__slug=slug) | Q(is_delete=0, user=user_obj,
                dataframe_model__slug=slug))
        else:
            dataframe_user_shared_set = DataFrameShared.objects.filter(
                is_delete=0, user=user_obj, dataframe_model__slug=slug)
        if dataframe_user_shared_set.count() == 1:
            dataframe_user_shared_obj = dataframe_user_shared_set[0]
        else:
            return {'res': -1, 'errorMsg': 'Invalid slug'}
    if dataframe_user_shared_obj is not None:
        if dispo is None:
            dispo = date_now.strftime('%Y-%m-%d')
        if isinstance(dispo, list):
            df = pickle.loads(blob_df)
            if len(dispo) == len(df):
                if mode == 'replace':
                    share_rights_obj = dataframe_user_shared_obj.share_rights
                    if share_rights_obj.is_admin:
                        DataFrameHistory.objects.filter(dataframe_model=
                            dataframe_user_shared_obj.dataframe_model,
                            dispo__in=dispo).delete()
                new_objects = []
                for idx, this_dispo in enumerate(dispo):
                    this_blob_df = pickle.dumps(df.iloc[idx].to_frame().T)
                    new_objects.append(DataFrameHistory(dataframe_model=
                        dataframe_user_shared_obj.dataframe_model, df_blob=
                        this_blob_df, dispo=this_dispo, date_created=
                        date_now, last_update=date_now))
                DataFrameHistory.objects.bulk_create(new_objects,
                    batch_size=500)
            else:
                return {'res': -1, 'errorMsg':
                    'If you want to use a list of dispo, it must have the same length at the dataframe'
                    }
        else:
            if mode == 'replace':
                share_rights_obj = dataframe_user_shared_obj.share_rights
                if share_rights_obj.is_admin:
                    dataframe_history_set = DataFrameHistory.objects.filter(
                        dataframe_model=dataframe_user_shared_obj.dataframe_model, dispo=dispo)
                    for dataframe_history_obj in dataframe_history_set:
                        dataframe_history_obj.delete()
            DataFrameHistory.objects.create(dataframe_model=
                dataframe_user_shared_obj.dataframe_model, df_blob=blob_df,
                dispo=dispo, date_created=date_now, last_update=date_now)
        return {'res': 1, 'slug': slug}
    return {'res': -1}


def sparta_43e5361c90(json_data, user_obj) ->dict:
    """
    Pud dataframe from the GUI (when user wants to save from the GUI, we must first create the dataframe here)
    """
    print('DEBUG put_df_from_gui')
    data_dict = json.loads(json_data['data'])
    columns_raw = data_dict['columns']
    if isinstance(columns_raw[0], list) or isinstance(columns_raw[0], tuple):
        columns = [tuple(col) for col in columns_raw]
        data_df = pd.DataFrame(data=data_dict['data'], index=pd.MultiIndex.from_tuples(columns), columns=data_dict['index']).T
    else:
        data_df = pd.DataFrame(data=data_dict['data'], index=columns_raw,
            columns=data_dict['index']).T
    df = data_df
    blob = pickle.dumps(df)
    encoded_blob = base64.b64encode(blob).decode('utf-8')
    json_data['df'] = encoded_blob
    res_put_df_dict = sparta_8b8da00f6d(json_data, user_obj)
    return res_put_df_dict


def sparta_521aed69f1(json_data, user_obj) ->dict:
    """
    Drop dataframe
    """
    table_name = json_data['table_name']
    slug = json_data.get('slug', None)
    user_groups = sparta_09abdd9532(user_obj)
    if len(user_groups) > 0:
        dataframe_user_shared_set = DataFrameShared.objects.filter(Q(
            is_delete=0, user_group__in=user_groups,
            dataframe_model__table_name=table_name) | Q(is_delete=0, user=
            user_obj, dataframe_model__table_name=table_name))
    else:
        dataframe_user_shared_set = DataFrameShared.objects.filter(is_delete
            =0, user=user_obj, dataframe_model__table_name=table_name)
    if dataframe_user_shared_set.count() == 0:
        return {'res': -1, 'errorMsg':
            'You do not have the rights to drop this dataframe'}
    elif dataframe_user_shared_set.count() == 1:
        dataframe_user_shared_obj = dataframe_user_shared_set[0]
        share_rights_obj = dataframe_user_shared_obj.share_rights
        if share_rights_obj.is_admin:
            dataframe_user_shared_obj.delete()
    elif slug is None:
        return {'res': -1, 'errorMsg': 'Missing slug'}
    else:
        if len(user_groups) > 0:
            dataframe_user_shared_set = DataFrameShared.objects.filter(Q(
                is_delete=0, user_group__in=user_groups,
                dataframe_model__slug=slug) | Q(is_delete=0, user=user_obj,
                dataframe_model__slug=slug))
        else:
            dataframe_user_shared_set = DataFrameShared.objects.filter(
                is_delete=0, user=user_obj, dataframe_model__slug=slug)
        if dataframe_user_shared_set.count() == 1:
            dataframe_user_shared_obj = dataframe_user_shared_set[0]
            share_rights_obj = dataframe_user_shared_obj.share_rights
            if share_rights_obj.is_admin:
                dataframe_user_shared_obj.delete()
    return {'res': 1}


def sparta_89abaa23b9(json_data, user_obj) ->dict:
    """
    Drop specific dispo date
    """
    dispo = json_data['dispo']
    if dispo is not None:
        dispo = sparta_126dfbb816(dispo)
    table_name = json_data['table_name']
    slug = json_data.get('slug', None)
    user_groups = sparta_09abdd9532(user_obj)
    if len(user_groups) > 0:
        dataframe_user_shared_set = DataFrameShared.objects.filter(Q(
            is_delete=0, user_group__in=user_groups,
            dataframe_model__table_name=table_name) | Q(is_delete=0, user=
            user_obj, dataframe_model__table_name=table_name))
    else:
        dataframe_user_shared_set = DataFrameShared.objects.filter(is_delete
            =0, user=user_obj, dataframe_model__table_name=table_name)
    if dataframe_user_shared_set.count() == 0:
        return {'res': -1, 'errorMsg':
            'You do not have the rights to drop this dataframe'}
    elif dataframe_user_shared_set.count() == 1:
        dataframe_user_shared_obj = dataframe_user_shared_set[0]
        share_rights_obj = dataframe_user_shared_obj.share_rights
        if share_rights_obj.is_admin:
            dataframe_history_set = DataFrameHistory.objects.filter(
                dataframe_model=dataframe_user_shared_obj.dataframe_model,
                dispo=dispo)
            for dataframe_history_obj in dataframe_history_set:
                dataframe_history_obj.delete()
    elif slug is None:
        return {'res': -1, 'errorMsg': 'Missing slug'}
    else:
        if len(user_groups) > 0:
            dataframe_user_shared_set = DataFrameShared.objects.filter(Q(
                is_delete=0, user_group__in=user_groups,
                dataframe_model__slug=slug) | Q(is_delete=0, user=user_obj,
                dataframe_model__slug=slug))
        else:
            dataframe_user_shared_set = DataFrameShared.objects.filter(
                is_delete=0, user=user_obj, dataframe_model__slug=slug)
        if dataframe_user_shared_set.count() == 1:
            dataframe_user_shared_obj = dataframe_user_shared_set[0]
            share_rights_obj = dataframe_user_shared_obj.share_rights
            if share_rights_obj.is_admin:
                dataframe_history_set = DataFrameHistory.objects.filter(
                    dataframe_model=dataframe_user_shared_obj.dataframe_model, dispo=dispo)
                for dataframe_history_obj in dataframe_history_set:
                    dataframe_history_obj.delete()
    return {'res': 1}


def sparta_e5b146daee(json_data, user_obj) ->dict:
    """
    Drop dataframe by id
    """
    dataframe_model_set = DataFrameModel.objects.filter(id=json_data['id'])
    if dataframe_model_set.count() > 0:
        dataframe_model_obj = dataframe_model_set[0]
        user_groups = sparta_09abdd9532(user_obj)
        if len(user_groups) > 0:
            dataframe_user_shared_set = DataFrameShared.objects.filter(Q(
                is_delete=0, user_group__in=user_groups, dataframe_model=
                dataframe_model_obj) | Q(is_delete=0, user=user_obj,
                dataframe_model=dataframe_model_obj))
        else:
            dataframe_user_shared_set = DataFrameShared.objects.filter(
                is_delete=0, user=user_obj, dataframe_model=dataframe_model_obj
                )
        if dataframe_user_shared_set.count() == 1:
            dataframe_user_shared_obj = dataframe_user_shared_set[0]
            share_rights = dataframe_user_shared_obj.share_rights
            if share_rights.is_admin:
                dataframe_model_obj.delete()
                return {'res': 1}
            return {'res': -1, 'errorMsg':
                "You don't have sufficient rights to drop this object"}
        return {'res': -1, 'errorMsg':
            "You don't have the rights to drop this object"}
    return {'res': -1, 'errorMsg': 'Object not found...'}


def sparta_b9341eb929(json_data, user_obj) ->dict:
    """
    Get available dataframes
    """
    user_groups = sparta_09abdd9532(user_obj)
    if len(user_groups) > 0:
        dataframe_user_shared_set = DataFrameShared.objects.filter(Q(
            is_delete=0, user_group__in=user_groups) | Q(is_delete=0, user=
            user_obj))
    else:
        dataframe_user_shared_set = DataFrameShared.objects.filter(is_delete
            =0, user=user_obj)
    res = []
    for dataframe_user_shared_obj in dataframe_user_shared_set:
        share_rights = dataframe_user_shared_obj.share_rights
        dataframe_model = dataframe_user_shared_obj.dataframe_model
        res.append({'name': dataframe_model.table_name, 'slug':
            dataframe_model.slug, 'description': dataframe_model.description, 'is_expose_widget': dataframe_model.is_expose_widget, 'is_public_widget': dataframe_model.is_public_widget, 'has_widget_password': dataframe_model.has_widget_password, 'date_created': str(dataframe_model.date_created.strftime('%Y-%m-%d')), 'last_update': str(
            dataframe_model.last_update.strftime('%Y-%m-%d %H:%M:%S')),
            'is_admin': share_rights.is_admin, 'has_write_rights':
            share_rights.has_write_rights, 'id': dataframe_model.id})
    if len(res) > 0:
        res = sorted(res, key=lambda x: x['id'], reverse=True)
    return {'res': 1, 'available_df': res}


def sparta_db94f6cb87(json_data, user_obj) ->dict:
    """
    Get dataframe
    """
    table_name = json_data.get('table_name', None)
    slug = json_data.get('slug', None)
    dispo = json_data.get('dispo', None)
    if dispo is not None:
        dispo = sparta_126dfbb816(dispo)
    user_groups = sparta_09abdd9532(user_obj)
    if table_name is not None:
        if len(user_groups) > 0:
            dataframe_user_shared_set = DataFrameShared.objects.filter(Q(
                is_delete=0, user_group__in=user_groups,
                dataframe_model__table_name=table_name) | Q(is_delete=0,
                user=user_obj, dataframe_model__table_name=table_name))
        else:
            dataframe_user_shared_set = DataFrameShared.objects.filter(
                is_delete=0, user=user_obj, dataframe_model__table_name=
                table_name)
        if dataframe_user_shared_set.count() == 0:
            return {'res': -1, 'errorMsg':
                'You do not have the rights to get this dataframe'}
    dataframe_user_shared_obj = None
    if table_name is not None:
        if dataframe_user_shared_set.count() == 1:
            dataframe_user_shared_obj = dataframe_user_shared_set[0]
    if dataframe_user_shared_obj is None:
        if slug is None:
            return {'res': -1, 'errorMsg': 'Missing slug'}
        else:
            if len(user_groups) > 0:
                dataframe_user_shared_set = DataFrameShared.objects.filter(
                    Q(is_delete=0, user_group__in=user_groups,
                    dataframe_model__slug=slug) | Q(is_delete=0, user=
                    user_obj, dataframe_model__slug=slug))
            else:
                dataframe_user_shared_set = DataFrameShared.objects.filter(
                    is_delete=0, user=user_obj, dataframe_model__slug=slug)
            if dataframe_user_shared_set.count() == 1:
                dataframe_user_shared_obj = dataframe_user_shared_set[0]
    if dataframe_user_shared_obj is not None:
        if dataframe_user_shared_obj.dataframe_model.is_dataframe_connector:
            connector_config = json.loads(dataframe_user_shared_obj.dataframe_model.connector_config)
            connector_config['previewTopMod'] = 1
            from project.sparta_8688631f3d.sparta_5d2f5154f8 import qube_82ff246dc8 as qube_82ff246dc8
            data_preview_dict = qube_82ff246dc8.sparta_5a118bb77c(
                connector_config, user_obj)
            data_preview_dict = json.loads(data_preview_dict['data'])
            data_preview_df = pd.DataFrame(data_preview_dict['data'], index
                =data_preview_dict['index'], columns=data_preview_dict[
                'columns'])
            return {'res': 1, 'is_dataframe_connector': True,
                'data_preview_df': data_preview_df, 'dataframe_model_name':
                dataframe_user_shared_obj.dataframe_model.table_name,
                'is_encoded_blob': False}
        else:
            if dispo is None:
                dataframe_history_set = DataFrameHistory.objects.filter(
                    dataframe_model=dataframe_user_shared_obj.dataframe_model)
            elif isinstance(dispo, list):
                dataframe_history_set = DataFrameHistory.objects.filter(
                    dataframe_model=dataframe_user_shared_obj.dataframe_model, dispo__in=dispo)
            else:
                dataframe_history_set = DataFrameHistory.objects.filter(
                    dataframe_model=dataframe_user_shared_obj.dataframe_model, dispo=dispo)
            res = []
            for dataframe_history_obj in dataframe_history_set:
                res.append({'df_blob': dataframe_history_obj.df_blob,
                    'dispo': dataframe_history_obj.dispo})
            blob = pickle.dumps(res)
            encoded_blob = base64.b64encode(blob).decode('utf-8')
            return {'res': 1, 'encoded_blob': encoded_blob,
                'dataframe_model_name': dataframe_user_shared_obj.dataframe_model.table_name, 'is_dataframe_connector': False,
                'is_encoded_blob': False}
    return {'res': 1, 'df': []}


def sparta_094806e994(json_data, user_obj):
    """
    
    """
    slug = json_data['slug']
    password = json_data['password']
    dispo = json_data.get('dispo', None)
    if dispo is not None:
        dispo = sparta_126dfbb816(dispo)
    widget_access_dict = sparta_b64f60322d(slug, user_obj, password)
    if widget_access_dict['res'] == 1:
        dataframe_model_obj = widget_access_dict['dataframe_model_obj']
        if dataframe_model_obj.dataframe_model.is_dataframe_connector:
            connector_config = json.loads(dataframe_model_obj.connector_config)
            connector_config['previewTopMod'] = 1
            from project.sparta_8688631f3d.sparta_5d2f5154f8 import qube_82ff246dc8 as qube_82ff246dc8
            data_preview_dict = qube_82ff246dc8.sparta_5a118bb77c(
                connector_config, user_obj)
            data_preview_dict = json.loads(data_preview_dict['data'])
            data_preview_df = pd.DataFrame(data_preview_dict['data'], index
                =data_preview_dict['index'], columns=data_preview_dict[
                'columns'])
            return {'res': 1, 'is_dataframe_connector': True,
                'data_preview_df': data_preview_df, 'dataframe_model_name':
                dataframe_model_obj.table_name}
        else:
            if dispo is None:
                dataframe_history_set = DataFrameHistory.objects.filter(
                    dataframe_model=dataframe_model_obj)
            elif isinstance(dispo, list):
                dataframe_history_set = DataFrameHistory.objects.filter(
                    dataframe_model=dataframe_model_obj, dispo__in=dispo)
            else:
                dataframe_history_set = DataFrameHistory.objects.filter(
                    dataframe_model=dataframe_model_obj, dispo=dispo)
            res = []
            for dataframe_history_obj in dataframe_history_set:
                res.append({'df_blob': dataframe_history_obj.df_blob,
                    'dispo': dataframe_history_obj.dispo})
            blob = pickle.dumps(res)
            encoded_blob = base64.b64encode(blob).decode('utf-8')
            widget_access_dict['encoded_blob'] = encoded_blob
            widget_access_dict['dataframe_model_name'
                ] = dataframe_model_obj.table_name,
    return widget_access_dict


def sparta_c2b7140512(slug, user_obj, dispo: None) ->list:
    """
    
    """
    if dispo is not None:
        dispo = sparta_126dfbb816(dispo)
    user_groups = sparta_09abdd9532(user_obj)
    if len(user_groups) > 0:
        dataframe_user_shared_set = DataFrameShared.objects.filter(Q(
            is_delete=0, user_group__in=user_groups, dataframe_model__slug=
            slug) | Q(is_delete=0, user=user_obj, dataframe_model__slug=slug))
    else:
        dataframe_user_shared_set = DataFrameShared.objects.filter(is_delete
            =0, user=user_obj, dataframe_model__slug=slug)
    if dataframe_user_shared_set.count() == 1:
        dataframe_user_shared_obj = dataframe_user_shared_set[0]
        if dispo is None:
            dataframe_history_set = DataFrameHistory.objects.filter(
                dataframe_model=dataframe_user_shared_obj.dataframe_model)
        elif isinstance(dispo, list):
            dataframe_history_set = DataFrameHistory.objects.filter(
                dataframe_model=dataframe_user_shared_obj.dataframe_model,
                dispo__in=dispo)
        else:
            dataframe_history_set = DataFrameHistory.objects.filter(
                dataframe_model=dataframe_user_shared_obj.dataframe_model,
                dispo=dispo)
        return [pickle.loads(elem_dict.df_blob).assign(dispo=elem_dict.dispo) for elem_dict in dataframe_history_set]
    return []


def sparta_732735c899(dataframe_model, dispo: None) ->list:
    """
    
    """
    if dispo is not None:
        dispo = sparta_126dfbb816(dispo)
    if dispo is None:
        dataframe_history_set = DataFrameHistory.objects.filter(dataframe_model
            =dataframe_model)
    elif isinstance(dispo, list):
        dataframe_history_set = DataFrameHistory.objects.filter(dataframe_model
            =dataframe_model, dispo__in=dispo)
    else:
        dataframe_history_set = DataFrameHistory.objects.filter(dataframe_model
            =dataframe_model, dispo=dispo)
    return [pickle.loads(elem_dict.df_blob).assign(dispo=elem_dict.dispo) for
        elem_dict in dataframe_history_set]


def sparta_d996dcb444(json_data, user_obj) ->dict:
    """
    Update dataframe
    """
    name = json_data.get('name', '')
    slug = json_data.get('slug', None)
    description = json_data.get('description', '')
    user_groups = sparta_09abdd9532(user_obj)
    if len(user_groups) > 0:
        dataframe_user_shared_set = DataFrameShared.objects.filter(Q(
            is_delete=0, user_group__in=user_groups, dataframe_model__slug=
            slug) | Q(is_delete=0, user=user_obj, dataframe_model__slug=slug))
    else:
        dataframe_user_shared_set = DataFrameShared.objects.filter(is_delete
            =0, user=user_obj, dataframe_model__slug=slug)
    if dataframe_user_shared_set.count() == 0:
        return {'res': -1, 'errorMsg':
            'You do not have the rights to edit this dataframe'}
    date_now = datetime.now().astimezone(UTC)
    dataframe_user_shared_obj = dataframe_user_shared_set[0]
    dataframe_model_obj = dataframe_user_shared_obj.dataframe_model
    dataframe_model_obj.table_name = name
    dataframe_model_obj.description = description
    widget_password_e = None
    has_widget_password = json_data['has_widget_password']
    if has_widget_password:
        widget_password = json_data['widget_password']
        widget_password_e = qube_c71ace27e3.sparta_b4548ea0cb(
            widget_password)
    dataframe_model_obj.is_expose_widget = json_data['is_expose_widget']
    dataframe_model_obj.is_public_widget = json_data['is_public_widget']
    dataframe_model_obj.has_widget_password = has_widget_password
    dataframe_model_obj.widget_password_e = widget_password_e
    dataframe_model_obj.last_update = date_now
    dataframe_model_obj.save()
    return {'res': 1}


def sparta_78e00a5a30(json_data, user_obj) ->dict:
    """
    Returns dataframe config
    """
    slug = json_data.get('slug', None)
    user_groups = sparta_09abdd9532(user_obj)
    if len(user_groups) > 0:
        dataframe_user_shared_set = DataFrameShared.objects.filter(Q(
            is_delete=0, user_group__in=user_groups, dataframe_model__slug=
            slug) | Q(is_delete=0, user=user_obj, dataframe_model__slug=slug))
    else:
        dataframe_user_shared_set = DataFrameShared.objects.filter(is_delete
            =0, user=user_obj, dataframe_model__slug=slug)
    if dataframe_user_shared_set.count() == 1:
        dataframe_user_shared_obj = dataframe_user_shared_set[0]
        dataframe_model_obj = dataframe_user_shared_obj.dataframe_model
        return dataframe_model_obj
    return None


def sparta_e629a319d4(json_data, user_obj) ->dict:
    """
    Returns dataframe config
    """
    dataframe_model_obj = sparta_78e00a5a30(json_data, user_obj)
    if dataframe_model_obj is not None:
        return {'res': 1, 'config': dataframe_model_obj.dataframe_config}
    return {'res': -1, 'errorMsg':
        'You do not have access to this dataframe...'}


def sparta_b6ad0dd8e2(json_data, user_obj) ->list:
    """
    Check if has dataframe slug
    """
    try:
        has_access_dict = sparta_558bd9a739(json_data['slug'], user_obj
            )
        b_has_access = has_access_dict['has_access']
        return {'res': 1, 'has_access': b_has_access}
    except:
        pass
    return {'res': -1}


def sparta_f889329a19(json_data, user_obj) ->dict:
    """
    
    """
    slug = json_data['slug']
    user_groups = sparta_09abdd9532(user_obj)
    if len(user_groups) > 0:
        dataframe_user_shared_set = DataFrameShared.objects.filter(Q(
            is_delete=0, user_group__in=user_groups, dataframe_model__slug=
            slug) | Q(is_delete=0, user=user_obj, dataframe_model__slug=slug))
    else:
        dataframe_user_shared_set = DataFrameShared.objects.filter(is_delete
            =0, user=user_obj, dataframe_model__slug=slug)
    if dataframe_user_shared_set.count() == 0:
        return {'res': -1, 'errorMsg':
            'You do not have the rights to edit this dataframe'}
    date_now = datetime.now().astimezone(UTC)
    dataframe_user_shared_obj = dataframe_user_shared_set[0]
    dataframe_model_obj = dataframe_user_shared_obj.dataframe_model
    dataframe_model_obj.dataframe_config = json_data['config']
    dataframe_model_obj.last_update = date_now
    dataframe_model_obj.save()
    plot_db_config = json_data.get('plotDBConfig', None)
    print('save_config_dataframe json_data')
    print(json_data)
    print(json_data.keys())
    if plot_db_config is not None:
        from project.sparta_8688631f3d.sparta_5d2f5154f8 import qube_82ff246dc8 as qube_82ff246dc8
        json_data['plotName'] = dataframe_model_obj.table_name
        json_data['is_created_from_dataframe'] = True
        if str(json_data.get('plot_chart_id', '-1')) == '-1':
            b_return_model = True
            res_dict = qube_82ff246dc8.sparta_2b42cd2e90(json_data, user_obj,
                b_return_model)
            print('res_dict create save plot')
            print(res_dict)
            if res_dict['res'] == 1:
                plot_db_chart_obj = res_dict['plot_db_chart_obj']
                dataframe_model_obj.plot_db_chart = plot_db_chart_obj
                dataframe_model_obj.save()
                return {'res': 1, 'plot_chart_id': plot_db_chart_obj.plot_chart_id}
        else:
            res_dict = qube_82ff246dc8.sparta_7882d22565(json_data, user_obj)
            print('res_dict update plot')
            print(res_dict)
    return {'res': 1}


def sparta_282db01ee6(json_data, user_obj) ->dict:
    """
    Create dataframe from connector
    """
    print('json_data create_dataframe_from_connector')
    print(json_data)
    json_data['previewTopMod'] = 1
    table_name = json_data['connector_name']
    date_now = datetime.now().astimezone(UTC)
    base_slug = slugify(table_name)
    slug = base_slug
    counter = 1
    while DataFrameModel.objects.filter(slug=slug).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1
    slug = slug.lower()
    dataframe_model_obj = DataFrameModel.objects.create(table_name=
        table_name, slug=slug, date_created=date_now,
        is_dataframe_connector=True, connector_config=json.dumps(json_data),
        last_update=date_now)
    share_rights_obj = ShareRights.objects.create(is_admin=True,
        has_write_rights=True, has_reshare_rights=True, last_update=date_now)
    dataframe_user_shared_obj = DataFrameShared.objects.create(dataframe_model
        =dataframe_model_obj, user=user_obj, date_created=date_now,
        share_rights=share_rights_obj, is_owner=True)
    return {'res': 1, 'slug': slug}


def sparta_50840ae5a4(json_data, user_obj) ->dict:
    """
    Preview dataframe from gui (copy/paste)
    """
    df = pd.DataFrame(json_data['clipboardData'])
    delimiters = json_data['delimiters']
    if delimiters is not None:
        if len(delimiters) > 0:
            cols = df.columns
            df = df[cols[0]].str.split(delimiters, expand=True)
    if json_data['bFirstRowHeader']:
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)
    if json_data['bFirstColIndex']:
        df = df.set_index(df.columns[0])
    table = df.to_html()
    return {'res': 1, 'table': table}


def sparta_bf7211d2b3(json_data, user_obj) ->dict:
    """
    Create dataframe from gui (copy/paste)
    """
    mode = 'replace'
    table_name = json_data['name']
    dispo = json_data.get('dispo', None)
    date_now = datetime.now().astimezone(UTC)
    df = pd.DataFrame(json_data['clipboardData'])
    delimiters = json_data['delimiters']
    if delimiters is not None:
        if len(delimiters) > 0:
            cols = df.columns
            df = df[cols[0]].str.split(delimiters, expand=True)
    if json_data['bFirstRowHeader']:
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)
    if json_data['bFirstColIndex']:
        df = df.set_index(df.columns[0])
    base_slug = slugify(table_name)
    slug = base_slug
    counter = 1
    while DataFrameModel.objects.filter(slug=slug).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1
    slug = slug.lower()
    dataframe_model_obj = DataFrameModel.objects.create(table_name=
        table_name, slug=slug, date_created=date_now, last_update=date_now)
    share_rights_obj = ShareRights.objects.create(is_admin=True,
        has_write_rights=True, has_reshare_rights=True, last_update=date_now)
    dataframe_user_shared_obj = DataFrameShared.objects.create(dataframe_model
        =dataframe_model_obj, user=user_obj, date_created=date_now,
        share_rights=share_rights_obj, is_owner=True)
    if dataframe_user_shared_obj is not None:
        if dispo is None:
            dispo = date_now.strftime('%Y-%m-%d')
        if isinstance(dispo, list):
            if len(dispo) == len(df):
                if mode == 'replace':
                    share_rights_obj = dataframe_user_shared_obj.share_rights
                    if share_rights_obj.is_admin:
                        DataFrameHistory.objects.filter(dataframe_model=
                            dataframe_user_shared_obj.dataframe_model,
                            dispo__in=dispo).delete()
                new_objects = []
                for idx, this_dispo in enumerate(dispo):
                    this_blob_df = pickle.dumps(df.iloc[idx].to_frame().T)
                    new_objects.append(DataFrameHistory(dataframe_model=
                        dataframe_user_shared_obj.dataframe_model, df_blob=
                        this_blob_df, dispo=this_dispo, date_created=
                        date_now, last_update=date_now))
                DataFrameHistory.objects.bulk_create(new_objects,
                    batch_size=500)
            else:
                return {'res': -1, 'errorMsg':
                    'If you want to use a list of dispo, it must have the same length at the dataframe'
                    }
        else:
            if mode == 'replace':
                share_rights_obj = dataframe_user_shared_obj.share_rights
                if share_rights_obj.is_admin:
                    dataframe_history_set = DataFrameHistory.objects.filter(
                        dataframe_model=dataframe_user_shared_obj.dataframe_model, dispo=dispo)
                    for dataframe_history_obj in dataframe_history_set:
                        dataframe_history_obj.delete()
            blob_df = pickle.dumps(df)
            DataFrameHistory.objects.create(dataframe_model=
                dataframe_user_shared_obj.dataframe_model, df_blob=blob_df,
                dispo=dispo, date_created=date_now, last_update=date_now)
        return {'res': 1, 'slug': slug}
    return {'res': 1, 'slug': slug}


def sparta_3d1b756528(json_data, user_obj) ->dict:
    """
    Load dataframe statistics (explorer tab)
    """
    dispo = json_data.get('dispo', None)
    slug = json_data['slug']
    if json_data.get('password', None) is not None:
        widget_access_dict = sparta_b64f60322d(slug, user_obj, json_data[
            'password'])
        if widget_access_dict['res'] == 1:
            dataframe_model_obj = widget_access_dict['dataframe_model_obj']
            data_df_list = sparta_732735c899(dataframe_model_obj,
                dispo)
        else:
            return {'res': -1, 'password': 'Invalid password', 'errorMsg':
                'Invalid password'}
    else:
        data_df_list = sparta_c2b7140512(slug, user_obj, dispo)
    try:
        df_all = pd.concat(data_df_list)
        df_all = process_dataframe_components(df_all)
        data_table_stats_df = df_all.describe()
        return {'res': 1, 'data': data_table_stats_df.to_json(orient='split')}
    except Exception as e:
        return {'res': -1, 'errorMsg':
            'Cannot compute the statistics for this object. Make sure all dataframes are stored with the same data/columns structure'
            , 'errorMsg2': str(e)}


def sparta_3fd6fca817(json_data, user_obj) ->dict:
    """
    Compute statistics dynamically (GUI dataframe using the passed dataframe)
    """
    data_dict = json.loads(json_data['data'])
    columns_raw = data_dict['columns']
    if isinstance(columns_raw[0], list) or isinstance(columns_raw[0], tuple):
        columns = [tuple(col) for col in columns_raw]
        data_df = pd.DataFrame(data=data_dict['data'], index=pd.MultiIndex.from_tuples(columns), columns=data_dict['index']).T
    elif len(data_dict['data']) == len(data_dict['index']):
        data_df = pd.DataFrame(data=data_dict['data'], columns=columns_raw,
            index=data_dict['index'])
    else:
        data_df = pd.DataFrame(data=data_dict['data'], index=columns_raw,
            columns=data_dict['index']).T
    try:
        data_table_stats_df = data_df.describe()
        return {'res': 1, 'data': data_table_stats_df.to_json(orient='split')}
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback Get statistics from GUI dataframe')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_49cde73e5b(data_df, json_data) ->pd.DataFrame:
    """
    
    """
    for key, val in json_data['logTransformationDict'].items():
        if val:
            data_df[key] = data_df[key].apply(lambda x: math.log(x))
    for key, val in json_data['differencingDict'].items():
        if val:
            differencing_dict = json_data.get('differencingDict', None)
            if differencing_dict is not None:
                offset = differencing_dict.get(key, 0)
                if offset != 0:
                    data_df[key] = data_df[key] - data_df[key].shift(offset)
    return data_df


def sparta_036d8592d3(json_data) ->pd.DataFrame:
    """
    Returns teh dataframe sent from the user (dataframe components vue).It handles both concatenate and dispo mode
    """
    is_filter_dispo = json_data.get('isFilterDispo', False)
    data_dict = json.loads(json_data['data'])
    columns_raw = data_dict['columns']
    if is_filter_dispo:
        if isinstance(columns_raw[0], list) or isinstance(columns_raw[0], tuple
            ):
            columns = [tuple(col) for col in columns_raw]
            data_df = pd.DataFrame(data=data_dict['data'], columns=pd.MultiIndex.from_tuples(columns), index=data_dict['index'])
        else:
            data_df = pd.DataFrame(data=data_dict['data'], index=data_dict[
                'index'], columns=columns_raw)
    elif isinstance(columns_raw[0], list) or isinstance(columns_raw[0], tuple):
        columns = [tuple(col) for col in columns_raw]
        data_df = pd.DataFrame(data=data_dict['data'], index=pd.MultiIndex.from_tuples(columns), columns=data_dict['index']).T
    else:
        data_df = pd.DataFrame(data=data_dict['data'], index=columns_raw,
            columns=data_dict['index']).T
    data_df['__sq_index__'] = data_df.index
    return data_df


def sparta_98f74ccd72(json_data, user_obj) ->dict:
    """
    Run columns statistics
    """
    from .qube_414188f292 import analyze_columns
    data_df = sparta_036d8592d3(json_data)
    selected_columns = list(data_df.columns)
    try:
        data_df = sparta_49cde73e5b(data_df, json_data)
        res_dict = sparta_0b3f11ae69(data_df, selected_columns, B_DARK_THEME=
            json_data.get('B_DARK_THEME', False))
        return {'res': 1, 'analysis': json.dumps(res_dict, allow_nan=False)}
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback > ')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_4add53a7d7(json_data, user_obj) ->dict:
    """
    Run columns statistics
    """
    from .qube_414188f292 import analyze_columns_corr
    data_df = sparta_036d8592d3(json_data)
    selected_columns = list(data_df.columns)
    selected_columns = [elem for elem in selected_columns if elem !=
        '__sq_index__']
    try:
        data_df = sparta_49cde73e5b(data_df, json_data)
        res_dict = sparta_5bb748fe57(data_df, selected_columns,
            B_DARK_THEME=json_data.get('B_DARK_THEME', False))
        return {'res': 1, 'analysis': json.dumps(res_dict, allow_nan=False)}
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_f6f94d8f34(json_data, user_obj) ->dict:
    """
    Time series analysis
    """
    from .qube_414188f292 import time_series_analysis
    data_df = sparta_036d8592d3(json_data)
    try:
        x_col = json_data['datesCol']
        y_cols = json_data['returnsCols']
        res_dict = sparta_83057626cf(data_df, x_col, y_cols,
            B_DARK_THEME=json_data.get('B_DARK_THEME', False), start_date=
            json_data.get('startDate', None), end_date=json_data.get(
            'endDate', None), date_type=json_data.get('horizonType', None))
        return {'res': 1, 'analysis': json.dumps(res_dict, allow_nan=False)}
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_9e1f33babb(json_data, user_obj) ->dict:
    """
    Run relationship explorer
    """
    from .qube_414188f292 import relationship_explorer
    data_df = sparta_036d8592d3(json_data)
    try:
        data_df = sparta_49cde73e5b(data_df, json_data)
        res_dict = sparta_ab594fe27f(data_df, json_data['selectedY'],
            json_data['selectedX'], in_sample=json_data.get('bInSample', 
            False), test_size=1 - float(json_data.get('trainTest', 80)) / 
            100, rw_beta=int(json_data['rw_beta']), rw_corr=int(json_data[
            'rw_corr']), B_DARK_THEME=json_data.get('B_DARK_THEME', False))
        return {'res': 1, 'relationship_explorer': json.dumps(res_dict)}
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_da165ab5dc(json_data, user_obj) ->dict:
    """
    Returns dataframe infos
    """
    slug = json_data.get('slug', None)
    user_groups = sparta_09abdd9532(user_obj)
    if len(user_groups) > 0:
        dataframe_user_shared_set = DataFrameShared.objects.filter(Q(
            is_delete=0, user_group__in=user_groups, dataframe_model__slug=
            slug) | Q(is_delete=0, user=user_obj, dataframe_model__slug=slug))
    else:
        dataframe_user_shared_set = DataFrameShared.objects.filter(is_delete
            =0, user=user_obj, dataframe_model__slug=slug)
    if dataframe_user_shared_set.count() == 1:
        dataframe_user_shared_obj = dataframe_user_shared_set[0]
        dataframe_model_obj = dataframe_user_shared_obj.dataframe_model
        dataframe_history_set = DataFrameHistory.objects.filter(dataframe_model
            =dataframe_model_obj)
        res = []
        total_size = 0
        for dataframe_history_obj in dataframe_history_set:
            df_blob = dataframe_history_obj.df_blob
            dispo = dataframe_history_obj.dispo
            res.append({'df_blob': df_blob, 'dispo': dispo})
            if isinstance(df_blob, bytes):
                total_size += len(df_blob)
            else:
                total_size += len(str(df_blob).encode('utf-8'))
            total_size += len(str(dispo).encode('utf-8'))
        date_created = str(dataframe_model_obj.date_created.strftime(
            '%Y-%m-%d'))
        last_update = str(dataframe_model_obj.last_update.strftime(
            '%Y-%m-%d %H:%M:%S'))
        return {'res': 1, 'infos': {'row_nb': len(res), 'size': total_size,
            'last_update': last_update, 'date_created': date_created,
            'name': dataframe_model_obj.table_name, 'slug':
            dataframe_model_obj.slug, 'description': dataframe_model_obj.description, 'is_expose_widget': dataframe_model_obj.is_expose_widget, 'is_public_widget': dataframe_model_obj.is_public_widget, 'has_widget_password': dataframe_model_obj.has_widget_password}}
    return {'res': -1, 'errorMsg':
        'You do not have access to this dataframe...'}


def sparta_7c464016e3(json_data, user_obj) ->dict:
    """
    PCA Analysis: check if sklearn is installed
    """

    def sparta_80ce82edf8():
        try:
            import sklearn
            return True
        except ImportError:
            return False
    return {'res': 1, 'is_sklearn_installed': sparta_80ce82edf8()}


def sparta_dd015eda03(package_name):
    """ Installs a package within the current virtual environment and streams stdout live """
    print(f'install package: {package_name}')
    process = subprocess.Popen([sys.executable, '-m', 'pip', 'install',
        package_name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1)
    output = ''
    for line in process.stdout:
        print(line, end='')
        output += line
    process.wait()
    if process.returncode == 0:
        return {'res': 1, 'success': True, 'output': output, 'is_installed':
            True}
    else:
        return {'res': -1, 'success': False, 'output': output,
            'is_installed': False, 'errorMsg': output}


def sparta_45eb74352a(json_data, user_obj) ->dict:
    """
    Install sklearn
    """
    res_dict = sparta_dd015eda03('scikit-learn')
    return res_dict


def sparta_c4ca903ec4(json_data, user_obj) ->dict:
    """
    RUN pca analysis
    """
    from .qube_414188f292 import run_pca
    data_df = sparta_036d8592d3(json_data)
    try:
        res_pca_dict = sparta_d37279503b(data_df, y_cols=json_data['pcaDataset'],
            n_components=json_data['nbComponents'], explained_variance=
            json_data['nbComponentsVariance'], scale=json_data['bScalePCA'],
            components_mode=json_data['pcaComponentsMode'], B_DARK_THEME=
            json_data.get('B_DARK_THEME', False))
        return res_pca_dict
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback PCA')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_956d6de037(json_data, user_obj) ->dict:
    """
    Run clustering analysis
    """
    from .qube_414188f292 import run_clustering_kmeans, run_clustering_dbscan
    data_df = sparta_036d8592d3(json_data)
    try:
        if json_data['clusteringModel'] == 'Kmean':
            res_clustering_dict = sparta_20c38de387(data_df, y_cols=
                json_data['colDataset'], n_clusters=json_data[
                'nbComponents'], B_DARK_THEME=json_data.get('B_DARK_THEME',
                False))
        else:
            res_clustering_dict = sparta_cebc7a6fa4(data_df, y_cols=
                json_data['colDataset'], min_samples=json_data['minSamples'
                ], epsilon=json_data['epsilon'], B_DARK_THEME=json_data.get
                ('B_DARK_THEME', False))
        return res_clustering_dict
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback clustering')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_12e59f8c45(json_data, user_obj) ->dict:
    """
    Run correlation network analysis
    """
    from .qube_414188f292 import run_correlation_network
    data_df = sparta_036d8592d3(json_data)
    try:
        res_clustering_dict = sparta_12e59f8c45(data_df, y_cols=
            json_data['dataset'], threshold=json_data['threshold'],
            B_DARK_THEME=json_data.get('B_DARK_THEME', False))
        return res_clustering_dict
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback clustering')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_b18dc1eca5(json_data, user_obj) ->dict:
    """
    Run tsne analysis
    """
    from .qube_414188f292 import run_tsne
    data_df = sparta_036d8592d3(json_data)
    try:
        res_clustering_dict = sparta_b18dc1eca5(data_df, y_cols=json_data['dataset'],
            n_components=json_data['nbComponents'], perplexity=json_data[
            'perplexity'], B_DARK_THEME=json_data.get('B_DARK_THEME', False))
        return res_clustering_dict
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback clustering')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_f1405f1445(json_data, user_obj) ->dict:
    """
    Run polynomial regression
    """
    from .qube_414188f292 import run_polynomial_regression
    data_df = sparta_036d8592d3(json_data)
    try:
        res_dict = sparta_f1405f1445(data_df, y_target=json_data[
            'target'], x_cols=json_data['selectedX'], degree=int(json_data.get('degree', 2)), in_sample=json_data.get('bInSample', True),
            standardize=json_data.get('bNormalizePolyReg', True), test_size
            =1 - float(json_data.get('trainTest', 80)) / 100, B_DARK_THEME=
            json_data.get('B_DARK_THEME', False))
        return res_dict
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback polynomial reg')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_58d34bbe0e(json_data, user_obj) ->dict:
    """
    Run decision tree regression
    """
    from .qube_414188f292 import run_decision_tree_regression
    data_df = sparta_036d8592d3(json_data)
    try:
        max_depth = json_data['maxDepth']
        if str(max_depth) == '-1':
            max_depth = None
        else:
            max_depth = int(max_depth)
        res_dict = sparta_58d34bbe0e(data_df, y_target=json_data
            ['target'], x_cols=json_data['selectedX'], max_depth=max_depth,
            in_sample=json_data.get('bInSample', False), standardize=
            json_data.get('bNormalizeDecisionTree', True), test_size=1 - 
            float(json_data.get('trainTest', 80)) / 100, B_DARK_THEME=
            json_data.get('B_DARK_THEME', False))
        return res_dict
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback polynomial reg')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_828e889664(json_data, user_obj) ->dict:
    """
    Run decision tree regression Grid Search CV
    """
    from .qube_414188f292 import run_decision_tree_regression_grid_search
    data_df = sparta_036d8592d3(json_data)
    try:
        max_depth = json_data['maxDepth']
        if str(max_depth) == '-1':
            max_depth = None
        else:
            max_depth = int(max_depth)
        res_dict = sparta_828e889664(data_df,
            y_target=json_data['target'], x_cols=json_data['selectedX'],
            max_depth=max_depth, in_sample=json_data.get('bInSample', False
            ), standardize=json_data.get('bNormalizeDecisionTree', True),
            test_size=1 - float(json_data.get('trainTest', 80)) / 100,
            B_DARK_THEME=json_data.get('B_DARK_THEME', False))
        return res_dict
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback polynomial reg')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_13098e3963(json_data, user_obj) ->dict:
    """
    Run random forest regression
    """
    from .qube_414188f292 import run_random_forest_regression
    data_df = sparta_036d8592d3(json_data)
    try:
        res_dict = sparta_13098e3963(data_df, y_target=json_data
            ['target'], x_cols=json_data['selectedX'], standardize=
            json_data.get('bNormalizeDecisionTree', True), max_depth=
            json_data.get('max_depth', None), in_sample=json_data.get(
            'bInSample', False), test_size=1 - float(json_data.get(
            'trainTest', 80)) / 100, B_DARK_THEME=json_data.get(
            'B_DARK_THEME', False))
        return res_dict
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback polynomial reg')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_46971fbe3c(json_data, user_obj) ->dict:
    """
    Run random forest regression grid search
    """
    from .qube_414188f292 import run_random_forest_regression_grid_search
    data_df = sparta_036d8592d3(json_data)
    try:
        res_dict = sparta_46971fbe3c(data_df,
            y_target=json_data['target'], x_cols=json_data['selectedX'],
            max_depth=json_data.get('max_depth', None), in_sample=json_data.get('bInSample', False), standardize=json_data.get(
            'bNormalizeDecisionTree', True), test_size=1 - float(json_data.get('trainTest', 80)) / 100, B_DARK_THEME=json_data.get(
            'B_DARK_THEME', False))
        return res_dict
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback polynomial reg')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_cb6ad1128b(json_data, user_obj) ->dict:
    """
    Run Quantile regression
    """
    from .qube_414188f292 import run_quantile_regression
    data_df = sparta_036d8592d3(json_data)
    try:
        res_dict = sparta_cb6ad1128b(data_df, y_target=json_data[
            'target'], x_cols=json_data['selectedX'], quantiles=json_data.get('selectedQuantiles', [0.1, 0.5, 0.9]), standardize=
            json_data.get('bNormalizeQuantileReg', True), in_sample=
            json_data.get('bInSample', True), test_size=1 - float(json_data.get('trainTest', 80)) / 100, B_DARK_THEME=json_data.get(
            'B_DARK_THEME', False))
        return res_dict
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback quantile reg')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_30c82c506c(json_data, user_obj) ->dict:
    """
    Run Rolling regression
    """
    print('RUN ROLLING REGRESSION NOW')
    from .qube_414188f292 import run_rolling_regression
    data_df = sparta_036d8592d3(json_data)
    try:
        res_dict = sparta_30c82c506c(data_df, y_target=json_data[
            'target'], x_cols=json_data['selectedX'], window=int(json_data.get('window', 20)), standardize=json_data.get(
            'bNormalizeRollingReg', True), test_size=1 - float(json_data.get('trainTest', 80)) / 100, B_DARK_THEME=json_data.get(
            'B_DARK_THEME', False))
        return res_dict
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback rolling reg')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_7397b20443(json_data, user_obj) ->dict:
    """
    Run Recursive regression
    """
    from .qube_414188f292 import run_recursive_regression
    data_df = sparta_036d8592d3(json_data)
    try:
        res_dict = sparta_7397b20443(data_df, y_target=json_data[
            'target'], x_cols=json_data['selectedX'], standardize=json_data.get('bNormalizeRecursiveReg', True), B_DARK_THEME=json_data.get('B_DARK_THEME', False))
        return res_dict
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback quantile reg')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_192772e288(json_data, user_obj) ->dict:
    """
    Run features importance analysis
    """
    from .qube_414188f292 import run_features_importance_randomforest, run_features_importance_xgboost
    data_df = sparta_036d8592d3(json_data)
    try:
        if json_data['model'] == 'Random Forest':
            res_dict = sparta_f1dbb32097(data_df,
                y_target=json_data['target'], x_cols=json_data['dataset'],
                n_estimators=json_data.get('n_estimators', 100), max_depth=
                json_data.get('max_depth', None), min_samples_split=
                json_data.get('min_samples_split', 1), min_samples_leaf=
                json_data.get('min_samples_leaf', 1), max_features=
                json_data.get('max_features', 'sqrt'), bootstrap=json_data.get('bootstrap', True), B_DARK_THEME=json_data.get(
                'B_DARK_THEME', False))
        else:
            res_dict = sparta_15f8cb4fa6(data_df, y_cols=
                json_data['dataset'], n_components=json_data['nbComponents'
                ], perplexity=json_data['perplexity'], B_DARK_THEME=
                json_data.get('B_DARK_THEME', False))
        return res_dict
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback clustering')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_a8bd61a647(json_data, user_obj) ->dict:
    """
    Run mutual information
    """
    from .qube_414188f292 import run_mutual_information
    data_df = sparta_036d8592d3(json_data)
    try:
        res_dict = sparta_a8bd61a647(data_df, y_target=json_data[
            'target'], x_cols=json_data['dataset'], B_DARK_THEME=json_data.get('B_DARK_THEME', False))
        return res_dict
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback polynomial reg')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_be06ec29aa(json_data, user_obj) ->dict:
    """
    Check if lib installed
    """
    lib = json_data['lib']
    install_but_import_errors = None
    is_installed = False
    if lib == 'arch':
        try:
            import arch
            is_installed = True
        except ImportError:
            is_installed = False
    elif lib == 'wavelet':
        try:
            import pywt
            is_installed = True
            families = []
            if is_installed:
                import pywt
                families = pywt.wavelist()
            return {'res': 1, 'is_installed': is_installed, 'families':
                families}
        except ImportError:
            is_installed = False
    elif lib == 'ruptures':
        try:
            import ruptures as rpt
            is_installed = True
        except ImportError:
            is_installed = False
    elif lib == 'sklearn':
        try:
            import sklearn
            is_installed = True
        except ImportError:
            is_installed = False
    elif lib == 'prophet':
        try:
            from prophet import Prophet
            is_installed = True
        except ImportError:
            is_installed = False
    elif lib == 'keras':
        try:
            import keras
            is_installed = True
        except ModuleNotFoundError as e:
            print(f'module not found: {e}')
            is_installed = False
        except Exception as e:
            print(f'Exception found: {e}')
            is_installed = False
            install_but_import_errors = str(e)
    return {'res': 1, 'is_installed': is_installed,
        'install_but_import_errors': install_but_import_errors}


def sparta_e60325e6fe(json_data, user_obj) ->dict:
    """
    Install lib
    """
    lib = json_data['lib']
    if lib == 'arch':
        res_dict = sparta_dd015eda03('arch')
    elif lib == 'wavelet':
        res_dict = sparta_dd015eda03('PyWavelets')
    elif lib == 'ruptures':
        res_dict = sparta_dd015eda03('ruptures')
    elif lib == 'sklearn':
        res_dict = sparta_dd015eda03('scikit-learn')
    elif lib == 'prophet':
        res_dict = sparta_dd015eda03('prophet')
    elif lib == 'keras':
        res_dict = sparta_dd015eda03('scikit-learn')
        if res_dict['res'] == -1:
            return res_dict
        print('res_dict scikit learn')
        print(res_dict)
        res_dict = sparta_dd015eda03('keras')
        if res_dict['res'] == -1:
            return res_dict
        print('res_dict KERAS')
        print(res_dict)
        res_dict = sparta_dd015eda03('tensorflow')
        if res_dict['res'] == -1:
            return res_dict
        print('res_dict TF')
        print(res_dict)
    return res_dict


def sparta_23dce0f005(json_data, user_obj) ->dict:
    """
    Run features importance analysis
    """
    import project.sparta_8688631f3d.sparta_8c6a44fbc0.qube_054e97a968 as qube_054e97a968
    data_df = sparta_036d8592d3(json_data)
    tsa_model = json_data['tsaModel']
    try:
        if tsa_model == 'adf':
            cols_dataset = json_data['colDataset']
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_fa8803935a(data_df, json_data.get(
                'params', None))
        elif tsa_model == 'kpss':
            cols_dataset = json_data['colDataset']
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_34e6c46007(data_df, json_data.get(
                'params', None))
        elif tsa_model == 'perron':
            cols_dataset = json_data['colDataset']
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_0bbdb27917(data_df, json_data.get(
                'params', None))
        elif tsa_model == 'za':
            cols_dataset = json_data['colDataset']
            date_col = json_data.get('dateCol', None)
            dates_series = data_df[date_col]
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_ff2c453a66(data_df, dates_series,
                json_data.get('params', None), B_DARK_THEME=json_data.get(
                'B_DARK_THEME', False))
        elif tsa_model == 'stl':
            cols_dataset = json_data['colDataset']
            date_col = json_data['dateCol']
            dates_series = None
            if date_col is not None:
                if len(date_col) > 0:
                    try:
                        dates_series = data_df[date_col]
                    except:
                        dates_series = None
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_aaa67c8beb(data_df, dates_series, json_data.get('params', None), B_DARK_THEME=json_data.get(
                'B_DARK_THEME', False))
        elif tsa_model == 'wavelet':
            cols_dataset = json_data['colDataset']
            date_col = json_data['dateCol']
            dates_series = None
            if date_col is not None:
                if len(date_col) > 0:
                    try:
                        dates_series = data_df[date_col]
                    except:
                        dates_series = None
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_b31582ba62(data_df, dates_series,
                json_data.get('params', None), B_DARK_THEME=json_data.get(
                'B_DARK_THEME', False))
        elif tsa_model == 'hmm':
            cols_dataset = json_data['colDataset']
            date_col = json_data.get('dateCol', None)
            dates_series = None
            if date_col is not None:
                if len(date_col) > 0:
                    try:
                        dates_series = data_df[date_col]
                    except:
                        dates_series = None
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_a1b8205d91(data_df, dates_series, json_data.get('params', None), B_DARK_THEME=json_data.get(
                'B_DARK_THEME', False))
        elif tsa_model == 'ruptures':
            cols_dataset = json_data['colDataset']
            date_col = json_data.get('dateCol', None)
            dates_series = None
            if date_col is not None:
                if len(date_col) > 0:
                    try:
                        dates_series = data_df[date_col]
                    except:
                        dates_series = None
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_9113fda66f(data_df, dates_series,
                json_data.get('params', None), B_DARK_THEME=json_data.get(
                'B_DARK_THEME', False))
        elif tsa_model == 'cusum':
            cols_dataset = json_data['colDataset']
            date_col = json_data.get('dateCol', None)
            dates_series = None
            if date_col is not None:
                if len(date_col) > 0:
                    try:
                        dates_series = data_df[date_col]
                    except:
                        dates_series = None
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_85ada6b2e9(data_df, dates_series,
                json_data.get('params', None), B_DARK_THEME=json_data.get(
                'B_DARK_THEME', False))
        elif tsa_model == 'zscore':
            cols_dataset = json_data['colDataset']
            date_col = json_data.get('dateCol', None)
            dates_series = None
            if date_col is not None:
                if len(date_col) > 0:
                    try:
                        dates_series = data_df[date_col]
                    except:
                        dates_series = None
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_7b77175e3f(data_df, dates_series,
                json_data.get('params', None), B_DARK_THEME=json_data.get(
                'B_DARK_THEME', False))
        elif tsa_model == 'isolationForest':
            cols_dataset = json_data['colDataset']
            date_col = json_data.get('dateCol', None)
            dates_series = None
            if date_col is not None:
                if len(date_col) > 0:
                    try:
                        dates_series = data_df[date_col]
                    except:
                        dates_series = None
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_2d743610de(data_df,
                dates_series, json_data.get('params', None), B_DARK_THEME=
                json_data.get('B_DARK_THEME', False))
        elif tsa_model == 'madMedian':
            cols_dataset = json_data['colDataset']
            date_col = json_data.get('dateCol', None)
            dates_series = None
            if date_col is not None:
                if len(date_col) > 0:
                    try:
                        dates_series = data_df[date_col]
                    except:
                        dates_series = None
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_6a58641189(data_df,
                dates_series, json_data.get('params', None), B_DARK_THEME=
                json_data.get('B_DARK_THEME', False))
        elif tsa_model == 'prophetOutlier':
            cols_dataset = json_data['colDataset']
            date_col = json_data.get('dateCol', None)
            dates_series = None
            if date_col is not None:
                if len(date_col) > 0:
                    try:
                        dates_series = data_df[date_col]
                    except:
                        dates_series = None
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_4b85f428e7(data_df,
                dates_series, json_data.get('params', None), B_DARK_THEME=
                json_data.get('B_DARK_THEME', False))
        elif tsa_model == 'granger':
            cols_dataset = json_data['colDataset']
            target = json_data['target']
            target_series = data_df[target]
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_cd935bb29f(data_df, target_series,
                json_data.get('params', None), B_DARK_THEME=json_data.get(
                'B_DARK_THEME', False))
        elif tsa_model == 'cointegration':
            cols_dataset = json_data['colDataset']
            target = json_data['target']
            target_series = data_df[target]
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_93698c5868(data_df,
                target_series, json_data.get('params', None), B_DARK_THEME=
                json_data.get('B_DARK_THEME', False))
        elif tsa_model == 'canonical_corr':
            cols_dataset_1 = json_data['colDataset1']
            cols_dataset_2 = json_data['colDataset2']
            data1_df = data_df[cols_dataset_1]
            data2_df = data_df[cols_dataset_2]
            return qube_054e97a968.sparta_2949500dfc(data1_df,
                data2_df, json_data.get('params', None), B_DARK_THEME=
                json_data.get('B_DARK_THEME', False))
        elif tsa_model == 'sarima':
            cols_dataset = json_data['colDataset']
            date_col = json_data.get('dateCol', None)
            dates_series = None
            if date_col is not None:
                if len(date_col) > 0:
                    try:
                        dates_series = data_df[date_col]
                    except:
                        dates_series = None
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_a32431de61(data_df, dates_series,
                json_data.get('params', None), B_DARK_THEME=json_data.get(
                'B_DARK_THEME', False))
        elif tsa_model == 'ets':
            cols_dataset = json_data['colDataset']
            date_col = json_data.get('dateCol', None)
            dates_series = None
            if date_col is not None:
                if len(date_col) > 0:
                    try:
                        dates_series = data_df[date_col]
                    except:
                        dates_series = None
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_54a5d4960b(data_df, dates_series, json_data.get('params', None), B_DARK_THEME=json_data.get(
                'B_DARK_THEME', False))
        elif tsa_model == 'prophetForecast':
            cols_dataset = json_data['colDataset']
            date_col = json_data.get('dateCol', None)
            dates_series = None
            if date_col is not None:
                if len(date_col) > 0:
                    try:
                        dates_series = data_df[date_col]
                    except:
                        dates_series = None
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_d227332dbc(data_df,
                dates_series, json_data.get('params', None), B_DARK_THEME=
                json_data.get('B_DARK_THEME', False))
        elif tsa_model == 'lstm':
            cols_dataset = json_data['colDataset']
            date_col = json_data.get('dateCol', None)
            dates_series = None
            if date_col is not None:
                if len(date_col) > 0:
                    try:
                        dates_series = data_df[date_col]
                    except:
                        dates_series = None
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_24936163ab(data_df, dates_series,
                json_data.get('params', None), B_DARK_THEME=json_data.get(
                'B_DARK_THEME', False))
        elif tsa_model == 'var':
            cols_dataset = json_data['colDataset']
            date_col = json_data.get('dateCol', None)
            dates_series = None
            if date_col is not None:
                if len(date_col) > 0:
                    try:
                        dates_series = data_df[date_col]
                    except:
                        dates_series = None
            data_df = data_df[cols_dataset]
            return qube_054e97a968.sparta_ae44c4a420(data_df, dates_series, json_data.get('params', None), B_DARK_THEME=json_data.get(
                'B_DARK_THEME', False))
    except Exception as e:
        this_traceback = traceback.format_exc()
        print('this_traceback TSA')
        print(this_traceback)
        return {'res': -1, 'errorMsg': str(e)}


def sparta_b0d5903f1f(token_permission) ->dict:
    """
    Check if has plotDB access using token (PlotDBPermission model)
    This is used to access plotDB from the API from dashboard/notebook without authenticating user (or owner user)
    """
    dataframe_permission_set = DataFramePermission.objects.filter(token=
        token_permission)
    dataframe_permission_count = dataframe_permission_set.count()
    if dataframe_permission_count > 0:
        dataframe_permission_obj = dataframe_permission_set[
            dataframe_permission_count - 1]
        return {'res': 1, 'dataframe_model_obj': dataframe_permission_obj.dataframe_model}
    return {'res': -1}


def has_permission_widget_or_shared_rights(dataframe_model_obj, user_obj,
    password_widget=None) ->bool:
    """
    This function returns True if the user has the permission to read the widget and False otherwise
    """
    has_widget_password = dataframe_model_obj.has_widget_password
    has_shared_right = False
    if user_obj.is_authenticated:
        user_groups = sparta_09abdd9532(user_obj)
        if len(user_groups) > 0:
            dataframe_shared_set = DataFrameShared.objects.filter(Q(
                is_delete=0, user_group__in=user_groups,
                dataframe_model__is_delete=0, dataframe_model=
                dataframe_model_obj) | Q(is_delete=0, user=user_obj,
                dataframe_model__is_delete=0, dataframe_model=
                dataframe_model_obj))
        else:
            dataframe_shared_set = DataFrameShared.objects.filter(is_delete
                =0, user=user_obj, dataframe_model__is_delete=0,
                dataframe_model=dataframe_model_obj)
        if dataframe_shared_set.count() > 0:
            has_shared_right = True
    if has_shared_right:
        return True
    if dataframe_model_obj.is_expose_widget:
        if dataframe_model_obj.is_public_widget:
            if not has_widget_password:
                return True
            else:
                try:
                    if qube_c71ace27e3.sparta_5b66dfafff(
                        dataframe_model_obj.widget_password_e
                        ) == password_widget:
                        return True
                    else:
                        return False
                except:
                    return False
        else:
            return False
    return False


def sparta_b64f60322d(slug, user_obj, password_widget=None) ->dict:
    """
    Check if user can access widget (read only). This is used at the view level (see def plot_widget in viewPlotDB.py)
    res: 
        1  Can access widget
        2  No access, require password (missing password)
        3  No access, wrong password
       -1  Not allowed, redirect to login   
    """
    logger.debug(f'CHECK NOW has_widget_access: {slug}')
    dataframe_model_set = DataFrameModel.objects.filter(slug=slug,
        is_delete=False).all()
    b_found = False
    dataframe_model_count = dataframe_model_set.count()
    if dataframe_model_count == 1:
        b_found = True
    if not b_found:
        dataframe_model_set = DataFrameModel.objects.filter(slug__startswith
            =slug, is_delete=False).all()
        dataframe_model_count = dataframe_model_set.count()
        if dataframe_model_count == 1:
            b_found = True
    if b_found:
        dataframe_model_obj = dataframe_model_set[dataframe_model_count - 1]
        has_widget_password = dataframe_model_obj.has_widget_password
        if dataframe_model_obj.is_expose_widget:
            if dataframe_model_obj.is_public_widget:
                if not has_widget_password:
                    return {'res': 1, 'dataframe_model_obj':
                        dataframe_model_obj}
                elif password_widget is None:
                    return {'res': 2, 'errorMsg': 'Require password',
                        'dataframe_model_obj': dataframe_model_obj}
                else:
                    try:
                        if qube_c71ace27e3.sparta_5b66dfafff(
                            dataframe_model_obj.widget_password_e
                            ) == password_widget:
                            return {'res': 1, 'dataframe_model_obj':
                                dataframe_model_obj}
                        else:
                            return {'res': 3, 'errorMsg':
                                'Invalid password', 'dataframe_model_obj':
                                dataframe_model_obj}
                    except:
                        return {'res': 3, 'errorMsg': 'Invalid password',
                            'dataframe_model_obj': dataframe_model_obj}
            elif user_obj.is_authenticated:
                user_groups = sparta_09abdd9532(user_obj)
                if len(user_groups) > 0:
                    dataframe_shared_set = DataFrameShared.objects.filter(Q
                        (is_delete=0, user_group__in=user_groups,
                        dataframe_model__is_delete=0, dataframe_model=
                        dataframe_model_obj) | Q(is_delete=0, user=user_obj,
                        dataframe_model__is_delete=0, dataframe_model=
                        dataframe_model_obj))
                else:
                    dataframe_shared_set = DataFrameShared.objects.filter(
                        is_delete=0, user=user_obj,
                        dataframe_model__is_delete=0, dataframe_model=
                        dataframe_model_obj)
                if dataframe_shared_set.count() > 0:
                    return {'res': 1, 'dataframe_model_obj':
                        dataframe_model_obj}
            else:
                return {'res': -1}
    return {'res': -1}


def sparta_558bd9a739(slug, user_obj) ->dict:
    """
    Check if user can access to plot (read only)
    We only check if we have shared rights (or owner)
    """
    dataframe_model_set = DataFrameModel.objects.filter(slug=slug,
        is_delete=False).all()
    b_found = False
    dataframe_model_count = dataframe_model_set.count()
    if dataframe_model_count == 1:
        b_found = True
    if not b_found:
        dataframe_model_set = DataFrameModel.objects.filter(slug__startswith
            =slug, is_delete=False).all()
        dataframe_model_count = dataframe_model_set.count()
        if dataframe_model_count == 1:
            b_found = True
    if b_found:
        dataframe_model_obj = dataframe_model_set[0]
        user_groups = sparta_09abdd9532(user_obj)
        if len(user_groups) > 0:
            dataframe_shared_set = DataFrameShared.objects.filter(Q(
                is_delete=0, user_group__in=user_groups,
                dataframe_model__is_delete=0, dataframe_model=
                dataframe_model_obj) | Q(is_delete=0, user=user_obj,
                dataframe_model__is_delete=0, dataframe_model=
                dataframe_model_obj))
        else:
            dataframe_shared_set = DataFrameShared.objects.filter(is_delete
                =0, user=user_obj, dataframe_model__is_delete=0,
                dataframe_model=dataframe_model_obj)
        if dataframe_shared_set.count() > 0:
            dataframe_shared_obj = dataframe_shared_set[0]
            dataframe_model_obj = dataframe_shared_obj.dataframe_model
            return {'res': 1, 'has_access': True, 'dataframe_model_obj':
                dataframe_model_obj}
    return {'res': 1, 'has_access': False}

#END OF QUBE
