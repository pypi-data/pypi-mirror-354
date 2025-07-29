import pandas as pd
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_0bbca76031 import EngineBuilder
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import convert_to_dataframe
from project.logger_config import logger


class RedisConnector(EngineBuilder):

    def __init__(self, host, port, user=None, password=None, db: int=0):
        """
        
        """
        super().__init__(host=host, port=port, user=user, password=password,
            engine_name='redis')
        self.db = db
        self.connector = self.connect_db()

    def connect_db(self):
        return self.build_redis(db=self.db)

    def test_connection(self) ->bool:
        """
        Test connection
        """
        try:
            if self.connector.ping():
                return True
            else:
                return False
        except Exception as e:
            self.error_msg_test_connection = str(e)
            return False

    def get_keys(self) ->list:
        """
        Get list of redis keys as list
        """
        keys = self.connector.keys('*')
        return [key.decode() for key in keys]

    def get(self, key):
        """
        Get value from key (data type is handled automatically)
        """
        data_type = self.connector.type(key).decode()
        if data_type == 'string':
            value = self.connector.get(key)
            if value is not None:
                return value.decode()
        elif data_type == 'list':
            range_values = self.connector.lrange(key, 0, -1)
            if range_values is not None:
                range_values = [this_obj.decode() for this_obj in range_values]
                return range_values
        elif data_type == 'hash':
            range_values = self.connector.hgetall(key)
            if range_values is not None:
                range_values = [this_obj.decode() for this_obj in range_values]
                return range_values
        elif data_type == 'set':
            members = self.connector.smembers(key)
            if members is not None:
                members = [this_obj.decode() for this_obj in members]
                return members
        elif data_type == 'zset':
            range_values = self.connector.zrange(key, 0, -1, withscores=True)
            if range_values is not None:
                range_values = [this_obj.decode() for this_obj in range_values]
        else:
            return None
        return None

    def get_available_tables(self) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available tables of a database
        """
        try:
            return sorted(self.get_keys())
        except Exception as e:
            logger.debug('get available tables error')
            logger.debug(e)
        return []

    def get_table_columns(self, table_name) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available columns of a table
        """
        return [table_name]

    def get_data_table(self, table_name) ->pd.DataFrame:
        """
        
        """
        res = self.get(table_name)
        res_df = convert_to_dataframe(res)
        res_df.columns = [table_name]
        return res_df

    def get_data_table_top(self, table_name, top_limit=100) ->pd.DataFrame:
        res_df = self.get_data_table(table_name)
        try:
            return res_df.head(top_limit)
        except:
            return pd.DataFrame()

#END OF QUBE
