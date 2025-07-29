from distutils.spawn import spawn
import json
import platform
import subprocess
import os
from project.logger_config import logger
IS_WINDOWS = False
if platform.system() == 'Windows':
    IS_WINDOWS = True
from project.models import UserProfile
from channels.generic.websocket import WebsocketConsumer


class XtermGitWS(WebsocketConsumer):
    """
        This class is called when a cell is executed in the codeEditor
    """
    channel_session = True
    http_user_and_session = True

    def connect(self):
        self.accept()
        self.user = self.scope['user']
        self.json_data_dict = dict()

    def disconnect(self, close_code):
        """
            Release memory, kill when disconnect
        """
        self.process = None
        self.master, self.slave = None, None
        try:
            self.close()
        except:
            pass

    def receive(self, text_data):
        logger.debug('RECEIVE GIT XTERMS')
        if len(text_data) > 0:
            json_data = json.loads(text_data)
            cmd = json_data['cmd']
            logger.debug('json_data')
            logger.debug(json_data)
            if not cmd.startswith('git'):
                res = {'res': 1, 'output': '', 'err': [
                    'Invalid git command...',
                    'Enter command git --help to get the list of available commands'
                    ]}
                resJson = json.dumps(res)
                self.send(text_data=resJson)
                return
            self.json_data_dict = json_data
            logger.debug('cmd > ' + str(cmd))
            project_path = json_data['projectPath']
            if IS_WINDOWS:
                command = f'"%ProgramFiles%\\Git\\bin\\bash.exe" -c "{cmd}"'
            else:
                command = cmd
            git_cmd = subprocess.Popen(command, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, shell=True, cwd=project_path)
            git_cmd_output = git_cmd.stdout.readlines()
            logger.debug('git_cmd_output')
            logger.debug(git_cmd_output)
            if len(git_cmd_output) > 0:
                git_cmd_output = [thisObj.decode() for thisObj in
                    git_cmd_output]
                logger.debug('git_cmd_output')
                logger.debug(git_cmd_output)
            git_cmd_err = git_cmd.stderr.readlines()
            logger.debug('git_cmd_err')
            logger.debug(git_cmd_err)
            if len(git_cmd_err) > 0:
                git_cmd_err = [thisObj.decode() for thisObj in git_cmd_err]
                logger.debug('git_cmd_err')
                logger.debug(git_cmd_err)
            logger.debug(json_data)
            res = {'res': 1, 'output': git_cmd_output, 'err': git_cmd_err}
            resJson = json.dumps(res)
            self.send(text_data=resJson)

#END OF QUBE
