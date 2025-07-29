import os,zipfile,pytz
UTC=pytz.utc
from django.conf import settings as conf_settings
def sparta_26df5a52dc():
	B='APPDATA'
	if conf_settings.PLATFORMS_NFS:
		A='/var/nfs/notebooks/'
		if not os.path.exists(A):os.makedirs(A)
		return A
	if conf_settings.PLATFORM=='LOCAL_DESKTOP'or conf_settings.IS_LOCAL_PLATFORM:
		if conf_settings.PLATFORM_DEBUG=='DEBUG-CLIENT-2':return os.path.join(os.environ[B],'SpartaQuantNB/CLIENT2')
		return os.path.join(os.environ[B],'SpartaQuantNB')
	if conf_settings.PLATFORM=='LOCAL_CE':return'/app/notebooks/'
def sparta_afb301b82d(userId):A=sparta_26df5a52dc();B=os.path.join(A,userId);return B
def sparta_53f7afb06e(notebookProjectId,userId):A=sparta_afb301b82d(userId);B=os.path.join(A,notebookProjectId);return B
def sparta_d52af333e3(notebookProjectId,userId):A=sparta_afb301b82d(userId);B=os.path.join(A,notebookProjectId);return os.path.exists(B)
def sparta_839b140f59(notebookProjectId,userId,ipynbFileName):A=sparta_afb301b82d(userId);B=os.path.join(A,notebookProjectId);return os.path.isfile(os.path.join(B,ipynbFileName))
def sparta_855076b0cf(notebookProjectId,userId):
	C=userId;B=notebookProjectId;D=sparta_53f7afb06e(B,C);G=sparta_afb301b82d(C);A=f"{G}/zipTmp/"
	if not os.path.exists(A):os.makedirs(A)
	H=f"{A}/{B}.zip";E=zipfile.ZipFile(H,'w',zipfile.ZIP_DEFLATED);I=len(D)+1
	for(J,M,K)in os.walk(D):
		for L in K:F=os.path.join(J,L);E.write(F,F[I:])
	return E
def sparta_83b349e911(notebookProjectId,userId):B=userId;A=notebookProjectId;sparta_855076b0cf(A,B);C=f"{A}.zip";D=sparta_afb301b82d(B);E=f"{D}/zipTmp/{A}.zip";F=open(E,'rb');return{'zipName':C,'zipObj':F}