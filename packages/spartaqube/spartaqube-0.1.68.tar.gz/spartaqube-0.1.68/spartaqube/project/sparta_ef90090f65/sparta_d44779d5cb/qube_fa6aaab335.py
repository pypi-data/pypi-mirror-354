import json
import base64
import websocket
from channels.generic.websocket import WebsocketConsumer
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.sparta_8688631f3d.sparta_9df5aeb023 import qube_49f539b4d6 as qube_49f539b4d6
from project.logger_config import logger


class GitNotebookWS(WebsocketConsumer):
    """
        WS to manage git notebook
        https://github.com/AIM-IT4/Quantitative-Finance---Technical-Analysis-to-VaR-uisng-Indian-Stocks.git
    """
    channel_session = True
    http_user_and_session = True

    def connect(self):
        self.accept()
        self.user = self.scope['user']
        self.json_data_dict = dict()

    def disconnect(self, close_code):
        try:
            self.close()
        except:
            pass

    def sendStatusMsg(self, thisMsg):
        """
            Send message back (for status for instance)
        """
        res = {'res': 3, 'statusMsg': thisMsg}
        self.send(text_data=json.dumps(res))

    def receive(self, text_data):
        logger.debug('RECEIVE GIT INSTALL')
        logger.debug('text_data > ')
        logger.debug(text_data)
        if len(text_data) > 0:
            json_data = json.loads(text_data)
            self.json_data_dict = json_data
            resDict = qube_49f539b4d6.sparta_5d6808835e(self, json_data, self.user)
            self.send(text_data=json.dumps(resDict))
            logger.debug('FINISH SOCKET')

#END OF QUBE
