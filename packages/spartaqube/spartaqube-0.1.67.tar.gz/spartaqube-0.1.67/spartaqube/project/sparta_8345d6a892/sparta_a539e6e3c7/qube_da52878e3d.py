import json
import base64
import asyncio
import subprocess
import uuid
import os
import requests
import pandas as pd
from subprocess import PIPE
from django.db.models import Q
from datetime import datetime, timedelta
import pytz
UTC = pytz.utc
from project.models_spartaqube import DBConnector, DBConnectorUserShared, PlotDBChart, PlotDBChartShared
from project.models import ShareRights
from project.sparta_8345d6a892.sparta_87f32c6e97 import qube_93b4ab09a2 as qube_93b4ab09a2
from project.sparta_8345d6a892.sparta_f0696e4f00 import qube_3df3f7aa47
from project.sparta_8345d6a892.sparta_26ea98fb42 import qube_9c73ae35fa as qube_9c73ae35fa
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_668c4588b1 import Connector as Connector
from project.logger_config import logger


def sparta_3e4a62a2a0(json_data, user_obj) ->dict:
    """
    
    """
    logger.debug('Call autocompelte api')
    logger.debug(json_data)
    key = json_data['key']
    api_func = json_data['api_func']
    output = []
    if api_func == 'tv_symbols':
        output = sparta_dd4c73759e(key)
    return {'res': 1, 'output': output, 'key': key}


def sparta_dd4c73759e(key_symbol) ->list:
    """
    
    """
    url = (
        f'https://symbol-search.tradingview.com/local_search/v3/?text={key_symbol}&hl=1&exchange=&lang=en&search_type=undefined&domain=production&sort_by_country=US'
        )
    proxies_dict = {'http': os.environ.get('http_proxy', None), 'https': os.environ.get('https_proxy', None)}
    req_res = requests.get(url, proxies=proxies_dict)
    try:
        if int(req_res.status_code) == 200:
            res_dict = json.loads(req_res.text)
            res_symbols_list = res_dict['symbols']
            for elem_dict in res_symbols_list:
                elem_dict['symbol_id'] = elem_dict['symbol'].replace('<em>', ''
                    ).replace('</em>', '')
                elem_dict['title'] = elem_dict['symbol_id']
                elem_dict['subtitle'] = elem_dict['description'].replace('<em>'
                    , '').replace('</em>', '')
                elem_dict['value'] = elem_dict['symbol_id']
            return res_symbols_list
        return []
    except:
        return []

#END OF QUBE
