import base64
import hashlib
from cryptography.fernet import Fernet


def sparta_6369714303() ->str:
    """
    Get encryption key
    """
    keygen_fernet = 'db-conn'
    key = keygen_fernet.encode('utf-8')
    key = hashlib.md5(key).hexdigest()
    key = base64.b64encode(key.encode('utf-8'))
    return key.decode('utf-8')


def sparta_f70c8bace8(password_to_encrypt) ->str:
    password_to_encrypt = password_to_encrypt.encode('utf-8')
    f = Fernet(sparta_6369714303().encode('utf-8'))
    password_e = f.encrypt(password_to_encrypt).decode('utf-8')
    password_e = base64.b64encode(password_e.encode('utf-8')).decode('utf-8')
    return password_e


def sparta_3f375a99fa(password_e) ->str:
    f = Fernet(sparta_6369714303().encode('utf-8'))
    password = base64.b64decode(password_e)
    password = f.decrypt(password).decode('utf-8')
    return password


def sparta_6f6ecf58c9() ->list:
    """
    
    """
    optional_libraries = {'oracle': {'lib': 'cx_Oracle', 'pip': [
        'cx_Oracle==8.3.1']}, 'redis': {'lib': 'redis', 'pip': [
        'redis==5.0.1']}, 'couchdb': {'lib': 'couchdb', 'pip': [
        'CouchDB==1.2']}, 'aerospike': {'lib': 'aerospike', 'pip': [
        'aerospike==15.0.0']}, 'clickhouse': {'lib': 'clickhouse_connect',
        'pip': ['clickhouse-connect==0.7.16']}, 'questdb': {'lib':
        'questdb.ingress', 'pip': ['questdb==1.2.0']}, 'cassandra': {'lib':
        'cassandra.cluster', 'pip': ['cassandra-driver==3.29.0']},
        'influxdb': {'lib': 'influxdb_client', 'pip': [
        'influxdb-client==1.44.0', 'influxdb==5.3.2']}}
    all_connectors = sorted(['aerospike', 'cassandra', 'clickhouse',
        'couchdb', 'csv', 'duckdb', 'influxdb', 'json_api', 'mariadb',
        'mongo', 'mssql', 'mysql', 'oracle', 'parquet', 'postgres',
        'python', 'questdb', 'redis', 'scylladb', 'sqlite', 'wss'])
    res_engines_list = []
    for connector in all_connectors:
        if connector in optional_libraries:
            module = optional_libraries[connector]['lib']
            try:
                __import__(module)
                res_engines_list.append({'name': connector, 'is_default': 
                    False, 'is_available': True})
            except ImportError:
                res_engines_list.append({'name': connector, 'is_default': 
                    False, 'is_available': False, 'pip': optional_libraries
                    [connector]['pip']})
        else:
            res_engines_list.append({'name': connector, 'is_default': True,
                'is_available': True})
    sorted_data = sorted(res_engines_list, key=lambda x: x['name'])
    return sorted_data

#END OF QUBE
