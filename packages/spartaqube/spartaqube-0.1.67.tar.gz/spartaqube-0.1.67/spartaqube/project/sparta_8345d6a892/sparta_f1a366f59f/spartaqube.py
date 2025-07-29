import os
import json
import uuid
import base64
import pickle
import pandas as pd
import urllib.parse
from IPython.core.display import display, HTML
import warnings
warnings.filterwarnings('ignore', message=
    'Consider using IPython.display.IFrame instead', category=UserWarning)
from datetime import datetime, timedelta
import pytz
UTC = pytz.utc
from project.models import UserProfile, PlotDBChart, PlotDBChartShared, PlotDBPermission, DataFrameShared, DataFramePermission
from project.sparta_8345d6a892.sparta_f1a366f59f.qube_137201374c import sparta_a65a94aacc
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import convert_to_dataframe, convert_dataframe_to_json, process_dataframe_components
from project.sparta_8345d6a892.sparta_952c41e91e.qube_68510697e1 import sparta_078b7892c7
from project.sparta_8345d6a892.sparta_950a603163 import qube_2ab426de66 as qube_2ab426de66


class Spartaqube:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, api_token_id=None):
        if self._initialized:
            return
        self._initialized = True
        if api_token_id is None:
            try:
                api_token_id = os.environ['api_key']
            except:
                pass
        self.api_token_id = api_token_id
        self.user_obj = UserProfile.objects.get(api_key=api_token_id).user

    def test(self):
        print('test')

    def get_widget_data(self, widget_id) ->list:
        json_data = {'api_service': 'get_widget_data', 'widget_id': widget_id}
        return sparta_a65a94aacc(json_data, self.user_obj)

    def sparta_b9447b9359(self, widget_id) ->list:
        json_data = {'api_service': 'has_widget_id', 'widget_id': widget_id}
        return sparta_a65a94aacc(json_data, self.user_obj)

    def get_widget(self, widget_id, width='100%', height=500) ->list:
        """
        Get widget iframe
        Owner of widget is supposed to be logged in the kernel to access this widget 
        """
        plot_db_chart_shared_set = PlotDBChartShared.objects.filter(is_delete
            =0, user=self.user_obj, plot_db_chart__is_delete=0,
            plot_db_chart__plot_chart_id=widget_id)
        if plot_db_chart_shared_set.count() > 0:
            token = str(uuid.uuid4())
            date_now = datetime.now().astimezone(UTC)
            PlotDBPermission.objects.create(plot_db_chart=
                plot_db_chart_shared_set[0].plot_db_chart, token=token,
                date_created=date_now)
            return HTML(
                f'<iframe src="/plot-widget-token/{token}" width="{width}" height="{height}" frameborder="0" allow="clipboard-write"></iframe>'
                )
        return 'You do not have the rights to access this object'

    def iplot(self, *argv, width='100%', height=550):
        """
        Interactive plot
        """
        if len(argv) == 0:
            raise Exception('You must pass at least one input variable to plot'
                )
        else:
            notebook_variables_dict = dict()
            for key_idx, value in enumerate(argv):
                if value is None:
                    continue
                notebook_variables_df = convert_to_dataframe(value)
                notebook_variables_dict[key_idx] = convert_dataframe_to_json(
                    notebook_variables_df)
            serialized_data = json.dumps(notebook_variables_dict)
            iframe_id = str(uuid.uuid4())
            iframe_html = f"""
                <form id="dataForm_{iframe_id}" action="plot-gui" method="POST" target="{iframe_id}">
                    <input type="hidden" name="data" value='{serialized_data}' />
                </form>
                <iframe 
                    id="{iframe_id}"
                    name="{iframe_id}"
                    width="{width}" 
                    height="{height}" 
                    frameborder="0" 
                    allow="clipboard-write"></iframe>

                <script>
                    // Submit the form automatically to send data to the iframe
                    document.getElementById('dataForm_{iframe_id}').submit();
                </script>
                """
            return HTML(iframe_html)

    def plot(self, *argv, **kwargs):
        """
        Plot API (also used for plot_template)
        """
        notebook_variables_dict = dict()
        for key, var in kwargs.items():
            if var is None:
                continue
            notebook_variables_df = convert_to_dataframe(var)
            notebook_variables_dict[key] = convert_dataframe_to_json(
                notebook_variables_df)
        type_chart = None
        if 'chart_type' not in kwargs:
            if 'widget_id' not in kwargs:
                raise Exception(
                    "Missing chart_type parameter. For instance: chart_type='line'"
                    )
            else:
                type_chart = 0
        if type_chart is None:
            plot_types_list = sparta_078b7892c7(b_return_type_id
                =True)
            try:
                chart_type = json.loads(notebook_variables_dict['chart_type'])[
                    'data'][0][0]
                type_chart = [elem for elem in plot_types_list if elem['ID'
                    ] == chart_type][0]['type_plot']
            except:
                raise Exception(
                    'Invalid chart type. Use an ID found in the DataFrame get_plot_types()'
                    )
        width = kwargs.get('width', '100%')
        height = kwargs.get('width', '500')
        interactive = kwargs.get('interactive', True)
        widget_id = kwargs.get('widget_id', None)
        vars_html_dict = {'interactive_api': 1 if interactive else 0,
            'is_api_template': 1 if widget_id is not None else 0,
            'widget_id': widget_id}
        json_vars_html = json.dumps(vars_html_dict)
        encoded_json_str = urllib.parse.quote(json_vars_html)
        data_res_dict = dict()
        data_res_dict['res'] = 1
        data_res_dict['notebook_variables'] = notebook_variables_dict
        data_res_dict['type_chart'] = type_chart
        data_res_dict['override_options'] = notebook_variables_dict.get(
            'options', dict())
        print('data_res_dict')
        print(data_res_dict)
        serialized_data = json.dumps(data_res_dict)
        iframe_id = str(uuid.uuid4())
        iframe_html = f"""
            <form id="dataForm_{iframe_id}" action="plot-api/{encoded_json_str}" method="POST" target="{iframe_id}">
                <input type="hidden" name="data" value='{serialized_data}' />
            </form>
            <iframe 
                id="{iframe_id}"
                name="{iframe_id}"
                width="{width}" 
                height="{height}" 
                frameborder="0" 
                allow="clipboard-write"></iframe>

            <script>
                // Submit the form automatically to send data to the iframe
                document.getElementById('dataForm_{iframe_id}').submit();
            </script>
            """
        return HTML(iframe_html)

    def plot_documentation(self, chart_type='line'):
        """
        This function should display both the command (code) and display the output
        """
        plot_types_list = self.get_plot_types()
        if len([elem for elem in plot_types_list if elem['ID'] == chart_type]
            ) > 0:
            url_doc = f'api#plot-{chart_type}'
            return url_doc
        else:
            raise Exception(
                'Invalid chart type. Use an ID found in the DataFrame get_plot_types()'
                )

    def plot_template(self, *args, **kwargs):
        """
        Plot template, call plot method with a widget_id
        """
        if 'widget_id' in kwargs:
            return self.plot(*args, **kwargs)
        raise Exception('Missing widget_id')

    def get_connector_tables(self, connector_id) ->list:
        json_data = {'api_service': 'get_connector_tables', 'connector_id':
            connector_id}
        return sparta_a65a94aacc(json_data, self.user_obj)

    def get_data_from_connector(self, connector_id, table=None, sql_query=
        None, output_format=None, dynamic_inputs: list=None) ->list:
        json_data = {'api_service': 'get_data_from_connector'}
        json_data['connector_id'] = connector_id
        json_data['table_name'] = table
        json_data['query_filter'] = sql_query
        json_data['bApplyFilter'] = 1 if sql_query is not None else 0
        dynamic_inputs_params = []
        if dynamic_inputs is not None:
            for key, val in dynamic_inputs.items():
                dynamic_inputs_params.append({'input': key, 'default': val})
        json_data['dynamic_inputs'] = dynamic_inputs_params
        res_data_dict = sparta_a65a94aacc(json_data, self.user_obj)
        is_df_format = False
        if output_format is None:
            is_df_format = True
        elif output_format == 'DataFrame':
            is_df_format = True
        if is_df_format:
            if res_data_dict['res'] == 1:
                data_dict_ = json.loads(res_data_dict['data'])
            return pd.DataFrame(data_dict_['data'], index=data_dict_[
                'index'], columns=data_dict_['columns'])
        return res_data_dict

    def apply_method(self, method_name, *args, **kwargs):
        """
        
        """
        json_data = kwargs
        json_data['api_service'] = method_name
        return sparta_a65a94aacc(json_data, self.user_obj)

    def __getattr__(self, name):
        return lambda *args, **kwargs: self.apply_method(name, *args, **kwargs)

    def sparta_d8865dd244(self, dispo) ->str:
        dispo_blob = pickle.dumps(dispo)
        return base64.b64encode(dispo_blob).decode('utf-8')

    def sparta_7a629ed005(self, df: pd.DataFrame, table_name: str, dispo=None, mode=
        'append'):
        """
        Insert dataframe
        mode: append or replace. If replace, it is based on the dispo date
        """
        data_dict = {'api_service': 'put_df'}
        blob = pickle.dumps(df)
        encoded_blob = base64.b64encode(blob).decode('utf-8')
        data_dict['df'] = encoded_blob
        data_dict['table_name'] = table_name
        data_dict['mode'] = mode
        data_dict['dispo'] = self.format_dispo(dispo)
        if mode not in ['append', 'replace']:
            raise Exception("Mode should be: 'append' or 'replace'")
        if isinstance(dispo, pd.Series) or isinstance(dispo, pd.DatetimeIndex
            ) or type(dispo).__name__ == 'ndarray' and type(dispo
            ).__module__ == 'numpy':
            dispo = list(dispo)
            data_dict['dispo'] = self.format_dispo(dispo)
        if isinstance(dispo, list):
            if len(dispo) != len(df):
                raise Exception(
                    'If you want to use a list of dispo, it must have the same length at the dataframe'
                    )
        res_dict = qube_2ab426de66.sparta_7a629ed005(data_dict, self.user_obj)
        if res_dict['res'] == 1:
            print('Dataframe inserted successfully!')
        return res_dict

    def sparta_9235b6fd90(self, table_name, slug=None):
        """
        Drop dataframe
        """
        data_dict = {'api_service': 'drop_df'}
        data_dict['table_name'] = table_name
        data_dict['slug'] = slug
        res_dict = qube_2ab426de66.sparta_9235b6fd90(data_dict, self.user_obj)
        if res_dict['res'] == 1:
            print('Dataframe dropped successfully!')
        return res_dict

    def sparta_d5ca62aae2(self, id):
        """
        Drop the dataframe using id
        """
        data_dict = {'api_service': 'drop_df_by_id'}
        data_dict['id'] = id
        res_dict = qube_2ab426de66.sparta_d5ca62aae2(data_dict, self.user_obj)
        if res_dict['res'] == 1:
            print(f'Dataframe dropped successfully for dispo!')
        return res_dict

    def sparta_691a6f0511(self, table_name, dispo, slug=None):
        """
        Drop specific dispo date
        """
        data_dict = {'api_service': 'drop_dispo_df'}
        data_dict['table_name'] = table_name
        data_dict['dispo'] = self.format_dispo(dispo)
        data_dict['slug'] = slug
        res_dict = qube_2ab426de66.sparta_691a6f0511(data_dict, self.user_obj)
        if res_dict['res'] == 1:
            print(f'Dataframe dropped successfully for dispo {dispo} !')
        return res_dict

    def sparta_9213552ac5(self) ->pd.DataFrame:
        """
        Get available dataframes
        """
        data_dict = {'api_service': 'get_available_df'}
        return qube_2ab426de66.sparta_9213552ac5(data_dict, self.user_obj)

    def sparta_56b6ba7925(self, table_name, dispo=None, slug=None, b_concat=True
        ) ->pd.DataFrame:
        """
        Get dataframe
        """
        data_dict = {'api_service': 'get_df'}
        data_dict['table_name'] = table_name
        data_dict['dispo'] = self.format_dispo(dispo)
        data_dict['slug'] = slug
        res_dict = qube_2ab426de66.sparta_56b6ba7925(data_dict, self.user_obj)
        if res_dict['res'] == 1:
            data_list = pickle.loads(base64.b64decode(res_dict[
                'encoded_blob'].encode('utf-8')))
            data_df_list = [pickle.loads(elem_dict['df_blob']).assign(dispo
                =elem_dict['dispo']) for elem_dict in data_list]
            if b_concat:
                try:
                    df_all = pd.concat(data_df_list)
                    df_all = process_dataframe_components(df_all)
                    return df_all
                except Exception as e:
                    print(
                        'Could not concatenate all dataframes together with following error message:'
                        )
                    raise str(e)
            else:
                return data_df_list
        return res_dict

    def open_df(self, dataframe_id, width='100%', height=500) ->list:
        """
        Get widget iframe
        Owner of widget is supposed to be logged in the kernel to access this widget 
        """
        dataframe_shared_set = DataFrameShared.objects.filter(is_delete=0,
            user=self.user_obj, plot_db_chart__is_delete=0,
            plot_db_chart__plot_chart_id=widget_id)
        if dataframe_shared_set.count() > 0:
            token = str(uuid.uuid4())
            date_now = datetime.now().astimezone(UTC)
            DataFramePermission.objects.create(dataframe_model=
                dataframe_shared_set[0].plot_db_chart, token=token,
                date_created=date_now)
            return HTML(
                f'<iframe src="/plot-dataframe-token/{token}" width="{width}" height="{height}" frameborder="0" allow="clipboard-write"></iframe>'
                )
        return 'You do not have the rights to access this object'

    def sparta_b734dce1d2(self, slug) ->list:
        json_data = {'api_service': 'has_dataframe_slug', 'slug': slug}
        return sparta_a65a94aacc(json_data, self.user_obj)

    def open_data_df(self, data_df: pd.DataFrame, name='', width='100%',
        height=600, detached=False):
        """
        Open dataframe in iframe (GUI mode)
        """
        iframe_id = str(uuid.uuid4())
        df_json = convert_dataframe_to_json(data_df)
        serialized_data = json.dumps(df_json)
        iframe_name = iframe_id
        if detached:
            iframe_name = name
        iframe_html = f"""
        <form id="dataForm_{iframe_id}" action="/plot-gui-df" method="POST" target="{iframe_id}">
            <input type="hidden" name="data" value='{serialized_data}' />
            <input type="hidden" name="name" value='{name}' />
        </form>
        <iframe 
            id="{iframe_id}"
            name="{iframe_name}"
            width="{width}" 
            height="{height}" 
            frameborder="0" 
            allow="clipboard-write"></iframe>
        <script>
            // Submit the form automatically to send data to the iframe
            document.getElementById('dataForm_{iframe_id}').submit();
        </script>
        """
        return HTML(iframe_html)

#END OF QUBE
