import os, sys, re
from django.conf import settings
import project.sparta_8345d6a892.sparta_26ea98fb42.sparta_c50c1aa87c.qube_6507a5a0b2 as qube_6507a5a0b2
import project.sparta_8345d6a892.sparta_26ea98fb42.sparta_c50c1aa87c.qube_8b730311cb as qube_8b730311cb
import project.sparta_8345d6a892.sparta_26ea98fb42.sparta_c50c1aa87c.qube_d4e7fa08c8 as qube_d4e7fa08c8
import project.sparta_8345d6a892.sparta_26ea98fb42.sparta_c50c1aa87c.qube_1b6041f0e9 as qube_1b6041f0e9
import project.sparta_8345d6a892.sparta_26ea98fb42.sparta_f412ec7a8b.qube_bcd194f39e as qube_bcd194f39e
import project.sparta_8345d6a892.sparta_26ea98fb42.sparta_f412ec7a8b.qube_0618554ba2 as qube_0618554ba2
import project.sparta_8345d6a892.sparta_26ea98fb42.sparta_f412ec7a8b.qube_7e24490532 as qube_7e24490532
import project.sparta_8345d6a892.sparta_26ea98fb42.sparta_f412ec7a8b.qube_598ed14f90 as qube_598ed14f90
import project.sparta_8345d6a892.sparta_26ea98fb42.sparta_f412ec7a8b.qube_0590aa4cc0 as qube_0590aa4cc0
import project.sparta_8345d6a892.sparta_26ea98fb42.sparta_f412ec7a8b.qube_ceca7c54cf as qube_ceca7c54cf
import project.sparta_8345d6a892.sparta_26ea98fb42.sparta_f412ec7a8b.qube_c4e92efa7f as qube_c4e92efa7f
import project.sparta_8345d6a892.sparta_26ea98fb42.sparta_f412ec7a8b.qube_611cc9da18 as qube_611cc9da18


def sparta_078b7892c7(b_return_type_id=False) ->list:
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


