from project.sparta_8345d6a892.sparta_f0696e4f00.qube_0bbca76031 import EngineBuilder
from project.logger_config import logger


class PostgresConnector(EngineBuilder):

    def __init__(self, host, port, user, password, database):
        """
        
        """
        super().__init__(host=host, port=port, user=user, password=password,
            database=database, engine_name='postgresql')
        self.connector = self.connect_db()

    def connect_db(self):
        return self.build_postgres()

    def test_connection(self) ->bool:
        """
        Test connection
        """
        try:
            if self.connector:
                self.connector.close()
                return True
            else:
                return False
        except Exception as e:
            logger.debug(f'Error: {e}')
            return False

#END OF QUBE
