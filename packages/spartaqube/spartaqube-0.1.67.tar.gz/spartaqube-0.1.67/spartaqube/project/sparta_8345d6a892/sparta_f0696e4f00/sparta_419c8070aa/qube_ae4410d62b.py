try:
    import aerospike
except:
    pass
import pandas as pd
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_0bbca76031 import EngineBuilder
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import convert_to_dataframe
from project.logger_config import logger


class AerospikeConnector(EngineBuilder):

    def __init__(self, host, port, user, password, database=None):
        """
        
        """
        port = int(port)
        super().__init__(host=host, port=port, user=user, password=password,
            database=database, engine_name='aerospike')
        self.connector = self.build_aerospike()

    def test_connection(self) ->bool:
        """
        Test connection
        """
        namespace = self.database
        config = {'hosts': [(self.host, self.port)]}
        if self.user and self.password:
            if len(self.user) > 0:
                config['user'] = self.user
            if len(self.password) > 0:
                config['password'] = self.password
        try:
            client = aerospike.client(config).connect()
            namespaces = client.info_all('namespaces')
            namespaces = [elem[1].strip() for elem in namespaces.values()]
            if namespace in namespaces:
                success = True
            else:
                self.error_msg_test_connection = (
                    f"Namespace '{namespace}' does not exist.")
                success = False
        except Exception as e:
            self.error_msg_test_connection = str(e)
            success = False
        finally:
            try:
                client.close()
            except:
                pass
        return success

    def get_available_tables(self) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available tables of a database
        """
        try:
            sets = set()
            client = self.connector
            namespace = self.database
            scan = client.scan(namespace, None)

            def callback(record):
                key, metadata, bins = record
                sets.add(key[1])
            scan.foreach(callback)
            sets = list(sets)
            return sets
        except Exception as e:
            logger.debug(e)
            return []

    def get_table_columns(self, table_name) ->list:
        """
        OVERRIDE engine_builder
        This method returns all the available columns of a table
        """
        try:
            bins = set()
            client = self.connector
            set_name = table_name
            namespace = self.database
            scan = client.scan(namespace, set_name)

            def callback(record):
                _, _, record_bins = record
                for bin_name in record_bins.keys():
                    bins.add(bin_name)
            scan.foreach(callback)
            bins = list(bins)
            return bins
        except Exception as e:
            return []

    def get_data_table(self, table_name) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        client = self.connector
        namespace = self.database
        set_name = table_name
        records = []
        scan = client.scan(namespace, set_name)

        def callback(record):
            key, metadata, bins = record
            records.append(bins)
        scan.foreach(callback)
        return convert_to_dataframe(pd.DataFrame(records))

    def get_data_table_top(self, table_name, top_limit=100) ->pd.DataFrame:
        """
        Retrieves the top `top_limit` records from the specified Aerospike set.Parameters:
        - table_name (str): The name of the set (Aerospike equivalent of a table).- top_limit (int): The number of records to return (default: 100).Returns:
        - pd.DataFrame: A DataFrame containing the retrieved records."""
        try:
            client = self.connector
            namespace = self.database
            set_name = table_name
            records = []
            scan = client.scan(namespace, set_name)

            def callback(record):
                key, metadata, bins = record
                if len(records) < top_limit:
                    records.append(bins)
            scan.foreach(callback)
            return pd.DataFrame(records)
        except aerospike.exception.AerospikeError as e:
            raise Exception(f'Failed to fetch data from Aerospike: {e}')

    def get_data_table_query(self, sql, table_name=None) ->pd.DataFrame:
        """
        OVERRIDE engine_builder
        """
        exec(sql, globals(), locals())
        filters_to_apply = eval('filters')
        client = self.connector
        namespace = self.database
        set_name = table_name
        query = client.query(namespace, set_name)
        for column, value in filters_to_apply.items():
            if isinstance(value, tuple) and value[0] == 'range':
                query.where(aerospike.predicates.between(column, value[1],
                    value[2]))
            else:
                query.where(aerospike.predicates.equals(column, value))
        records = []

        def callback(record):
            key, metadata, bins = record
            records.append(bins)
            logger.debug(key)
        query.foreach(callback)
        return convert_to_dataframe(pd.DataFrame(records))

#END OF QUBE
