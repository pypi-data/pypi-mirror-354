import json
from channels.generic.websocket import WebsocketConsumer
from project.logger_config import logger


class StatusWS(WebsocketConsumer):
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
        res = {'res': 1}
        resJson = json.dumps(res)
        self.send(text_data=resJson)

#END OF QUBE
