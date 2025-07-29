_A='utf-8'
import base64,hashlib
from cryptography.fernet import Fernet
def sparta_6369714303():B='widget-plot-db';A=B.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A.decode(_A)
def sparta_331d5499ac(password_to_encrypt):A=password_to_encrypt;A=A.encode(_A);C=Fernet(sparta_6369714303().encode(_A));B=C.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_201801731a(password_e):B=Fernet(sparta_6369714303().encode(_A));A=base64.b64decode(password_e);A=B.decrypt(A).decode(_A);return A