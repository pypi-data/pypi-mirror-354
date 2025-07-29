import os, sys, re
from django.conf import settings
import project.sparta_8688631f3d.sparta_5d2f5154f8.sparta_5156b948f0.qube_e7e0ebc552 as qube_e7e0ebc552
import project.sparta_8688631f3d.sparta_5d2f5154f8.sparta_5156b948f0.qube_74eb19d84b as qube_74eb19d84b
import project.sparta_8688631f3d.sparta_5d2f5154f8.sparta_5156b948f0.qube_6f8733073a as qube_6f8733073a
import project.sparta_8688631f3d.sparta_5d2f5154f8.sparta_5156b948f0.qube_5fc31a7036 as qube_5fc31a7036
import project.sparta_8688631f3d.sparta_5d2f5154f8.sparta_24d1ca3e0e.qube_431bf62423 as qube_431bf62423
import project.sparta_8688631f3d.sparta_5d2f5154f8.sparta_24d1ca3e0e.qube_d37c1119ad as qube_d37c1119ad
import project.sparta_8688631f3d.sparta_5d2f5154f8.sparta_24d1ca3e0e.qube_87c11c0f45 as qube_87c11c0f45
import project.sparta_8688631f3d.sparta_5d2f5154f8.sparta_24d1ca3e0e.qube_4cb927777e as qube_4cb927777e
import project.sparta_8688631f3d.sparta_5d2f5154f8.sparta_24d1ca3e0e.qube_cd259f35a4 as qube_cd259f35a4
import project.sparta_8688631f3d.sparta_5d2f5154f8.sparta_24d1ca3e0e.qube_a29924008c as qube_a29924008c
import project.sparta_8688631f3d.sparta_5d2f5154f8.sparta_24d1ca3e0e.qube_ae17c53ef5 as qube_ae17c53ef5
import project.sparta_8688631f3d.sparta_5d2f5154f8.sparta_24d1ca3e0e.qube_e42b4354f9 as qube_e42b4354f9


def sparta_6d633ad2e5(b_return_type_id=False) ->list:
    """
    Return list of available plot type (for api)
    """

    def extract_values_by_key(input_string, key='typeId'):
        escaped_key = re.escape(key)
        pattern = f'\'{escaped_key}\':\\s*(true|false|\\d+|\'.*?\'|\\".*?\\")'
        matches = re.findall(pattern, input_string, re.IGNORECASE)
        values = [m.strip('\'"') for m in matches]
        return values

    def parse_js_file(file_path) ->list:
        with open(file_path, 'r') as file:
            content = file.read()
        content = content.split('// PARSED ENDLINE COMMENT (DO NOT REMOVE)')[0]
        js_content = content
        match = re.search('return\\s*({[\\s\\S]*?});', js_content)
        if not match:
            raise ValueError('No return dictionary found in the file.')
        js_dict_str = match.group(1)
        typeid_list = extract_values_by_key(js_dict_str, 'typeId')
        slug_api_list = extract_values_by_key(js_dict_str, 'slugApi')
        display_list = extract_values_by_key(js_dict_str, 'display')
        name_list = extract_values_by_key(js_dict_str, 'name')
        library_list = extract_values_by_key(js_dict_str, 'libraryName')
        plot_types = []
        cnt = 0
        for idx, _ in enumerate(typeid_list):
            if display_list[idx] == 'true':
                slug_api = slug_api_list[idx]
                if slug_api != '-1' and len(slug_api) > 0:
                    tmp_dict = {'ID': slug_api_list[idx], 'Name': name_list
                        [idx], 'Library': library_list[idx]}
                    if b_return_type_id or True:
                        tmp_dict['type_plot'] = typeid_list[idx]
                    plot_types.append(tmp_dict)
                    cnt += 1
        return plot_types
    current_path = os.path.dirname(__file__)
    core_path = os.path.dirname(current_path)
    project_path = os.path.dirname(core_path)
    main_path = os.path.dirname(project_path)
    if settings.DEBUG:
        static_path = os.path.join(main_path, 'static')
    else:
        static_path = os.path.join(main_path, 'staticfiles')
    file_path = os.path.join(static_path,
        'js/vueComponent/plot-db/new-plot/plot-config/plotConfigMixin.js')
    if not os.path.exists(file_path):
        file_path = os.path.join(static_path, 'js/util/plotConfigMixin.js')
    file_path = os.path.normpath(file_path)
    plot_types: list = parse_js_file(file_path)
    return plot_types


