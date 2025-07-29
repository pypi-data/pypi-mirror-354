import io, sys
import pandas as pd
import json
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_0bbca76031 import EngineBuilder
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import convert_to_dataframe
from project.logger_config import logger


class PythonConnector(EngineBuilder):

    def __init__(self, py_code_processing=None, dynamic_inputs=None):
        """
        
        """
        super().__init__(host=None, port=None)
        self.connector = self.build_python(py_code_processing=
            py_code_processing, dynamic_inputs=dynamic_inputs)
        self.py_code_processing = py_code_processing
        self.dynamic_inputs = dynamic_inputs

    def test_connection(self) ->bool:
        """
        Test connection
        """
        self.error_msg_test_connection = ''
        if self.dynamic_inputs is not None:
            if len(self.dynamic_inputs) > 0:
                for input_dict in self.dynamic_inputs:
                    globals()[input_dict['input']] = input_dict['default']
        try:
            exec(self.py_code_processing, globals(), locals())
            return True
        except Exception as e:
            self.error_msg_test_connection = str(e)
            return False

    def preview_output_connector_bowler(self, b_get_print_buffer=True) ->list:
        """
        Preview connector output
        """
        self.error_msg_test_connection = ''
        if self.dynamic_inputs is not None:
            if len(self.dynamic_inputs) > 0:
                for input_dict in self.dynamic_inputs:
                    globals()[input_dict['input']] = input_dict['default']
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

    def get_data_table(self, *args) ->pd.DataFrame:
        """
        This method loads a table (OVERRIDE THE BASE CASE)
        """
        preview_output_list = self.preview_output_connector_bowler(
            b_get_print_buffer=False)
        if preview_output_list is not None:
            resp, _ = preview_output_list
            resp = convert_to_dataframe(resp)
            return resp
        else:
            return None

    def get_data_table_top(self, *args) ->pd.DataFrame:
        """
        This method loads a table (OVERRIDE THE BASE CASE)
        """
        return self.get_data_table(args)

    def get_available_tables(self) ->list:
        """
        This method returns all the available tables of a database using sql_alchemy
        """
        return []

#END OF QUBE
