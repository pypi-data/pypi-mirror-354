import os
import json
import base64
import hashlib
import random
from cryptography.fernet import Fernet


def sparta_1ce3c6aaa0():
    key = '__API_AUTH__'
    key = key.encode('utf-8')
    key = hashlib.md5(key).hexdigest()
    key = base64.b64encode(key.encode('utf-8'))
    return key


def sparta_572071ffb6(objectToCrypt):
    key = sparta_1ce3c6aaa0()
    f = Fernet(key)
    objectToCrypt = objectToCrypt.encode('utf-8')
    objectCrypt = f.encrypt(objectToCrypt).decode('utf-8')
    objectCrypt = base64.b64encode(objectCrypt.encode('utf-8')).decode('utf-8')
    return objectCrypt


def sparta_e084bdbf78(apiAuth):
    """
        Decrypt formula (stored in the dataQuantDB object)
    """
    key = sparta_1ce3c6aaa0()
    f = Fernet(key)
    apiAuth = base64.b64decode(apiAuth)
    return f.decrypt(apiAuth).decode('utf-8')


def sparta_3dba37ff1a(kCrypt):
    key = '__SQ_AUTH__' + str(kCrypt)
    key = key.encode('utf-8')
    key = hashlib.md5(key).hexdigest()
    key = base64.b64encode(key.encode('utf-8'))
    return key


def sparta_fc27c87e76(objectToCrypt, kCrypt):
    key = sparta_3dba37ff1a(kCrypt)
    f = Fernet(key)
    objectToCrypt = objectToCrypt.encode('utf-8')
    objectCrypt = f.encrypt(objectToCrypt).decode('utf-8')
    objectCrypt = base64.b64encode(objectCrypt.encode('utf-8')).decode('utf-8')
    return objectCrypt


def sparta_6b3af50159(objectToDecrypt, kCrypt):
    """
        Decrypt auth login
    """
    key = sparta_3dba37ff1a(kCrypt)
    f = Fernet(key)
    objectToDecrypt = base64.b64decode(objectToDecrypt)
    return f.decrypt(objectToDecrypt).decode('utf-8')


def sparta_c9b4cab4ca(kCrypt):
    key = '__SQ_EMAIL__' + str(kCrypt)
    key = key.encode('utf-8')
    key = hashlib.md5(key).hexdigest()
    key = base64.b64encode(key.encode('utf-8'))
    return key


def sparta_1103355c43(objectToCrypt, kCrypt):
    key = sparta_c9b4cab4ca(kCrypt)
    f = Fernet(key)
    objectToCrypt = objectToCrypt.encode('utf-8')
    objectCrypt = f.encrypt(objectToCrypt).decode('utf-8')
    objectCrypt = base64.b64encode(objectCrypt.encode('utf-8')).decode('utf-8')
    return objectCrypt


def sparta_67ac695bd7(objectToDecrypt, kCrypt):
    """
        Decrypt notebook cells
    """
    key = sparta_c9b4cab4ca(kCrypt)
    f = Fernet(key)
    objectToDecrypt = base64.b64decode(objectToDecrypt)
    return f.decrypt(objectToDecrypt).decode('utf-8')


def sparta_f2fe6b9f15(kCrypt):
    key = '__SQ_KEY_SSO_CRYPT__' + str(kCrypt)
    key = key.encode('utf-8')
    key = hashlib.md5(key).hexdigest()
    key = base64.b64encode(key.encode('utf-8'))
    return key


def sparta_12caae26b5(objectToCrypt, kCrypt):
    key = sparta_f2fe6b9f15(kCrypt)
    f = Fernet(key)
    objectToCrypt = objectToCrypt.encode('utf-8')
    objectCrypt = f.encrypt(objectToCrypt).decode('utf-8')
    objectCrypt = base64.b64encode(objectCrypt.encode('utf-8')).decode('utf-8')
    return objectCrypt


def sparta_4c272e99eb(objectToDecrypt, kCrypt):
    """
        Decrypt Code Exec (stored in the execMonitoring object)
    """
    key = sparta_f2fe6b9f15(kCrypt)
    f = Fernet(key)
    objectToDecrypt = base64.b64decode(objectToDecrypt)
    return f.decrypt(objectToDecrypt).decode('utf-8')


def sparta_f2ed0d4762():
    key = '__SQ_IPYNB_SQ_METADATA__'
    key = key.encode('utf-8')
    key = hashlib.md5(key).hexdigest()
    key = base64.b64encode(key.encode('utf-8'))
    return key


def sparta_3749eb6ce2(objectToCrypt):
    key = sparta_f2ed0d4762()
    f = Fernet(key)
    objectToCrypt = objectToCrypt.encode('utf-8')
    objectCrypt = f.encrypt(objectToCrypt).decode('utf-8')
    objectCrypt = base64.b64encode(objectCrypt.encode('utf-8')).decode('utf-8')
    return objectCrypt


def sparta_3b9426148a(objectToDecrypt):
    """
        Decrypt ipnyb metadata
    """
    key = sparta_f2ed0d4762()
    f = Fernet(key)
    objectToDecrypt = base64.b64decode(objectToDecrypt)
    return f.decrypt(objectToDecrypt).decode('utf-8')

#END OF QUBE
