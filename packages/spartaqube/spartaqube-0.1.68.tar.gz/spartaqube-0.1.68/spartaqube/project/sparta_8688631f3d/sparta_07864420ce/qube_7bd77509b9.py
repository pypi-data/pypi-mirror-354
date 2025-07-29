_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_4a6a97060c():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_4be4e17609(objectToCrypt):A=objectToCrypt;C=sparta_4a6a97060c();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_718364e5c8(apiAuth):A=apiAuth;B=sparta_4a6a97060c();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_9eb1121f9f(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_97ed3de84e(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_9eb1121f9f(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_3bc4ed9dd3(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_9eb1121f9f(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_e4a91e7a1e(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_5c501b8a96(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_e4a91e7a1e(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_82278b60a0(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_e4a91e7a1e(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_ece59bbfcd(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_6effbe6b3b(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_ece59bbfcd(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_fbe4ae8b32(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_ece59bbfcd(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_acfaa1af4b():A='__SQ_IPYNB_SQ_METADATA__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_408fe47d60(objectToCrypt):A=objectToCrypt;C=sparta_acfaa1af4b();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_e87241929f(objectToDecrypt):A=objectToDecrypt;B=sparta_acfaa1af4b();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)