import re,os,json,stat,importlib,io,sys,subprocess,platform,base64,traceback,uuid,shutil
from pathlib import Path
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from spartaqube_app.path_mapper_obf import sparta_b6a401eb72
from project.models import ShareRights
from project.sparta_8345d6a892.sparta_87f32c6e97 import qube_93b4ab09a2 as qube_93b4ab09a2
from project.sparta_8345d6a892.sparta_26ea98fb42 import qube_9c73ae35fa as qube_9c73ae35fa
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_668c4588b1 import Connector as Connector
from project.sparta_8345d6a892.sparta_db87358646 import qube_af0123880b as qube_af0123880b
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import sparta_ad557db230
from project.sparta_8345d6a892.sparta_e4b2f842b2 import qube_9bc385c03d as qube_9bc385c03d
from project.sparta_8345d6a892.sparta_e4b2f842b2 import qube_8ecd6dcb08 as qube_8ecd6dcb08
from project.sparta_8345d6a892.sparta_707f379a9b.qube_43327fe104 import sparta_8d863c145d
from project.sparta_8345d6a892.sparta_952c41e91e.qube_7b0846f3f9 import sparta_e6a027bd1e,sparta_7d51b73540
from project.logger_config import logger
from project.sparta_8345d6a892.sparta_952c41e91e.qube_ef9e4f9eb1 import sparta_9c89cfd808
from project.sparta_8345d6a892.sparta_5d42e2bd55 import qube_3b271aaa00 as qube_3b271aaa00
def sparta_bcefba0d6f(user_obj):
	A=qube_93b4ab09a2.sparta_b0ee4cd292(user_obj)
	if len(A)>0:B=[A.user_group for A in A]
	else:B=[]
	return B
def sparta_1bf011fae2(json_data,user_obj):A=json_data;A['is_plot_db']=True;return qube_3b271aaa00.sparta_fac2977bb3(A,user_obj)
def sparta_739916762c():
	B=sparta_9c89cfd808();A=os.path.join(B,'plot_db_developer')
	def C(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=True)
	C(A);return{'res':1,'path':A}