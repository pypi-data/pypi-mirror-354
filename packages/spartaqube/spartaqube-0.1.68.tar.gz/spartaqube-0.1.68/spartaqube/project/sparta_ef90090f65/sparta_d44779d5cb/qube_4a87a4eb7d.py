import re
import json
import subprocess
from channels.generic.websocket import WebsocketConsumer
from project.sparta_8688631f3d.sparta_9df5aeb023 import qube_2ee3065b9a as qube_2ee3065b9a
from project.logger_config import logger


def sparta_8fd274e921(command: str) ->bool:
    """
    Check if a pip install command has the correct syntax.Args:
        command (str): The command to check.Returns:
        bool: True if the syntax is correct, False otherwise."""
    if not command.startswith('pip install'):
        return False
    pattern = (
        '^pip install( [a-zA-Z0-9_\\-\\.]+(==|>=|<=|>|<)?[a-zA-Z0-9_\\-\\.]*)+$'
        )
    return bool(re.match(pattern, command))


class PipInstallWS(WebsocketConsumer):
    """

    """
    channel_session = True
    http_user_and_session = True

    def connect(self):
        """
        
        """
        logger.debug('Connect Now')
        self.accept()
        self.json_data_dict = dict()

    def disconnect(self, close_code=None):
        """
        Release memory
        """
        logger.debug('Disconnect')
        try:
            self.close()
        except:
            pass

    def receive(self, text_data):
        """
        
        """
        if len(text_data) > 0:
            json_data = json.loads(text_data)
            pip_cmd_input = json_data['pipInstallCmd'].strip()
            env_name = json_data['env_name']
            pip_path = qube_2ee3065b9a.sparta_5e7ac7feb4(env_name)
            pip_cmd = pip_cmd_input.replace('pip', pip_path)
            if not sparta_8fd274e921(pip_cmd_input):
                res = {'res': -1, 'errorMsg': 'Invalid syntax'}
                resJson = json.dumps(res)
                self.send(text_data=resJson)
                return
            success = 0
            process = subprocess.Popen(pip_cmd, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True)
            try:
                for line in process.stdout:
                    if ('Successfully installed' in line or 
                        'Requirement already satisfied' in line):
                        success = 1
                    res = {'res': 2, 'line': line}
                    resJson = json.dumps(res)
                    self.send(text_data=resJson)
            except Exception as e:
                logger.debug(f'An error occurred: {e}')
                res = {'res': -1, 'line': line}
                resJson = json.dumps(res)
                self.send(text_data=resJson)
            process.wait()
        res = {'res': 1, 'success': success}
        resJson = json.dumps(res)
        self.send(text_data=resJson)

#END OF QUBE
