try:
    from influxdb_client import InfluxDBClient
    from influxdb_client.client.exceptions import InfluxDBError
except:
    pass
import pandas as pd
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_0bbca76031 import EngineBuilder
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import convert_to_dataframe
from project.logger_config import logger


class InfluxdbConnector(EngineBuilder):

    def __init__(self, host, port, token, organization, bucket, user=None,
        password=None):
        """
        
        """
        if host.startswith('localhost'):
            host = 'http://localhost'
        super().__init__(host=host, port=port, engine_name='influxdb')
        self.connector = self.build_influxdb(token, organization, user,
            password)
        self.bucket = bucket
        self.token = token
        self.organization = organization
        self.user = user
        self.password = password

    def test_connection(self) ->bool:
        """
        Test connection
        """
        res = False
        try:
            url = f'{self.host}:{self.port}'
            client = None
            if self.token is not None:
                if len(self.token) > 0:
                    client = InfluxDBClient(url=url, token=self.token, org=
                        self.organization)
            if client is None:
                if self.user is not None:
                    if len(self.user) > 0:
                        client = InfluxDBClient(url=url, username=self.user,
                            password=self.password, org=self.organization)
            if client is None:
                res = False
                self.error_msg_test_connection = (
                    'Either token with org or username with password must be provided.'
                    )
            else:
                try:
                    query_api = client.query_api()
                    query = (
                        f'from(bucket: "{self.bucket}") |> range(start: -1h)')
                    result = query_api.query(query)
                    res = True
                except Exception as e:
                    self.error_msg_test_connection = str(e)
        except InfluxDBError as e:
            self.error_msg_test_connection = str(e)
            logger.debug('Failed to connect to InfluxDB:', e)
        except ValueError as ve:
            self.error_msg_test_connection = str(ve)
            logger.debug(ve)
        finally:
            if client is not None:
                client.close()
        return res

    def get_available_buckets(self) ->list:
        """

        """
        try:
            client = self.connector
            buckets_api = client.buckets_api()
            buckets = buckets_api.find_buckets().buckets
            bucket_names = [bucket.name for bucket in buckets]
            return bucket_names
        except InfluxDBError as e:
            logger.debug('Failed to list buckets:', e)
            return []
        finally:
            client.close()

    def get_available_tables(self) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available tables of a database
        """
        try:
            client = self.connector
            query_api = client.query_api()
            query = (
                f'import "influxdata/influxdb/schema" schema.measurements(bucket: "{self.bucket}")'
                )
            tables = query_api.query(query, org=self.organization)
            measurements = [record.get_value() for table in tables for
                record in table.records]
            return measurements
        except InfluxDBError as e:
            logger.debug('Failed to list measurements from the bucket:', e)
            return []
        finally:
            client.close()

    def get_table_columns(self, table_name) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available columns of a table
        """
        measurement = table_name
        try:
            client = self.connector
            query_api = client.query_api()
            query = f"""
            import "influxdata/influxdb/schema"
            schema.fieldKeys(
            bucket: "{self.bucket}",
            predicate: (r) => r._measurement == "{measurement}"
            )
            """
            tables = query_api.query(query, org=self.organization)
            columns = [record.get_value() for table in tables for record in
                table.records]
            return columns
        except InfluxDBError as e:
            logger.debug('Failed to list columns from the measurement:', e)
            return []
        finally:
            client.close()

    def get_data_table(self, table_name) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        measurement = table_name
        try:
            client = self.connector
            query_api = client.query_api()
            query = f"""
            from(bucket: "{self.bucket}")
            |> range(start: 0)
            |> filter(fn: (r) => r._measurement == "{measurement}")
            """
            tables = query_api.query(query, org=self.organization)
            data = []
            for table in tables:
                for record in table.records:
                    data.append({'time': record.get_time(), 'measurement':
                        record.get_measurement(), 'field': record.get_field
                        (), 'value': record.get_value(), 'tags': record.values}
                        )
            return convert_to_dataframe(data)
        except InfluxDBError as e:
            logger.debug('Failed to query data from the measurement:', e)
            return []
        finally:
            client.close()

    def get_data_table_top(self, table_name, top_limit=100) ->pd.DataFrame:
        """
        Retrieves the top `top_limit` records from the specified measurement in InfluxDB.Parameters:
        - table_name (str): The name of the measurement (InfluxDB equivalent of a table).- top_limit (int): The number of records to return (default: 100).Returns:
        - pd.DataFrame: A DataFrame containing the retrieved records."""
        measurement = table_name
        try:
            client = self.connector
            query_api = client.query_api()
            query = f"""
            from(bucket: "{self.bucket}")
            |> range(start: -30d)  // Adjust time range if necessary
            |> filter(fn: (r) => r._measurement == "{measurement}")
            |> limit(n: {top_limit})
            """
            tables = query_api.query(query, org=self.organization)
            data = []
            for table in tables:
                for record in table.records:
                    data.append({'time': record.get_time(), 'measurement':
                        record.get_measurement(), 'field': record.get_field
                        (), 'value': record.get_value(), 'tags': record.values}
                        )
            return pd.DataFrame(data)
        except InfluxDBError as e:
            logger.debug(
                f'Failed to query data from measurement {table_name}: {e}')
            return pd.DataFrame()

    def get_data_table_query(self, sql, table_name=None) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        measurement = table_name
        client = self.connector
        query_api = client.query_api()
        sql_arr = sql.split('\n')
        sql_arr = [elem for elem in sql_arr if len(elem) > 0]
        sql = ''.join([elem for elem in sql_arr if elem[0] != '#'])
        query = f'from(bucket: "{self.bucket}") {sql}'
        tables = query_api.query(query, org=self.organization)
        data = []
        for table in tables:
            for record in table.records:
                data.append({'time': record.get_time(), 'measurement':
                    record.get_measurement(), 'field': record.get_field(),
                    'value': record.get_value(), 'tags': record.values})
        if client is not None:
            client.close()
        if len(data) > 0:
            return convert_to_dataframe(data)
        else:
            return pd.DataFrame()

#END OF QUBE
