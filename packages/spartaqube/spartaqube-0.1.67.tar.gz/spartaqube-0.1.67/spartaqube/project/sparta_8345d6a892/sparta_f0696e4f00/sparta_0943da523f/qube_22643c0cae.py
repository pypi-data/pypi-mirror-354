import sys
import json
import asyncio
import websocket
import threading
import pandas as pd
from io import StringIO
from collections import deque
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_0bbca76031 import EngineBuilder
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import convert_to_dataframe, convert_dataframe_to_json
from project.logger_config import logger


class WssConnector(EngineBuilder):

    def __init__(self, socket_url, dynamic_inputs=None, py_code_processing=None
        ):
        """
        
        """
        super().__init__(host=None, port=None)
        self.ws_streamer = None
        self.stop_event = threading.Event()
        self.original_stdout = None
        self.thread_streaming = None
        self.thread_streaming_processing = None
        self.thread_streaming_print = None
        self.connector = self.build_wss(socket_url=socket_url,
            dynamic_inputs=dynamic_inputs, py_code_processing=
            py_code_processing)
        self.socket_url = socket_url
        self.dynamic_inputs = dynamic_inputs
        self.py_code_processing = py_code_processing
        self.msg_structure = None

    def test_connection(self) ->bool:
        """
        Test connection
        """
        self.error_msg_test_connection = ''
        if self.dynamic_inputs is not None:
            if len(self.dynamic_inputs) > 0:
                for input_dict in self.dynamic_inputs:
                    self.socket_url = self.socket_url.replace('{' + str(
                        input_dict['input']) + '}', input_dict['default'])
        global is_wss_valid
        is_wss_valid = False

        def on_open(ws):
            global is_wss_valid
            is_wss_valid = True
            ws.close()

        def on_close(ws, close_status_code, close_msg):
            logger.debug('Connection closed')
        ws = websocket.WebSocketApp(self.socket_url, on_open=on_open,
            on_close=on_close)
        ws.run_forever()
        return is_wss_valid

    def start_stream(self, gui_websocket, b_get_print_buffer=True):
        """
        Stream data using wss connector
        """
        self.error_msg_test_connection = ''
        if self.dynamic_inputs is not None:
            if len(self.dynamic_inputs) > 0:
                for input_dict in self.dynamic_inputs:
                    self.socket_url = self.socket_url.replace('{' + str(
                        input_dict['input']) + '}', input_dict['default'])
        exec(self.py_code_processing, globals(), locals())
        on_message_connector = locals()['on_message']
        on_open_connector = locals()['on_open']
        on_error_connector = locals()['on_error']
        on_close_connector = locals()['on_close']
        queue_connector = globals()['queue']
        queue_print = deque(maxlen=100)


        class PrintCapture:

            def __init__(self):
                self._original_stdout = sys.stdout
                self._stringio = StringIO()

            def write(self, message):
                self._original_stdout.write(message)
                self._stringio.write(message)
                queue_print.append(message)

            def flush(self):
                self._original_stdout.flush()

        def on_error_override(ws, error):
            """
            Override on_error methods in order to stop the threads and stream if an error is detected
            """
            on_error_connector(ws, error)
            self.send_error_event_and_stop(gui_websocket, str(error))
        self.ws_streamer = websocket.WebSocketApp(self.socket_url,
            on_message=on_message_connector, on_open=on_open_connector,
            on_error=on_error_override, on_close=on_close_connector)

        def thread_streaming_processing_func():
            """
            Processing message queue
            """
            while not self.stop_event.is_set():
                while queue_connector:
                    msg = queue_connector.pop()
                    msg_df = convert_to_dataframe(msg)
                    msg_json = convert_dataframe_to_json(msg_df)
                    res = {'res': 1, 'msg': msg, 'msg_json': msg_json,
                        'maxlen': queue_connector.maxlen}
                    resJson = json.dumps(res)
                    gui_websocket.send(resJson)

        def thread_streaming_print_func():
            """
            Processing print messages
            """
            while not self.stop_event.is_set():
                while queue_print:
                    msg = queue_print.pop()
                    res = {'res': 2, 'print': msg}
                    resJson = json.dumps(res)
                    gui_websocket.send(resJson)

        def thread_streaming_func():
            """
            Run the WebSocketApp
            """
            self.ws_streamer.run_forever()
        self.stop_event.clear()
        self.original_stdout = sys.stdout
        sys.stdout = PrintCapture()
        self.thread_streaming = threading.Thread(target=
            thread_streaming_func, args=())
        self.thread_streaming.start()
        self.thread_streaming_processing = threading.Thread(target=
            thread_streaming_processing_func, args=())
        self.thread_streaming_processing.start()
        self.thread_streaming_print = threading.Thread(target=
            thread_streaming_print_func, args=())
        self.thread_streaming_print.start()

    def stop_threads(self):
        """
        
        """
        sys.stdout = self.original_stdout
        self.ws_streamer.close()
        try:
            if (self.thread_streaming_processing and self.thread_streaming_processing.is_alive()):
                self.stop_event.set()
                self.thread_streaming_processing.join()
        except:
            pass
        try:
            if self.thread_streaming and self.thread_streaming.is_alive():
                self.stop_event.set()
                self.thread_streaming.join()
        except:
            pass
        try:
            if (self.thread_streaming_print and self.thread_streaming_print.is_alive()):
                self.stop_event.set()
                self.thread_streaming_print.join()
        except:
            pass

    def stop_stream(self, gui_websocket):
        """
        
        """
        logger.debug('### stop stream event ###')
        self.stop_threads()
        res = {'res': -100}
        resJson = json.dumps(res)
        gui_websocket.send(resJson)

    def send_error_event_and_stop(self, gui_websocket, error_msg):
        """
        
        """
        logger.debug(
            f'Error detected, stop stream and kill threads: {error_msg}')
        try:
            self.stop_threads()
        except:
            pass
        res = {'res': -1, 'errorMsg': str(error_msg)}
        resJson = json.dumps(res)
        gui_websocket.send(resJson)

    def get_wss_structure(self) ->pd.DataFrame:
        """
        DEPRECATED (NOT USED)
        """
        self.error_msg_test_connection = ''
        if self.dynamic_inputs is not None:
            if len(self.dynamic_inputs) > 0:
                for input_dict in self.dynamic_inputs:
                    self.socket_url = self.socket_url.replace('{' + str(
                        input_dict['input']) + '}', input_dict['default'])
        exec(self.py_code_processing, globals(), locals())
        on_message_connector = locals()['on_message']
        on_open_connector = locals()['on_open']
        on_error_connector = locals()['on_error']
        on_close_connector = locals()['on_close']
        queue_connector = globals()['queue']

        def on_error_override(ws, error):
            """
            Override on_error methods in order to stop the threads and stream if an error is detected
            """
            on_error_connector(ws, error)
        self.ws_streamer = websocket.WebSocketApp(self.socket_url,
            on_message=on_message_connector, on_open=on_open_connector,
            on_error=on_error_override, on_close=on_close_connector)

        def thread_streaming_func():
            """
            Run the WebSocketApp
            """
            self.ws_streamer.run_forever()
        self.original_stdout = sys.stdout
        self.stop_event.clear()
        self.thread_streaming = threading.Thread(target=
            thread_streaming_func, args=())
        self.thread_streaming.start()
        while not self.stop_event.is_set():
            while queue_connector:
                self.msg_structure = queue_connector.pop()
                self.stop_threads()
                break
        logger.debug(self.msg_structure)

#END OF QUBE