def sparta_7522261757() ->dict:
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
        'options': qube_8b730311cb.sparta_2ca9c57a09(), 'examples':
        qube_bcd194f39e.sparta_7b5b9afddf()}, 'bar': {'input':
        get_chart_js_input('bar'), 'options': qube_8b730311cb.sparta_2ca9c57a09(), 'examples': qube_bcd194f39e.sparta_70fb95fcaa()},
        'area': {'input': get_chart_js_input('area'), 'options':
        qube_8b730311cb.sparta_2ca9c57a09(), 'examples': qube_bcd194f39e.sparta_639ff0fa02()}, 'scatter': {'input': get_chart_js_input(
        'scatter'), 'options': qube_8b730311cb.sparta_2ca9c57a09(),
        'examples': qube_bcd194f39e.sparta_993a5e0ef4()}, 'pie': {
        'input': get_chart_js_input('pie'), 'options': qube_8b730311cb.sparta_2ca9c57a09(), 'examples': qube_bcd194f39e.sparta_9fb06b3884()},
        'donut': {'input': get_chart_js_input('donut'), 'options':
        qube_8b730311cb.sparta_2ca9c57a09(), 'examples': qube_bcd194f39e.sparta_69a5cd50a4()}, 'radar': {'input': get_chart_js_input(
        'radar'), 'options': qube_8b730311cb.sparta_2ca9c57a09(), 'examples':
        qube_bcd194f39e.sparta_c116dde54e()}, 'bubble': {'input':
        get_chart_js_input('bubble'), 'options': qube_8b730311cb.sparta_2ca9c57a09(), 'examples': qube_bcd194f39e.sparta_f5ce73abba
        ()}, 'barH': {'input': get_chart_js_input('barH'), 'options':
        qube_8b730311cb.sparta_2ca9c57a09(), 'examples': qube_bcd194f39e.sparta_21ce89036a()}, 'polar': {'input':
        get_chart_js_input('polar'), 'options': qube_8b730311cb.sparta_2ca9c57a09(), 'examples': qube_bcd194f39e.sparta_8b841726aa(
        )}, 'mixed': {'input': get_chart_js_input('mixed'), 'options':
        qube_8b730311cb.sparta_2ca9c57a09(), 'examples': qube_bcd194f39e.sparta_f45645ef3a()}, 'matrix': {'input': get_chart_js_input(
        'matrix'), 'options': qube_8b730311cb.sparta_2ca9c57a09(),
        'examples': qube_bcd194f39e.sparta_a91c11c61d()}, 'timescale': {
        'input': get_chart_js_input('timescale'), 'options':
        qube_8b730311cb.sparta_2ca9c57a09(), 'examples': qube_bcd194f39e.sparta_70fb95fcaa()}, 'histogram': {'input': get_chart_js_input(
        'histogram'), 'options': qube_8b730311cb.sparta_2ca9c57a09(),
        'examples': qube_bcd194f39e.sparta_4e9e0c2164()},
        'realTimeStock': {'input': get_tv_input('realTimeStock'), 'options':
        qube_6507a5a0b2.sparta_6eb4a4be90(), 'examples':
        qube_598ed14f90.sparta_67a0b531e1()}, 'stockHeatmap': {
        'input': get_tv_input('stockHeatmap'), 'options': qube_6507a5a0b2.sparta_423208cfbc(), 'examples': qube_598ed14f90.sparta_550853b2e8()}, 'etfHeatmap': {'input': get_tv_input(
        'etfHeatmap'), 'options': qube_6507a5a0b2.sparta_eb9f955caf(),
        'examples': qube_598ed14f90.sparta_cd7ad21c4f()},
        'economicCalendar': {'input': get_tv_input('economicCalendar'),
        'options': qube_6507a5a0b2.sparta_759d55333e(), 'examples':
        qube_598ed14f90.sparta_10ed87370a()}, 'cryptoTable': {
        'input': get_tv_input('cryptoTable'), 'options': qube_6507a5a0b2.sparta_25b5413aa7(), 'examples': qube_598ed14f90.sparta_8fdac0c1dc()}, 'cryptoHeatmap': {'input':
        get_tv_input('cryptoHeatmap'), 'options': qube_6507a5a0b2.sparta_50854d7dae(), 'examples': qube_598ed14f90.sparta_dd0341f0a9()}, 'forex': {'input': get_tv_input(
        'forex'), 'options': qube_6507a5a0b2.sparta_4bcbb923ed(), 'examples':
        qube_598ed14f90.sparta_58af1b1947()}, 'forexHeatmap': {'input':
        get_tv_input('forexHeatmap'), 'options': qube_6507a5a0b2.sparta_2969125bde(), 'examples': qube_598ed14f90.sparta_58af1b1947
        ('forexHeatmap')}, 'marketData': {'input': get_tv_input(
        'marketData'), 'options': qube_6507a5a0b2.sparta_23033918bf(),
        'examples': qube_598ed14f90.sparta_7dc4ba2779()},
        'stockMarket': {'input': get_tv_input('stockMarket'), 'options':
        qube_6507a5a0b2.sparta_fe6a628e59(), 'examples': qube_598ed14f90.sparta_67a0b531e1()}, 'screener': {'input': get_tv_input
        ('screener'), 'options': qube_6507a5a0b2.sparta_1af34fce2e(), 'examples':
        qube_598ed14f90.sparta_9e164ad71b()}, 'stockAnalysis': {'input':
        get_tv_input('stockAnalysis'), 'options': qube_6507a5a0b2.sparta_040d217cd6(), 'examples': qube_598ed14f90.sparta_67a0b531e1('stockAnalysis')}, 'technicalAnalysis':
        {'input': get_tv_input('technicalAnalysis'), 'options':
        qube_6507a5a0b2.sparta_48623748dd(), 'examples':
        qube_598ed14f90.sparta_998b66722c()},
        'companyProfile': {'input': get_tv_input('companyProfile'),
        'options': qube_6507a5a0b2.sparta_53acb5a378(), 'examples':
        qube_598ed14f90.sparta_67a0b531e1('companyProfile')},
        'topStories': {'input': get_tv_input('topStories'), 'options':
        qube_6507a5a0b2.sparta_d6b33eb985(), 'examples': qube_598ed14f90.sparta_f0079a8752()}, 'symbolOverview': {'input':
        get_tv_input('symbolOverview'), 'options': qube_6507a5a0b2.sparta_46c9c2a282(), 'examples': qube_598ed14f90.sparta_989d2eed0c()}, 'symbolMini': {'input':
        get_tv_input('symbolMini'), 'options': qube_6507a5a0b2.sparta_c67c8abfd7(), 'examples': qube_598ed14f90.sparta_67a0b531e1('symbolMini')}, 'symbolInfo': {'input':
        get_tv_input('symbolInfo'), 'options': qube_6507a5a0b2.sparta_b8e177b2c9(), 'examples': qube_598ed14f90.sparta_67a0b531e1('symbolInfo')}, 'singleTicker': {
        'input': get_tv_input('singleTicker'), 'options': qube_6507a5a0b2.sparta_d6bfcf05ac(), 'examples': qube_598ed14f90.sparta_67a0b531e1('singleTicker')}, 'tickerTape': {
        'input': get_tv_input('tickerTape'), 'options': qube_6507a5a0b2.sparta_16b4231d71(), 'examples': qube_598ed14f90.sparta_8173709c43()}, 'tickerWidget': {'input': get_tv_input
        ('tickerWidget'), 'options': qube_6507a5a0b2.sparta_22514868fd(),
        'examples': qube_598ed14f90.sparta_d507526c72()},
        'candlestick': {'input': get_lightweight_input('candlestick'),
        'options': None, 'examples': qube_0618554ba2.sparta_8d01a79d2a()}, 'ts_line': {'input':
        get_lightweight_input('ts_line'), 'options': None, 'examples':
        qube_0618554ba2.sparta_115bbb1aa3()}, 'ts_area': {'input':
        get_lightweight_input('ts_area'), 'options': None, 'examples':
        qube_0618554ba2.sparta_f3b2e3fa5e()}, 'ts_baseline': {'input':
        get_lightweight_input('ts_baseline'), 'options': None, 'examples':
        qube_0618554ba2.sparta_f34e056ca1()}, 'ts_bar': {'input':
        get_lightweight_input('ts_bar'), 'options': None, 'examples':
        qube_0618554ba2.sparta_c70b968a15()}, 'ts_shaded': {'input':
        get_lightweight_input('ts_shaded'), 'options': None, 'examples':
        qube_0618554ba2.sparta_3ce43b300c()}, 'ts_lollipop': {
        'input': get_lightweight_input('ts_lollipop'), 'options': None,
        'examples': qube_0618554ba2.sparta_100f12cb58()}, 'performance':
        {'input': get_lightweight_input('performance'), 'options': None,
        'examples': qube_0618554ba2.sparta_3e425dc8ea()},
        'ts_area_bands': {'input': get_lightweight_input('ts_area_bands'),
        'options': None, 'examples': qube_0618554ba2.sparta_b3511a5a0f
        ()}, 'gauge1': {'input': get_gauge_input('gauge1'), 'options':
        qube_d4e7fa08c8.sparta_d68086c8d3(), 'examples': qube_7e24490532.sparta_6b530fae92()}, 'gauge2': {'input': get_gauge_input(
        'gauge2'), 'options': qube_d4e7fa08c8.sparta_b39ff680ec(), 'examples':
        qube_7e24490532.sparta_5f952688de()}, 'gauge3': {'input':
        get_gauge_input('gauge3'), 'options': qube_d4e7fa08c8.sparta_f443cee3d4(), 'examples': qube_7e24490532.sparta_01ab6256a5(
        )}, 'gauge4': {'input': get_gauge_input('gauge4'), 'options':
        qube_d4e7fa08c8.sparta_8d4e3bd2eb(), 'examples': qube_7e24490532.sparta_d1e5ffdc90()}, 'dataframe': {'input': dataframe_dict,
        'options': None, 'examples': qube_0590aa4cc0.sparta_24206cb972
        ()}, 'quantstats': {'input': quantstats_dict, 'options': None,
        'examples': qube_0590aa4cc0.sparta_84d20211aa()},
        'dynamicRescale': {'input': dynamic_rescale_dict, 'options': None,
        'examples': qube_ceca7c54cf.sparta_ac506d5c30()},
        'regression': {'input': regression_dict, 'options': None,
        'examples': qube_ceca7c54cf.sparta_507354b3c4()}, 'calendar':
        {'input': calendar_dict, 'options': None, 'examples':
        qube_ceca7c54cf.sparta_a960f90f44()}, 'wordcloud': {'input':
        wordcloud_dict, 'options': None, 'examples': qube_ceca7c54cf.sparta_d1be68d1c9()}, 'notebook': {'input': notebook_dict,
        'options': None, 'examples': qube_0590aa4cc0.sparta_15f582becd(
        )}, 'summary_statistics': {'input': summary_statistics_dict,
        'options': None, 'examples': qube_0590aa4cc0.sparta_96bf1b50bc()}, 'OLS': {'input':
        get_df_relationships_default('OLS'), 'options': None, 'examples':
        qube_c4e92efa7f.sparta_b68f8c4340()}, 'PolynomialRegression':
        {'input': get_df_relationships_default('PolynomialRegression'),
        'options': None, 'examples': qube_c4e92efa7f.sparta_80c940361d()}, 'DecisionTreeRegression': {'input':
        get_df_relationships_default('DecisionTreeRegression'), 'options':
        None, 'examples': qube_c4e92efa7f.sparta_beffc13eb7()},
        'RandomForestRegression': {'input': get_df_relationships_default(
        'RandomForestRegression'), 'options': None, 'examples':
        qube_c4e92efa7f.sparta_da7c650f5f()}, 'clustering': {
        'input': get_df_relationships_default('clustering'), 'options':
        None, 'examples': qube_c4e92efa7f.sparta_dc0d9d4c0f()},
        'correlation_network': {'input': get_df_relationships_default(
        'correlation_network'), 'options': None, 'examples':
        qube_c4e92efa7f.sparta_fb66245ab7()}, 'pca': {
        'input': get_df_relationships_default('pca'), 'options': None,
        'examples': qube_c4e92efa7f.sparta_53e1ae9289()}, 'tsne': {'input':
        get_df_relationships_default('tsne'), 'options': None, 'examples':
        qube_c4e92efa7f.sparta_ee989e275a()}, 'features_importance': {
        'input': get_df_relationships_default('features_importance'),
        'options': None, 'examples': qube_c4e92efa7f.sparta_e84e320c93()}, 'mutual_information': {'input':
        get_df_relationships_default('mutual_information'), 'options': None,
        'examples': qube_c4e92efa7f.sparta_a5401e19e6()},
        'quantile_regression': {'input': get_df_relationships_default(
        'quantile_regression'), 'options': None, 'examples':
        qube_c4e92efa7f.sparta_b25ce6c5cd()},
        'rolling_regression': {'input': get_df_relationships_default(
        'rolling_regression'), 'options': None, 'examples': qube_c4e92efa7f.sparta_8edd918964()}, 'recursive_regression': {
        'input': get_df_relationships_default('recursive_regression'),
        'options': None, 'examples': qube_c4e92efa7f.sparta_200a023ac7()}, 'stl': {'input':
        get_df_tsa_default('stl'), 'options': None, 'examples':
        qube_611cc9da18.sparta_79a0cdbdb9()}, 'wavelet': {'input':
        get_df_tsa_default('wavelet'), 'options': None, 'examples':
        qube_611cc9da18.sparta_eaabb3b149()}, 'hmm': {'input':
        get_df_tsa_default('hmm'), 'options': None, 'examples':
        qube_611cc9da18.sparta_de51544463()}, 'cusum': {'input':
        get_df_tsa_default('cusum'), 'options': None, 'examples':
        qube_611cc9da18.sparta_ff928a8de6()}, 'ruptures': {'input':
        get_df_tsa_default('ruptures'), 'options': None, 'examples':
        qube_611cc9da18.sparta_1df0907c3e()}, 'zscore': {'input':
        get_df_tsa_default('zscore'), 'options': None, 'examples':
        qube_611cc9da18.sparta_adb2e3e41a()}, 'prophet_outlier': {'input':
        get_df_tsa_default('prophet_outlier'), 'options': None, 'examples':
        qube_611cc9da18.sparta_2bbe66a1d5()}, 'isolation_forest':
        {'input': get_df_tsa_default('isolation_forest'), 'options': None,
        'examples': qube_611cc9da18.sparta_27e26ce311()}, 'mad':
        {'input': get_df_tsa_default('mad'), 'options': None, 'examples':
        qube_611cc9da18.sparta_fd7724f076()}, 'sarima': {'input':
        get_df_tsa_default('sarima'), 'options': None, 'examples':
        qube_611cc9da18.sparta_94b4ca83ee()}, 'ets': {'input':
        get_df_tsa_default('ets'), 'options': None, 'examples':
        qube_611cc9da18.sparta_046cbb1ec5()}, 'prophet_forecast': {'input':
        get_df_tsa_default('prophet_forecast'), 'options': None, 'examples':
        qube_611cc9da18.sparta_508073b5cc()}, 'var': {'input':
        get_df_tsa_default('var'), 'options': None, 'examples':
        qube_611cc9da18.sparta_59485b856c()}, 'adf_test': {'input':
        get_df_tsa_default('adf_test'), 'options': None, 'examples':
        qube_611cc9da18.sparta_b7e4cc0230()}, 'kpss_test': {'input':
        get_df_tsa_default('kpss_test'), 'options': None, 'examples':
        qube_611cc9da18.sparta_3f83c62ab5()}, 'perron_test': {'input':
        get_df_tsa_default('perron_test'), 'options': None, 'examples':
        qube_611cc9da18.sparta_c8ca6bb80c()}, 'zivot_andrews_test':
        {'input': get_df_tsa_default('zivot_andrews_test'), 'options': None,
        'examples': qube_611cc9da18.sparta_2e546ae0cf()},
        'granger_test': {'input': get_df_tsa_default('granger_test'),
        'options': None, 'examples': qube_611cc9da18.sparta_5b89691ab5()}, 'cointegration_test': {'input':
        get_df_tsa_default('cointegration_test'), 'options': None,
        'examples': qube_611cc9da18.sparta_e0dd4cb3ae()},
        'canonical_corr': {'input': get_df_tsa_default('canonical_corr'),
        'options': None, 'examples': qube_611cc9da18.sparta_f561efc9b0()}}
    return inputs_options


def sparta_6620492d0f(plot_type: str='line') ->dict:
    plot_types_list = sparta_078b7892c7()
    try:
        plot_dict = [elem for elem in plot_types_list if elem['ID'] ==
            plot_type][0]
        plot_library = plot_dict['Library']
        plot_name = plot_dict['Name']
    except:
        plot_library = ''
        plot_name = plot_type.capitalize()
    plot_inputs_options_dict = sparta_7522261757()[plot_type]
    plot_inputs_options_dict['plot_name'] = plot_name
    plot_inputs_options_dict['plot_library'] = plot_library
    return plot_inputs_options_dict

#END OF QUBE
