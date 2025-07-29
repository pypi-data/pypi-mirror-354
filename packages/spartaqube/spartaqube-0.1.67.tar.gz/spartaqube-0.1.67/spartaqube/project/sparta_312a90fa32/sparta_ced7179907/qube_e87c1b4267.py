import os
from project.sparta_312a90fa32.sparta_ced7179907.qube_3c89ebaf65 import qube_3c89ebaf65
from project.sparta_312a90fa32.sparta_ced7179907.qube_6da93ea730 import qube_6da93ea730
from project.sparta_312a90fa32.sparta_ced7179907.qube_d0b1834943 import qube_d0b1834943
from project.sparta_312a90fa32.sparta_ced7179907.qube_d46a6e25da import qube_d46a6e25da
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_3c89ebaf65()
		elif A.dbType==1:A.dbCon=qube_6da93ea730()
		elif A.dbType==2:A.dbCon=qube_d0b1834943()
		elif A.dbType==4:A.dbCon=qube_d46a6e25da()
		return A.dbCon