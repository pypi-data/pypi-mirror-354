import io, sys, os
import pandas as pd
import json
import requests
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_0bbca76031 import EngineBuilder
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import convert_to_dataframe
from project.logger_config import logger


class JsonApiConnector(EngineBuilder):

    def __init__(self, json_url, dynamic_inputs=None, py_code_processing=None):
        """
        
        """
        super().__init__(host=None, port=None)
        self.connector = self.build_json_api(json_url=json_url,
            dynamic_inputs=dynamic_inputs, py_code_processing=
            py_code_processing)
        self.json_url = json_url
        self.dynamic_inputs = dynamic_inputs
        self.py_code_processing = py_code_processing

    def test_connection(self) ->bool:
        """
        Test connection
        """
        self.error_msg_test_connection = ''
        if self.dynamic_inputs is not None:
            if len(self.dynamic_inputs) > 0:
                for input_dict in self.dynamic_inputs:
                    self.json_url = self.json_url.replace('{' + str(
                        input_dict['input']) + '}', input_dict['default'])
        proxies_dict = {'http': os.environ.get('http_proxy', None), 'https':
            os.environ.get('https_proxy', None)}
        response = requests.get(self.json_url, proxies=proxies_dict)
        if response.status_code == 200:
            return True
        else:
            self.error_msg_test_connection = (
                f'Could not establish connection with status code response: {response.status_code}'
                )
            return False

    def preview_output_connector_bowler(self, b_get_print_buffer=True) ->list:
        """
        Preview connector output
        """
        self.error_msg_test_connection = ''
        if self.dynamic_inputs is not None:
            if len(self.dynamic_inputs) > 0:
                for input_dict in self.dynamic_inputs:
                    self.json_url = self.json_url.replace('{' + str(
                        input_dict['input']) + '}', input_dict['default'])
        logger.debug('JSON URL')
        logger.debug(self.json_url)
        proxies_dict = {'http': os.environ.get('http_proxy', None), 'https':
            os.environ.get('https_proxy', None)}
        response = requests.get(self.json_url, proxies=proxies_dict)
        if response.status_code == 200:
            resp = response.text
            print_buffer_content = ''
            if self.py_code_processing is not None:
                try:
                    self.py_code_processing = (self.py_code_processing +
                        '\nresp_preview = resp')
                    if b_get_print_buffer:
                        stdout_buffer = io.StringIO()
                        sys.stdout = stdout_buffer
                        exec(self.py_code_processing, globals(), locals())
                        print_buffer_content = stdout_buffer.getvalue()
                        sys.stdout = sys.__stdout__
                    else:
                        exec(self.py_code_processing, globals(), locals())
                    resp = eval('resp_preview')
                except Exception as e:
                    raise Exception(e)
            return resp, print_buffer_content
        else:
            raise Exception(
                f'Could not establish connection with status code response: {response.status_code}'
                )

    def get_json_api_dataframe(self) ->pd.DataFrame:
        """
        This method return the json_api as a pandas DataFrame
        """
        preview_output_list = self.preview_output_connector_bowler(
            b_get_print_buffer=False)
        if preview_output_list is not None:
            resp, _ = preview_output_list
            resp = convert_to_dataframe(resp)
            return resp
        return None

    def get_available_tables(self) ->list:
        """
        This method returns all the available tables of a database using sql_alchemy
        """
        return []

#END OF QUBE
