try:
    import clickhouse_connect
except:
    pass
import pandas as pd
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_0bbca76031 import EngineBuilder
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import convert_to_dataframe


class ClickhouseConnector(EngineBuilder):

    def __init__(self, host, port, database, user='default', password=''):
        """
        
        """
        super().__init__(host=host, port=port, user=user, password=password,
            database=database, engine_name='clickhouse')
        self.connector = self.build_clickhouse()

    def test_connection(self) ->bool:
        """
        Test connection
        """
        res = False
        try:
            client = clickhouse_connect.get_client(host=self.host, port=
                self.port, user=self.user, password=self.password, database
                =self.database)
            query = (
                f"SELECT name FROM system.databases WHERE name = '{self.database}'"
                )
            result = client.query(query)
            if result.result_rows:
                res = True
            else:
                self.error_msg_test_connection = 'Invalid database'
        except Exception as e:
            self.error_msg_test_connection = str(e)
        finally:
            if client:
                client.close()
        return res

    def get_available_tables(self) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available tables of a database
        """
        tables = []
        try:
            client = self.connector
            query = f'SHOW TABLES FROM {self.database}'
            result = client.query(query)
            tables = [row[0] for row in result.result_rows]
        except Exception as e:
            self.error_msg_test_connection = str(e)
            tables = []
        finally:
            if client:
                client.close()
        return tables

    def get_table_columns(self, table_name) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available columns of a table
        """
        columns = []
        try:
            client = self.connector
            query = f"""
                SELECT name, type FROM system.columns 
                WHERE database = '{self.database}' AND table = '{table_name}'
                """
            result = client.query(query)
            columns = [row[1] for row in result.result_rows]
        except Exception as e:
            self.error_msg_test_connection = str(e)
            columns = []
        finally:
            if client:
                client.close()
        return columns

    def get_data_table(self, table_name) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        try:
            client = self.connector
            query = f'SELECT * FROM {table_name}'
            result = client.query(query)
            columns = result.result_columns
            result = client.query(query)
            columns = result.column_names
            rows = result.result_rows
            res_df = convert_to_dataframe(pd.DataFrame(rows, columns=columns))
            if client:
                client.close()
            return res_df
        except Exception as e:
            if client:
                client.close()
            raise Exception(e)

    def get_data_table_top(self, table_name, top_limit=100) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        try:
            client = self.connector
            query = f'SELECT * FROM {table_name} LIMIT {top_limit}'
            result = client.query(query)
            columns = result.result_columns
            result = client.query(query)
            columns = result.column_names
            rows = result.result_rows
            res_df = convert_to_dataframe(pd.DataFrame(rows, columns=columns))
            if client:
                client.close()
            return res_df
        except Exception as e:
            if client:
                client.close()
            raise Exception(e)

    def get_data_table_query(self, sql, table_name=None) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        try:
            client = self.connector
            query = sql
            result = client.query(query)
            columns = result.result_columns
            result = client.query(query)
            columns = result.column_names
            rows = result.result_rows
            res_df = convert_to_dataframe(pd.DataFrame(rows, columns=columns))
            if client:
                client.close()
            return res_df
        except Exception as e:
            if client:
                client.close()
            raise Exception(e)

#END OF QUBE