def sparta_53106fda48() ->dict:
    """
    
    """
    argument_descriptions_mapper = {'x': {'type': ['list',
        'DataFrame Index'], 'description':
        'list or DataFrame index representing the x axis of your chart'},
        'y': {'type': ['list', 'list[list]', 'pd.DataFrame',
        '[pd.Series, pd.Series...]'], 'description':
        'list, list of lists, DataFrame, or list of Series representing the lines to plot'
        }, 'r': {'type': ['list', 'list[list]', 'pd.DataFrame',
        '[pd.Series, pd.Series...]'], 'description':
        'list, list of lists, DataFrame, or list of Series representing the radius to plot'
        }, 'stacked': {'type': ['boolean'], 'description':
        'If True and multiple series, all the series will be stacked together'
        }, 'date_format': {'type': ['str'], 'description':
        'For instance: yyyy-MM-dd, dd/MM/yyyy, yyyy-MM-dd HH:MM:SS etc... year: y, month: M, day: d, quarter: QQQ, week: w, hour: HH, minute: MM, seconds: SS, millisecond: ms'
        }, 'legend': {'type': ['list'], 'description':
        "A list containing the names of each series in your chart. Each element in the list corresponds to the name of a series, which will be displayed in the chart's legend."
        }, 'labels': {'type': ['list', 'list[list]'], 'description':
        'A list or list of lists containing the labels for each point (scatter/bubble chart).'
        }, 'ohlcv': {'type': ['pd.DataFrame()',
        '[open:list, high:list, low:list, close:list, volume:list]',
        '[open:pd.Series, high:pd.Series, low:pd.Series, close:pd.Series, volume:pd.Series]'
        ], 'description':
        'DataFrame with Open, High, Low, Close and optionally Volumes columns. Or a list containing eight list or pd.Series of Open, High, Low, Close and optionally volumes.'
        }, 'shaded_background': {'type': ['list', 'list[list]',
        'pd.DataFrame', '[pd.Series, pd.Series...]'], 'description':
        'The shaded_background input should be a list of numerical values representing the intensity levels of the shaded background, where each value corresponds to a specific color gradient'
        }, 'datalabels': {'type': ['list', 'list[list]'], 'description':
        'For charts containing a single series, provide a list of strings to represent the label of each point. If your chart includes multiple series, supply a list of lists, where each inner list specifies the labels for the points on each corresponding series'
        }, 'border': {'type': ['list', 'list[list]'], 'description':
        'For charts containing a single series, provide a list of color strings (in hex, rgb, or rgba format) to represent the border color of each point. If your chart includes multiple series, supply a list of lists, where each inner list specifies the border colors for the points on each corresponding series'
        }, 'background': {'type': ['list', 'list[list]'], 'description':
        'For charts containing a single series, provide a list of color strings (in hex, rgb, or rgba format) to represent the background color of each point. If your chart includes multiple series, supply a list of lists, where each inner list specifies the background colors for the points on each corresponding series'
        }, 'tooltips_title': {'type': ['list', 'list[list]'], 'description':
        'For charts containing a single series, provide a list of strings to represent the tooltip title of each point. If your chart includes multiple series, supply a list of lists, where each inner list specifies the tooltips for the points on each corresponding series'
        }, 'tooltips_label': {'type': ['list', 'list[list]'], 'description':
        'For charts containing a single series, provide a list of strings to represent the tooltip label of each point. If your chart includes multiple series, supply a list of lists, where each inner list specifies the tooltips for the points on each corresponding series'
        }, 'border_style': {'type': ['list', 'list[list]'], 'description':
        'For charts containing a single series, provide a list of strings to represent the border style of each point. If your chart includes multiple series, supply a list of lists, where each inner list specifies the border styles for the points on each corresponding series. Please make sure to only use border styles from the following list: <span style="font-weight:bold">"solid", "dotted", "dashed", "largeDashed", "sparseDotted"</span>.'
        }, 'chart_type': {'type': ['str'], 'description':
        'This is the type of the chart. You can find the available ID by running the get_plot_types()'
        }, 'gauge': {'type': ['dict'], 'description':
        "This dictionary must contains 3 keys: <span style='font-weight:bold'>'value'</span> that corresponds to the value of the gauge, <span style='font-weight:bold'>'min'</span> and <span style='font-weight:bold'>'max'</span> for the minimum and maximum value the gauge can take"
        }, 'interactive': {'type': ['boolean'], 'description':
        'If set to false, only the final plot will be displayed, without the option for interactive editing. Default value is true.'
        }, 'dataframe': {'type': [], 'description': ''}, 'dates': {'type':
        ['list', 'DataFrame Index'], 'description':
        'list or DataFrame index representing the dates of your time series'
        }, 'returns': {'type': ['list', 'pd.DataFrame', 'pd.Series'],
        'description':
        'list, DataFrame, or Series representing the (portfolio) returns of your time series'
        }, 'returns_bmk': {'type': ['list', 'pd.DataFrame', 'pd.Series'],
        'description':
        'list, DataFrame, or Series representing the (benchmark) returns of your time series'
        }, 'title': {'type': ['str'], 'description': 'Title of your plot'},
        'title_css': {'type': ['dict'], 'description':
        'Apply css to your title. Put all your css attributes into a dictionary. For instance: {"text-align": "center", "color": "red"} etc...'
        }, 'options': {'type': ['dict'], 'description':
        'You can override every attributes of the chart with the highest granularity in this options dictionary. Please refer to the option section below to find out more about all the attributes to override'
        }, 'width': {'type': ['int', 'str'], 'description':
        'This is the width of the widget. You can either specify an integer or a string with the percentage value (width="100%" for instance)'
        }, 'height': {'type': ['int', 'str'], 'description':
        'This is the height of the widget. You can either specify an integer or a string with the percentage value (height="100%" for instance)'
        }, 'gauge_zones': {'type': ['list'], 'description':
        'Separate the background sectors or zones to have static colors'},
        'gauge_zones_labels': {'type': ['list'], 'description':
        'Set labels for each zones'}, 'gauge_zones_height': {'type': [
        'list'], 'description':
        'Height parameter may be passed in to increase the size for each zone'}
        }
    vectorized_optional = {'datalabels': argument_descriptions_mapper[
        'datalabels'], 'border': argument_descriptions_mapper['border'],
        'background': argument_descriptions_mapper['background'],
        'tooltips_title': argument_descriptions_mapper['tooltips_title'],
        'tooltips_label': argument_descriptions_mapper['tooltips_label'],
        'border_style': argument_descriptions_mapper['border_style']}
    dimension_optional = {'width': argument_descriptions_mapper['width'],
        'height': argument_descriptions_mapper['height']}
    title_optional = {'title': argument_descriptions_mapper['title'],
        'title_css': argument_descriptions_mapper['title_css']}
    dataframe_dict = {'signature':
        "def plot(dataframe:list, chart_type='dataframe', title:str=None, title_css:dict=None, options:dict=None, width='60%', height=750)"
        , 'description': '', 'mandatory_args': {'dataframe':
        argument_descriptions_mapper['dataframe']}, 'optional_args': {**
        title_optional, **{'options': argument_descriptions_mapper[
        'options']}, **dimension_optional}}
    quantstats_dict = {'signature':
        "def plot(dates:list, returns:list, chart_type='quantstats', returns_bmk:list=None, title:str=None, title_css:dict=None, options:dict=None, width='60%', height=750)"
        , 'description': '', 'mandatory_args': {'dates':
        argument_descriptions_mapper['dates'], 'returns':
        argument_descriptions_mapper['returns']}, 'optional_args': {**{
        'returns_bmk': argument_descriptions_mapper['returns_bmk'],
        'options': argument_descriptions_mapper['options']}, **
        title_optional, **dimension_optional}}
    notebook_dict = {'signature':
        "def plot(chart_type='notebook', title:str=None, title_css:dict=None, options:dict=None, width='60%', height=750)"
        , 'description': '', 'mandatory_args': {'dataframe':
        argument_descriptions_mapper['dataframe']}, 'optional_args': {**
        title_optional, **dimension_optional}}
    dynamic_rescale_dict = {'signature':
        "def plot(chart_type='dynamicRescale', title:str=None, title_css:dict=None, options:dict=None, width='60%', height=750)"
        , 'description': '', 'mandatory_args': {'x':
        argument_descriptions_mapper['x'], 'y':
        argument_descriptions_mapper['y']}, 'optional_args': {**
        title_optional, **dimension_optional}}
    regression_dict = {'signature':
        "def plot(chart_type='regression', title:str=None, title_css:dict=None, options:dict=None, width='60%', height=750)"
        , 'description': '', 'mandatory_args': {'x':
        argument_descriptions_mapper['x'], 'y':
        argument_descriptions_mapper['y']}, 'optional_args': {**
        title_optional, **dimension_optional}}
    calendar_dict = {'signature':
        "def plot(chart_type='calendar', title:str=None, title_css:dict=None, options:dict=None, width='60%', height=750)"
        , 'description': '', 'mandatory_args': {'x':
        argument_descriptions_mapper['x'], 'y':
        argument_descriptions_mapper['y']}, 'optional_args': {**
        title_optional, **dimension_optional}}
    wordcloud_dict = {'signature':
        "def plot(chart_type='wordcloud', title:str=None, title_css:dict=None, options:dict=None, width='60%', height=750)"
        , 'description': '', 'mandatory_args': {'x':
        argument_descriptions_mapper['x'], 'y':
        argument_descriptions_mapper['y']}, 'optional_args': {**
        title_optional, **dimension_optional}}
    summary_statistics_dict = {'signature':
        "def plot(y:list, chart_type='summary_statistics', title:str=None, title_css:dict=None, options:dict=None, width='60%', height=750)"
        , 'description': '', 'mandatory_args': {'y':
        argument_descriptions_mapper['y']}, 'optional_args': {**
        title_optional, **{'options': argument_descriptions_mapper[
        'options']}, **dimension_optional}}

    def get_chart_js_input(chart_type='line'):
        """
        
        """
        if chart_type in ['scatter', 'bubble']:
            inputs_dict = {'signature':
                f"""def plot(x:list, y:list, legend:list=None, date_format:str=None, labels:list=None, datalabels:list=None, 
        border:list=None, background:list=None, tooltips_title:list=None, tooltips_label:list=None, 
        border_style:list=None, chart_type='{chart_type}', interactive=True, title:str=None, title_css:dict=None,
        options:dict=None, width='60%', height=750)"""
                , 'description': '', 'mandatory_args': {'x':
                argument_descriptions_mapper['x'], 'y':
                argument_descriptions_mapper['y']}, 'optional_args': {**
                title_optional, **{'date_format':
                argument_descriptions_mapper['date_format'], 'interactive':
                argument_descriptions_mapper['interactive'], 'options':
                argument_descriptions_mapper['options'], 'legend':
                argument_descriptions_mapper['legend'], 'labels':
                argument_descriptions_mapper['labels']}, **
                vectorized_optional, **dimension_optional}}
        elif chart_type in ['bar', 'area']:
            inputs_dict = {'signature':
                f"""def plot(x:list, y:list, stacked:bool=False, legend:list=None, date_format:str=None, datalabels:list=None, 
        border:list=None, background:list=None, tooltips_title:list=None, tooltips_label:list=None, 
        border_style:list=None, chart_type='{chart_type}', interactive=True, title:str=None, title_css:dict=None,
        options:dict=None, width='60%', height=750)"""
                , 'description': '', 'mandatory_args': {'x':
                argument_descriptions_mapper['x'], 'y':
                argument_descriptions_mapper['y']}, 'optional_args': {**
                title_optional, **{'date_format':
                argument_descriptions_mapper['date_format'], 'stacked':
                argument_descriptions_mapper['stacked'], 'interactive':
                argument_descriptions_mapper['interactive'], 'options':
                argument_descriptions_mapper['options'], 'legend':
                argument_descriptions_mapper['legend']}, **
                vectorized_optional, **dimension_optional}}
        else:
            inputs_dict = {'signature':
                f"""def plot(x:list, y:list, legend:list=None, date_format:str=None, datalabels:list=None, 
        border:list=None, background:list=None, tooltips_title:list=None, tooltips_label:list=None, 
        border_style:list=None, chart_type='{chart_type}', interactive=True, title:str=None, title_css:dict=None,
        options:dict=None, width='60%', height=750)"""
                , 'description': '', 'mandatory_args': {'x':
                argument_descriptions_mapper['x'], 'y':
                argument_descriptions_mapper['y']}, 'optional_args': {**
                title_optional, **{'date_format':
                argument_descriptions_mapper['date_format'], 'interactive':
                argument_descriptions_mapper['interactive'], 'options':
                argument_descriptions_mapper['options'], 'legend':
                argument_descriptions_mapper['legend']}, **
                vectorized_optional, **dimension_optional}}
        return inputs_dict

    def get_tv_input(chart_type='realTimeStock'):
        return {'signature':
            f"def plot(chart_type='{chart_type}', title:str=None, title_css:dict=None, options:dict=None, width='60%', height=750)"
            , 'description': '', 'mandatory_args': {}, 'optional_args': {**
            title_optional, **{'options': argument_descriptions_mapper[
            'options'], **dimension_optional}}}

    def get_lightweight_input(chart_type='ts_line'):
        if chart_type == 'ts_shaded':
            inputs_dict = {'signature':
                f"""def plot(x:list, y:list, shaded_background:list, legend:list=None, chart_type='{chart_type}', title:str=None, title_css:dict=None, 
    options:dict=None, width='60%', height=750)"""
                , 'description': '', 'mandatory_args': {'x':
                argument_descriptions_mapper['x'], 'y':
                argument_descriptions_mapper['y'], 'shaded_background':
                argument_descriptions_mapper['shaded_background']},
                'optional_args': {**{'options':
                argument_descriptions_mapper['options'], 'legend':
                argument_descriptions_mapper['legend']}, **dimension_optional}}
        elif chart_type == 'candlestick':
            inputs_dict = {'signature':
                f"""def plot(x:list, ohlcv:list, legend:list=None, chart_type='{chart_type}', title:str=None, title_css:dict=None,
    options:dict=None, width='60%', height=750)"""
                , 'description': '', 'mandatory_args': {'x':
                argument_descriptions_mapper['x'], 'ohlcv':
                argument_descriptions_mapper['y']}, 'optional_args': {**
                title_optional, **{'options': argument_descriptions_mapper[
                'options'], 'legend': argument_descriptions_mapper['legend'
                ]}, **dimension_optional}}
        else:
            inputs_dict = {'signature':
                f"""def plot(x:list, y:list, legend:list=None, chart_type='{chart_type}', title:str=None, title_css:dict=None,
    options:dict=None, width='60%', height=750)"""
                , 'description': '', 'mandatory_args': {'x':
                argument_descriptions_mapper['x'], 'y':
                argument_descriptions_mapper['y']}, 'optional_args': {**
                title_optional, **{'options': argument_descriptions_mapper[
                'options'], 'legend': argument_descriptions_mapper['legend'
                ]}, **dimension_optional}}
        return inputs_dict

    def get_gauge_input(chart_type='gauge1'):
        signature = ("def plot(chart_type='" + str(chart_type) +
            "', gauge={'value':10, 'min':1, 'max':100}, title:str=None, title_css:dict=None, options:dict=None, width='60%', height=750)"
            )
        optional_args = {**{'options': argument_descriptions_mapper[
            'options'], **dimension_optional}}
        if chart_type == 'gauge3':
            optional_args = {**{'gauge_zones': argument_descriptions_mapper
                ['gauge_zones'], 'gauge_zones_labels':
                argument_descriptions_mapper['gauge_zones_labels']}, **
                title_optional, **{'options': argument_descriptions_mapper[
                'options']}, **dimension_optional}
            signature = ("def plot(chart_type='" + str(chart_type) +
                "', gauge={'value':10, 'min':1, 'max':100}, gauge_zones:list=None, gauge_zones_labels:list=None, title:str=None, title_css:dict=None, options:dict=None, width='60%', height=750)"
                )
        elif chart_type == 'gauge4':
            optional_args = {'gauge_zones': argument_descriptions_mapper[
                'gauge_zones'], 'gauge_zones_labels':
                argument_descriptions_mapper['gauge_zones_labels'],
                'gauge_zones_height': argument_descriptions_mapper[
                'gauge_zones_height'], **title_optional, **{'options':
                argument_descriptions_mapper['options']}, **dimension_optional}
            signature = ("def plot(chart_type='" + str(chart_type) +
                "', gauge={'value':10, 'min':1, 'max':100}, gauge_zones:list=None, gauge_zones_labels:list=None, gauge_zones_height:list=None, title:str=None, title_css:dict=None, options:dict=None, width='60%', height=750)"
                )
        return {'signature': signature, 'description': '', 'mandatory_args':
            {'gauge': argument_descriptions_mapper['gauge']},
            'optional_args': {**title_optional, **optional_args}}

    def get_df_relationships_default(chart_type):
        return {'signature':
            f"def plot(chart_type='{chart_type}', title:str=None, title_css:dict=None, options:dict=None, width='60%', height=750)"
            , 'description': '', 'mandatory_args': {'x':
            argument_descriptions_mapper['x'], 'y':
            argument_descriptions_mapper['y']}, 'optional_args': {**
            title_optional, **dimension_optional}}

    def get_df_tsa_default(chart_type):
        return {'signature':
            f"def plot(chart_type='{chart_type}', title:str=None, title_css:dict=None, options:dict=None, width='60%', height=750)"
            , 'description': '', 'mandatory_args': {'x':
            argument_descriptions_mapper['x'], 'y':
            argument_descriptions_mapper['y']}, 'optional_args': {**
            title_optional, **dimension_optional}}
    inputs_options = {'line': {'input': get_chart_js_input('line'),
        'options': qube_74eb19d84b.sparta_311059c527(), 'examples':
        qube_431bf62423.sparta_d684eedcd4()}, 'bar': {'input':
        get_chart_js_input('bar'), 'options': qube_74eb19d84b.sparta_311059c527(), 'examples': qube_431bf62423.sparta_4416e50c74()},
        'area': {'input': get_chart_js_input('area'), 'options':
        qube_74eb19d84b.sparta_311059c527(), 'examples': qube_431bf62423.sparta_97d39de5eb()}, 'scatter': {'input': get_chart_js_input(
        'scatter'), 'options': qube_74eb19d84b.sparta_311059c527(),
        'examples': qube_431bf62423.sparta_3cb4dc19ae()}, 'pie': {
        'input': get_chart_js_input('pie'), 'options': qube_74eb19d84b.sparta_311059c527(), 'examples': qube_431bf62423.sparta_0af620b0b5()},
        'donut': {'input': get_chart_js_input('donut'), 'options':
        qube_74eb19d84b.sparta_311059c527(), 'examples': qube_431bf62423.sparta_fe076f83cd()}, 'radar': {'input': get_chart_js_input(
        'radar'), 'options': qube_74eb19d84b.sparta_311059c527(), 'examples':
        qube_431bf62423.sparta_99a03c8631()}, 'bubble': {'input':
        get_chart_js_input('bubble'), 'options': qube_74eb19d84b.sparta_311059c527(), 'examples': qube_431bf62423.sparta_4790244e94
        ()}, 'barH': {'input': get_chart_js_input('barH'), 'options':
        qube_74eb19d84b.sparta_311059c527(), 'examples': qube_431bf62423.sparta_575d1bf1e3()}, 'polar': {'input':
        get_chart_js_input('polar'), 'options': qube_74eb19d84b.sparta_311059c527(), 'examples': qube_431bf62423.sparta_8dedd6d43e(
        )}, 'mixed': {'input': get_chart_js_input('mixed'), 'options':
        qube_74eb19d84b.sparta_311059c527(), 'examples': qube_431bf62423.sparta_0a6e751493()}, 'matrix': {'input': get_chart_js_input(
        'matrix'), 'options': qube_74eb19d84b.sparta_311059c527(),
        'examples': qube_431bf62423.sparta_0bb9080a8c()}, 'timescale': {
        'input': get_chart_js_input('timescale'), 'options':
        qube_74eb19d84b.sparta_311059c527(), 'examples': qube_431bf62423.sparta_4416e50c74()}, 'histogram': {'input': get_chart_js_input(
        'histogram'), 'options': qube_74eb19d84b.sparta_311059c527(),
        'examples': qube_431bf62423.sparta_a991d02313()},
        'realTimeStock': {'input': get_tv_input('realTimeStock'), 'options':
        qube_e7e0ebc552.sparta_54cd5a8076(), 'examples':
        qube_4cb927777e.sparta_47cd949b65()}, 'stockHeatmap': {
        'input': get_tv_input('stockHeatmap'), 'options': qube_e7e0ebc552.sparta_eb632afce8(), 'examples': qube_4cb927777e.sparta_351858dd9b()}, 'etfHeatmap': {'input': get_tv_input(
        'etfHeatmap'), 'options': qube_e7e0ebc552.sparta_15d0fee56c(),
        'examples': qube_4cb927777e.sparta_3e14f3a8ed()},
        'economicCalendar': {'input': get_tv_input('economicCalendar'),
        'options': qube_e7e0ebc552.sparta_6dec8b0447(), 'examples':
        qube_4cb927777e.sparta_475f1c248d()}, 'cryptoTable': {
        'input': get_tv_input('cryptoTable'), 'options': qube_e7e0ebc552.sparta_66c7f01130(), 'examples': qube_4cb927777e.sparta_1c2159329a()}, 'cryptoHeatmap': {'input':
        get_tv_input('cryptoHeatmap'), 'options': qube_e7e0ebc552.sparta_4646f63fe8(), 'examples': qube_4cb927777e.sparta_c7c1c865ee()}, 'forex': {'input': get_tv_input(
        'forex'), 'options': qube_e7e0ebc552.sparta_cc53e23527(), 'examples':
        qube_4cb927777e.sparta_b423d0f213()}, 'forexHeatmap': {'input':
        get_tv_input('forexHeatmap'), 'options': qube_e7e0ebc552.sparta_825f8dfd4f(), 'examples': qube_4cb927777e.sparta_b423d0f213
        ('forexHeatmap')}, 'marketData': {'input': get_tv_input(
        'marketData'), 'options': qube_e7e0ebc552.sparta_4ccd67c49d(),
        'examples': qube_4cb927777e.sparta_03e465a604()},
        'stockMarket': {'input': get_tv_input('stockMarket'), 'options':
        qube_e7e0ebc552.sparta_0a9d52993f(), 'examples': qube_4cb927777e.sparta_47cd949b65()}, 'screener': {'input': get_tv_input
        ('screener'), 'options': qube_e7e0ebc552.sparta_468d6feb55(), 'examples':
        qube_4cb927777e.sparta_c6d7679af2()}, 'stockAnalysis': {'input':
        get_tv_input('stockAnalysis'), 'options': qube_e7e0ebc552.sparta_e72cac2683(), 'examples': qube_4cb927777e.sparta_47cd949b65('stockAnalysis')}, 'technicalAnalysis':
        {'input': get_tv_input('technicalAnalysis'), 'options':
        qube_e7e0ebc552.sparta_beb2ab247a(), 'examples':
        qube_4cb927777e.sparta_1907cbe8ae()},
        'companyProfile': {'input': get_tv_input('companyProfile'),
        'options': qube_e7e0ebc552.sparta_32f90160e6(), 'examples':
        qube_4cb927777e.sparta_47cd949b65('companyProfile')},
        'topStories': {'input': get_tv_input('topStories'), 'options':
        qube_e7e0ebc552.sparta_e124475ca3(), 'examples': qube_4cb927777e.sparta_f53c799aa9()}, 'symbolOverview': {'input':
        get_tv_input('symbolOverview'), 'options': qube_e7e0ebc552.sparta_be825eced1(), 'examples': qube_4cb927777e.sparta_c024a5f08b()}, 'symbolMini': {'input':
        get_tv_input('symbolMini'), 'options': qube_e7e0ebc552.sparta_7c7c2897b8(), 'examples': qube_4cb927777e.sparta_47cd949b65('symbolMini')}, 'symbolInfo': {'input':
        get_tv_input('symbolInfo'), 'options': qube_e7e0ebc552.sparta_23c11b05ae(), 'examples': qube_4cb927777e.sparta_47cd949b65('symbolInfo')}, 'singleTicker': {
        'input': get_tv_input('singleTicker'), 'options': qube_e7e0ebc552.sparta_7eb747f251(), 'examples': qube_4cb927777e.sparta_47cd949b65('singleTicker')}, 'tickerTape': {
        'input': get_tv_input('tickerTape'), 'options': qube_e7e0ebc552.sparta_d1a5c91aaa(), 'examples': qube_4cb927777e.sparta_aeed8730a0()}, 'tickerWidget': {'input': get_tv_input
        ('tickerWidget'), 'options': qube_e7e0ebc552.sparta_a8b182b2d4(),
        'examples': qube_4cb927777e.sparta_fc25a95549()},
        'candlestick': {'input': get_lightweight_input('candlestick'),
        'options': None, 'examples': qube_d37c1119ad.sparta_116fd3b18b()}, 'ts_line': {'input':
        get_lightweight_input('ts_line'), 'options': None, 'examples':
        qube_d37c1119ad.sparta_c24154ab8b()}, 'ts_area': {'input':
        get_lightweight_input('ts_area'), 'options': None, 'examples':
        qube_d37c1119ad.sparta_748c014306()}, 'ts_baseline': {'input':
        get_lightweight_input('ts_baseline'), 'options': None, 'examples':
        qube_d37c1119ad.sparta_94eb42749b()}, 'ts_bar': {'input':
        get_lightweight_input('ts_bar'), 'options': None, 'examples':
        qube_d37c1119ad.sparta_b42626b7d1()}, 'ts_shaded': {'input':
        get_lightweight_input('ts_shaded'), 'options': None, 'examples':
        qube_d37c1119ad.sparta_34a63ccef1()}, 'ts_lollipop': {
        'input': get_lightweight_input('ts_lollipop'), 'options': None,
        'examples': qube_d37c1119ad.sparta_8a2659027b()}, 'performance':
        {'input': get_lightweight_input('performance'), 'options': None,
        'examples': qube_d37c1119ad.sparta_2e5899fa7c()},
        'ts_area_bands': {'input': get_lightweight_input('ts_area_bands'),
        'options': None, 'examples': qube_d37c1119ad.sparta_5e9b04ec62
        ()}, 'gauge1': {'input': get_gauge_input('gauge1'), 'options':
        qube_6f8733073a.sparta_fa375b6887(), 'examples': qube_87c11c0f45.sparta_3ee8ba535a()}, 'gauge2': {'input': get_gauge_input(
        'gauge2'), 'options': qube_6f8733073a.sparta_3d3d6eddb9(), 'examples':
        qube_87c11c0f45.sparta_9a9ef70108()}, 'gauge3': {'input':
        get_gauge_input('gauge3'), 'options': qube_6f8733073a.sparta_2d99e83392(), 'examples': qube_87c11c0f45.sparta_020fe9e217(
        )}, 'gauge4': {'input': get_gauge_input('gauge4'), 'options':
        qube_6f8733073a.sparta_b86e78fd79(), 'examples': qube_87c11c0f45.sparta_bd4f127f3a()}, 'dataframe': {'input': dataframe_dict,
        'options': None, 'examples': qube_cd259f35a4.sparta_6e9ca748ce
        ()}, 'quantstats': {'input': quantstats_dict, 'options': None,
        'examples': qube_cd259f35a4.sparta_8fc3090543()},
        'dynamicRescale': {'input': dynamic_rescale_dict, 'options': None,
        'examples': qube_a29924008c.sparta_3e51dbca25()},
        'regression': {'input': regression_dict, 'options': None,
        'examples': qube_a29924008c.sparta_c40a133100()}, 'calendar':
        {'input': calendar_dict, 'options': None, 'examples':
        qube_a29924008c.sparta_dc4d350e07()}, 'wordcloud': {'input':
        wordcloud_dict, 'options': None, 'examples': qube_a29924008c.sparta_af21dc2f32()}, 'notebook': {'input': notebook_dict,
        'options': None, 'examples': qube_cd259f35a4.sparta_7c072e147f(
        )}, 'summary_statistics': {'input': summary_statistics_dict,
        'options': None, 'examples': qube_cd259f35a4.sparta_5a9379329a()}, 'OLS': {'input':
        get_df_relationships_default('OLS'), 'options': None, 'examples':
        qube_ae17c53ef5.sparta_fdee56f972()}, 'PolynomialRegression':
        {'input': get_df_relationships_default('PolynomialRegression'),
        'options': None, 'examples': qube_ae17c53ef5.sparta_1b04be4e24()}, 'DecisionTreeRegression': {'input':
        get_df_relationships_default('DecisionTreeRegression'), 'options':
        None, 'examples': qube_ae17c53ef5.sparta_8a6afabc31()},
        'RandomForestRegression': {'input': get_df_relationships_default(
        'RandomForestRegression'), 'options': None, 'examples':
        qube_ae17c53ef5.sparta_c549f4b724()}, 'clustering': {
        'input': get_df_relationships_default('clustering'), 'options':
        None, 'examples': qube_ae17c53ef5.sparta_fc7adc9a17()},
        'correlation_network': {'input': get_df_relationships_default(
        'correlation_network'), 'options': None, 'examples':
        qube_ae17c53ef5.sparta_b501153105()}, 'pca': {
        'input': get_df_relationships_default('pca'), 'options': None,
        'examples': qube_ae17c53ef5.sparta_3b223c613b()}, 'tsne': {'input':
        get_df_relationships_default('tsne'), 'options': None, 'examples':
        qube_ae17c53ef5.sparta_fbd254f4e8()}, 'features_importance': {
        'input': get_df_relationships_default('features_importance'),
        'options': None, 'examples': qube_ae17c53ef5.sparta_738f8c25c2()}, 'mutual_information': {'input':
        get_df_relationships_default('mutual_information'), 'options': None,
        'examples': qube_ae17c53ef5.sparta_92086e3062()},
        'quantile_regression': {'input': get_df_relationships_default(
        'quantile_regression'), 'options': None, 'examples':
        qube_ae17c53ef5.sparta_68ff4f9422()},
        'rolling_regression': {'input': get_df_relationships_default(
        'rolling_regression'), 'options': None, 'examples': qube_ae17c53ef5.sparta_c3474347c6()}, 'recursive_regression': {
        'input': get_df_relationships_default('recursive_regression'),
        'options': None, 'examples': qube_ae17c53ef5.sparta_6c497ed689()}, 'stl': {'input':
        get_df_tsa_default('stl'), 'options': None, 'examples':
        qube_e42b4354f9.sparta_de735dd15e()}, 'wavelet': {'input':
        get_df_tsa_default('wavelet'), 'options': None, 'examples':
        qube_e42b4354f9.sparta_c794447c21()}, 'hmm': {'input':
        get_df_tsa_default('hmm'), 'options': None, 'examples':
        qube_e42b4354f9.sparta_d97f55274d()}, 'cusum': {'input':
        get_df_tsa_default('cusum'), 'options': None, 'examples':
        qube_e42b4354f9.sparta_8ee93dcfa7()}, 'ruptures': {'input':
        get_df_tsa_default('ruptures'), 'options': None, 'examples':
        qube_e42b4354f9.sparta_0d76ad45d1()}, 'zscore': {'input':
        get_df_tsa_default('zscore'), 'options': None, 'examples':
        qube_e42b4354f9.sparta_8e4a9ce2e9()}, 'prophet_outlier': {'input':
        get_df_tsa_default('prophet_outlier'), 'options': None, 'examples':
        qube_e42b4354f9.sparta_c64ee1a765()}, 'isolation_forest':
        {'input': get_df_tsa_default('isolation_forest'), 'options': None,
        'examples': qube_e42b4354f9.sparta_3abf31c51b()}, 'mad':
        {'input': get_df_tsa_default('mad'), 'options': None, 'examples':
        qube_e42b4354f9.sparta_c2d6078d45()}, 'sarima': {'input':
        get_df_tsa_default('sarima'), 'options': None, 'examples':
        qube_e42b4354f9.sparta_1e25ddfa3d()}, 'ets': {'input':
        get_df_tsa_default('ets'), 'options': None, 'examples':
        qube_e42b4354f9.sparta_ca3c0e3574()}, 'prophet_forecast': {'input':
        get_df_tsa_default('prophet_forecast'), 'options': None, 'examples':
        qube_e42b4354f9.sparta_4af621d021()}, 'var': {'input':
        get_df_tsa_default('var'), 'options': None, 'examples':
        qube_e42b4354f9.sparta_5c9012b7b7()}, 'adf_test': {'input':
        get_df_tsa_default('adf_test'), 'options': None, 'examples':
        qube_e42b4354f9.sparta_85ff6b86c6()}, 'kpss_test': {'input':
        get_df_tsa_default('kpss_test'), 'options': None, 'examples':
        qube_e42b4354f9.sparta_f85fc9c2aa()}, 'perron_test': {'input':
        get_df_tsa_default('perron_test'), 'options': None, 'examples':
        qube_e42b4354f9.sparta_52fbdde8e1()}, 'zivot_andrews_test':
        {'input': get_df_tsa_default('zivot_andrews_test'), 'options': None,
        'examples': qube_e42b4354f9.sparta_a74de8fade()},
        'granger_test': {'input': get_df_tsa_default('granger_test'),
        'options': None, 'examples': qube_e42b4354f9.sparta_77ff0ab15f()}, 'cointegration_test': {'input':
        get_df_tsa_default('cointegration_test'), 'options': None,
        'examples': qube_e42b4354f9.sparta_7a35511239()},
        'canonical_corr': {'input': get_df_tsa_default('canonical_corr'),
        'options': None, 'examples': qube_e42b4354f9.sparta_43f66dc10c()}}
    return inputs_options


def sparta_4b708c2570(plot_type: str='line') ->dict:
    plot_types_list = sparta_6d633ad2e5()
    try:
        plot_dict = [elem for elem in plot_types_list if elem['ID'] ==
            plot_type][0]
        plot_library = plot_dict['Library']
        plot_name = plot_dict['Name']
    except:
        plot_library = ''
        plot_name = plot_type.capitalize()
    plot_inputs_options_dict = sparta_53106fda48()[plot_type]
    plot_inputs_options_dict['plot_name'] = plot_name
    plot_inputs_options_dict['plot_library'] = plot_library
    return plot_inputs_options_dict

#END OF QUBE
