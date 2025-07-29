_n='makemigrations'
_m='app.settings'
_l='DJANGO_SETTINGS_MODULE'
_k='python'
_j='thumbnail'
_i='previewImage'
_h='isPublic'
_g='isExpose'
_f='password'
_e='lumino_layout'
_d='developer_venv'
_c='lumino'
_b='Project not found...'
_a='You do not have the rights to access this project'
_Z='backend'
_Y='stdout'
_X='npm'
_W='luminoLayout'
_V='hasPassword'
_U='is_public_developer'
_T='has_password'
_S='is_expose_developer'
_R='is_plot_db'
_Q='static'
_P='frontend'
_O='manage.py'
_N='description'
_M='project_path'
_L='developerId'
_K='developer_obj'
_J='slug'
_I='developer_id'
_H='name'
_G='developer'
_F='projectPath'
_E=None
_D='errorMsg'
_C=False
_B='res'
_A=True
import re,os,json,stat,importlib,io,sys,subprocess,platform,base64,traceback,uuid,shutil
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from spartaqube_app.path_mapper_obf import sparta_bff35427ab
from project.models_spartaqube import Developer,DeveloperShared
from project.models import ShareRights
from project.sparta_8688631f3d.sparta_355a680bf7 import qube_1d2a59f054 as qube_1d2a59f054
from project.sparta_8688631f3d.sparta_5d2f5154f8 import qube_c71ace27e3 as qube_c71ace27e3
from project.sparta_8688631f3d.sparta_577b784581.qube_2949549c51 import Connector as Connector
from project.sparta_8688631f3d.sparta_97c9232dca import qube_de58073131 as qube_de58073131
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_8f0cad92aa import sparta_226d9606de
from project.sparta_8688631f3d.sparta_9df5aeb023 import qube_4009e9a33a as qube_4009e9a33a
from project.sparta_8688631f3d.sparta_9df5aeb023 import qube_49f539b4d6 as qube_49f539b4d6
from project.sparta_8688631f3d.sparta_5149e63dd6.qube_0a8e8bbdab import sparta_8c5bc8c8c4
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_cdd2396883 import sparta_99859b53bb,sparta_f8e322f1b3
from project.logger_config import logger
def sparta_291c67af3a():
	A=['esbuild-darwin-arm64','esbuild-darwin-x64','esbuild-linux-x64','esbuild-windows-x64.exe'];C=os.path.dirname(__file__);A=[os.path.join(C,'esbuild',A)for A in A]
	def D(file_path):
		A=file_path
		if os.name=='nt':
			try:subprocess.run(['icacls',A,'/grant','*S-1-1-0:(RX)'],check=_A);logger.debug(f"Executable permissions set for: {A} (Windows)")
			except subprocess.CalledProcessError as B:logger.debug(f"Failed to set permissions for {A} on Windows: {B}")
		else:
			try:os.chmod(A,stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH);logger.debug(f"Executable permissions set for: {A} (Unix/Linux/Mac)")
			except Exception as B:logger.debug(f"Failed to set permissions for {A} on Unix/Linux: {B}")
	for B in A:
		if os.path.exists(B):D(B)
		else:logger.debug(f"File not found: {B}")
	return{_B:1}
def sparta_09abdd9532(user_obj):
	A=qube_1d2a59f054.sparta_1c22139619(user_obj)
	if len(A)>0:B=[A.user_group for A in A]
	else:B=[]
	return B
def sparta_915b969cda(project_path):
	G='template';A=project_path
	if not os.path.exists(A):os.makedirs(A)
	D=A;H=os.path.dirname(__file__);E=os.path.join(sparta_bff35427ab()['django_app_template'],_G,G)
	for F in os.listdir(E):
		C=os.path.join(E,F);B=os.path.join(D,F)
		if os.path.isdir(C):shutil.copytree(C,B,dirs_exist_ok=_A)
		else:shutil.copy2(C,B)
	I=os.path.dirname(os.path.dirname(H));J=os.path.dirname(I);K=os.path.join(J,_Q);L=os.path.join(K,'js',_G,G,_P);B=os.path.join(D,_P);shutil.copytree(L,B,dirs_exist_ok=_A);return{_M:A}
def sparta_93b7d6dfd5(json_data,user_obj):
	F=json_data;C=user_obj;L=F.get(_R,_C);A=F[_F];A=sparta_226d9606de(A);G=Developer.objects.filter(project_path=A).all()
	if G.count()>0:
		B=G[0];H=sparta_09abdd9532(C)
		if len(H)>0:D=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=H,developer__is_delete=0,developer=B)|Q(is_delete=0,user=C,developer__is_delete=0,developer=B))
		else:D=DeveloperShared.objects.filter(is_delete=0,user=C,developer__is_delete=0,developer=B)
		I=_C
		if D.count()>0:
			M=D[0];J=M.share_rights
			if J.is_admin or J.has_write_rights:I=_A
		if not I:return{_B:-1,_D:'Chose another path. A project already exists at this location'}
	if not isinstance(A,str):return{_B:-1,_D:'Project path must be a string.'}
	try:A=os.path.abspath(A)
	except Exception as E:return{_B:-1,_D:f"Invalid project path: {str(E)}"}
	try:
		if not os.path.exists(A):os.makedirs(A)
		N=sparta_915b969cda(A);A=N[_M];K=''
		if L:B=sparta_06fbc65e99(C,A);K=B.developer_id
		return{_B:1,_M:A,_I:K}
	except Exception as E:return{_B:-1,_D:f"Failed to create folder: {str(E)}"}
def sparta_06fa80bd70(json_data,user_obj):A=json_data;A['bAddGitignore']=_A;A['bAddReadme']=_A;return qube_49f539b4d6.sparta_c717238807(A,user_obj)
def sparta_26617ebecb(json_data,user_obj):return sparta_069c710cda(json_data,user_obj)
def sparta_b0f7dbf938(json_data,user_obj):
	O='type';N='%Y-%m-%d';M='Recently used';H=json_data;G='icon';E=user_obj;C=H.get(_R,_C);I=sparta_09abdd9532(E)
	if len(I)>0:A=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=I,developer__is_delete=0,developer__is_plot_db=C,developer__is_saved_confirmed=_A)|Q(is_delete=0,user=E,developer__is_delete=0,developer__is_plot_db=C,developer__is_saved_confirmed=_A)|Q(is_delete=0,developer__is_delete=0,developer__is_expose_developer=_A,developer__is_public_developer=_A,developer__is_plot_db=C,developer__is_saved_confirmed=_A))
	else:A=DeveloperShared.objects.filter(Q(is_delete=0,user=E,developer__is_delete=0,developer__is_plot_db=C,developer__is_saved_confirmed=_A)|Q(is_delete=0,developer__is_delete=0,developer__is_expose_developer=_A,developer__is_public_developer=_A,developer__is_plot_db=C,developer__is_saved_confirmed=_A))
	if A.count()>0:
		D=H.get('orderBy',M)
		if D==M:A=A.order_by('-developer__last_date_used')
		elif D=='Date desc':A=A.order_by('-developer__last_update')
		elif D=='Date asc':A=A.order_by('developer__last_update')
		elif D=='Name desc':A=A.order_by('-developer__name')
		elif D=='Name asc':A=A.order_by('developer__name')
	J=[]
	for F in A:
		B=F.developer;P=F.share_rights;K=_E
		try:K=str(B.last_update.strftime(N))
		except:pass
		L=_E
		try:L=str(B.date_created.strftime(N))
		except Exception as R:logger.debug(R)
		J.append({_I:B.developer_id,_H:B.name,_J:B.slug,'slugApi':B.slug,_N:B.description,_S:B.is_expose_developer,_T:B.has_password,_U:B.is_public_developer,'is_owner':F.is_owner,'has_write_rights':P.has_write_rights,'last_update':K,'date_created':L,G:{O:G,G:'fa-cube'},'category':[_G],'typeChart':_G,O:_G,'typeId':B.developer_id,_F:B.project_path})
	return{_B:1,'developer_library':J}
def sparta_7d846801e4(json_data,user_obj):
	B=user_obj;E=json_data[_L];D=Developer.objects.filter(developer_id__startswith=E,is_delete=_C).all()
	if D.count()==1:
		A=D[D.count()-1];E=A.developer_id;F=sparta_09abdd9532(B)
		if len(F)>0:C=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=F,developer__is_delete=0,developer=A)|Q(is_delete=0,user=B,developer__is_delete=0,developer=A))
		else:C=DeveloperShared.objects.filter(is_delete=0,user=B,developer__is_delete=0,developer=A)
		if C.count()==0:return{_B:-1,_D:_a}
	else:return{_B:-1,_D:_b}
	C=DeveloperShared.objects.filter(is_owner=_A,developer=A,user=B)
	if C.count()>0:G=datetime.now().astimezone(UTC);A.last_date_used=G;A.save()
	return{_B:1,_G:{'basic':{_I:A.developer_id,'is_saved_confirmed':A.is_saved_confirmed,_R:A.is_plot_db,_H:A.name,_J:A.slug,_N:A.description,_S:A.is_expose_developer,_U:A.is_public_developer,_T:A.has_password,_d:A.developer_venv,_M:A.project_path},_c:{_e:A.lumino_layout}}}
def sparta_d6c09ccc07(json_data,user_obj):
	G=json_data;B=user_obj;E=G[_L]
	if not B.is_anonymous:
		F=Developer.objects.filter(developer_id__startswith=E,is_delete=_C).all()
		if F.count()==1:
			A=F[F.count()-1];E=A.developer_id;H=sparta_09abdd9532(B)
			if len(H)>0:D=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=H,developer__is_delete=0,developer=A)|Q(is_delete=0,user=B,developer__is_delete=0,developer=A)|Q(is_delete=0,developer__is_delete=0,developer__is_expose_developer=_A,developer__is_public_developer=_A))
			else:D=DeveloperShared.objects.filter(Q(is_delete=0,user=B,developer__is_delete=0,developer=A)|Q(is_delete=0,developer__is_delete=0,developer__is_expose_developer=_A,developer__is_public_developer=_A))
			if D.count()==0:return{_B:-1,_D:_a}
		else:return{_B:-1,_D:_b}
	else:
		I=G.get('modalPassword',_E);logger.debug(f"DEBUG DEVELOPER VIEW TEST >>> {I}");C=has_developer_access(E,B,password_developer=I);logger.debug('MODAL DEBUG DEBUG DEBUG developer_access_dict');logger.debug(C)
		if C[_B]!=1:return{_B:C[_B],_D:C[_D]}
		A=C[_K]
	if not B.is_anonymous:
		D=DeveloperShared.objects.filter(is_owner=_A,developer=A,user=B)
		if D.count()>0:J=datetime.now().astimezone(UTC);A.last_date_used=J;A.save()
	return{_B:1,_G:{'basic':{_I:A.developer_id,_H:A.name,_J:A.slug,_N:A.description,_S:A.is_expose_developer,_U:A.is_public_developer,_T:A.has_password,_d:A.developer_venv,_M:A.project_path},_c:{_e:A.lumino_layout}}}
def sparta_06fbc65e99(user_obj,project_path):B=project_path;A=datetime.now().astimezone(UTC);D=str(uuid.uuid4());B=sparta_226d9606de(B);C=Developer.objects.create(developer_id=D,project_path=B,date_created=A,last_update=A,last_date_used=A,spartaqube_version=sparta_8c5bc8c8c4());E=ShareRights.objects.create(is_admin=_A,has_write_rights=_A,has_reshare_rights=_A,last_update=A);DeveloperShared.objects.create(developer=C,user=user_obj,share_rights=E,is_owner=_A,date_created=A);return C
def sparta_7718c8707e(json_data,user_obj):
	I=user_obj;A=json_data;print('SAVE DEVELOPER NOW');print(A);O=A['isNew']
	if not O:return sparta_3f3312b264(A,I)
	C=A[_F];C=sparta_226d9606de(C);print('FUCK FUCK FUCK');print(C);J=Developer.objects.filter(project_path=C,is_delete=_C).all();print(J.count())
	if J.count()>0:
		A[_L]=J[0].developer_id;B=A[_J]
		if len(B)==0:B=A[_H]
		D=slugify(B);B=D;E=1
		while Developer.objects.filter(slug=B).exists():B=f"{D}-{E}";E+=1
		A[_J]=B;return sparta_3f3312b264(A,I)
	F=datetime.now().astimezone(UTC);M=str(uuid.uuid4());K=A[_V];G=_E
	if K:G=A[_f];G=qube_c71ace27e3.sparta_b4548ea0cb(G)
	P=A[_W];Q=A[_H];R=A[_N];C=A[_F];C=sparta_226d9606de(C);S=A[_g];T=A[_h];K=A[_V];U=A.get('developerVenv',_E);B=A[_J]
	if len(B)==0:B=A[_H]
	D=slugify(B);B=D;E=1
	while Developer.objects.filter(slug=B).exists():B=f"{D}-{E}";E+=1
	L=_E;H=A.get(_i,_E)
	if H is not _E:
		try:
			H=H.split(',')[1];V=base64.b64decode(H);W=os.path.dirname(__file__);C=os.path.dirname(os.path.dirname(os.path.dirname(W)));N=os.path.join(C,_Q,_j,_G);os.makedirs(N,exist_ok=_A);L=str(uuid.uuid4());X=os.path.join(N,f"{L}.png")
			with open(X,'wb')as Y:Y.write(V)
		except:pass
	Z=Developer.objects.create(developer_id=M,name=Q,slug=B,description=R,is_expose_developer=S,is_public_developer=T,has_password=K,password_e=G,lumino_layout=P,project_path=C,developer_venv=U,thumbnail_path=L,date_created=F,last_update=F,last_date_used=F,spartaqube_version=sparta_8c5bc8c8c4());a=ShareRights.objects.create(is_admin=_A,has_write_rights=_A,has_reshare_rights=_A,last_update=F);DeveloperShared.objects.create(developer=Z,user=I,share_rights=a,is_owner=_A,date_created=F);return{_B:1,_I:M}
def sparta_3f3312b264(json_data,user_obj):
	G=user_obj;B=json_data;L=datetime.now().astimezone(UTC);H=B[_L];I=Developer.objects.filter(developer_id__startswith=H,is_delete=_C).all()
	if I.count()==1:
		A=I[I.count()-1];H=A.developer_id;M=sparta_09abdd9532(G)
		if len(M)>0:J=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=M,developer__is_delete=0,developer=A)|Q(is_delete=0,user=G,developer__is_delete=0,developer=A))
		else:J=DeveloperShared.objects.filter(is_delete=0,user=G,developer__is_delete=0,developer=A)
		N=_C
		if J.count()>0:
			T=J[0];O=T.share_rights
			if O.is_admin or O.has_write_rights:N=_A
		if N:
			K=B[_W];U=B[_H];V=B[_N];W=B[_g];X=B[_h];Y=B[_V];C=B[_J]
			if A.slug!=C:
				if len(C)==0:C=B[_H]
				P=slugify(C);C=P;R=1
				while Developer.objects.filter(slug=C).exists():C=f"{P}-{R}";R+=1
			D=_E;E=B.get(_i,_E)
			if E is not _E:
				E=E.split(',')[1];Z=base64.b64decode(E)
				try:
					a=os.path.dirname(__file__);b=os.path.dirname(os.path.dirname(os.path.dirname(a)));S=os.path.join(b,_Q,_j,_G);os.makedirs(S,exist_ok=_A)
					if A.thumbnail_path is _E:D=str(uuid.uuid4())
					else:D=A.thumbnail_path
					c=os.path.join(S,f"{D}.png")
					with open(c,'wb')as d:d.write(Z)
				except:pass
			logger.debug('lumino_layout_dump');logger.debug(K);logger.debug(type(K));A.name=U;A.description=V;A.slug=C;A.is_saved_confirmed=_A;A.is_expose_developer=W;A.is_public_developer=X;A.thumbnail_path=D;A.lumino_layout=K;A.last_update=L;A.last_date_used=L
			if Y:
				F=B[_f]
				if len(F)>0:F=qube_c71ace27e3.sparta_b4548ea0cb(F);A.password_e=F;A.has_password=_A
			else:A.has_password=_C
			A.save()
	return{_B:1,_I:H}
def sparta_d3889e53de(json_data,user_obj):
	E=json_data;B=user_obj;F=E[_L];C=Developer.objects.filter(developer_id__startswith=F,is_delete=_C).all()
	if C.count()==1:
		A=C[C.count()-1];F=A.developer_id;G=sparta_09abdd9532(B)
		if len(G)>0:D=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=G,developer__is_delete=0,developer=A)|Q(is_delete=0,user=B,developer__is_delete=0,developer=A))
		else:D=DeveloperShared.objects.filter(is_delete=0,user=B,developer__is_delete=0,developer=A)
		H=_C
		if D.count()>0:
			J=D[0];I=J.share_rights
			if I.is_admin or I.has_write_rights:H=_A
		if H:K=E[_W];A.lumino_layout=K;A.save()
	return{_B:1}
def sparta_817be03a8f(json_data,user_obj):
	A=user_obj;G=json_data[_L];B=Developer.objects.filter(developer_id=G,is_delete=_C).all()
	if B.count()>0:
		C=B[B.count()-1];E=sparta_09abdd9532(A)
		if len(E)>0:D=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=E,developer__is_delete=0,developer=C)|Q(is_delete=0,user=A,developer__is_delete=0,developer=C))
		else:D=DeveloperShared.objects.filter(is_delete=0,user=A,developer__is_delete=0,developer=C)
		if D.count()>0:F=D[0];F.is_delete=_A;F.save()
	return{_B:1}
def has_developer_access(developer_id,user_obj,password_developer=_E):
	J='debug';I='Invalid password';F=password_developer;E=developer_id;C=user_obj;logger.debug(_I);logger.debug(E);B=Developer.objects.filter(developer_id__startswith=E,is_delete=_C).all();D=_C
	if B.count()==1:D=_A
	else:
		K=E;B=Developer.objects.filter(slug__startswith=K,is_delete=_C).all()
		if B.count()==1:D=_A
	logger.debug('b_found');logger.debug(D)
	if D:
		A=B[B.count()-1];L=A.has_password
		if A.is_expose_developer or not A.is_saved_confirmed:
			logger.debug('is exposed')
			if A.is_public_developer:
				logger.debug('is public')
				if not L:logger.debug('no password');return{_B:1,_K:A}
				else:
					logger.debug('hass password')
					if F is _E:logger.debug('empty password provided');return{_B:2,_D:'Require password',_K:A}
					else:
						try:
							if qube_c71ace27e3.sparta_5b66dfafff(A.password_e)==F:return{_B:1,_K:A}
							else:return{_B:3,_D:I,_K:A}
						except Exception as M:return{_B:3,_D:I,_K:A}
			elif C.is_authenticated:
				G=sparta_09abdd9532(C)
				if len(G)>0:H=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=G,developer__is_delete=0,developer=A)|Q(is_delete=0,user=C,developer__is_delete=0,developer=A))
				else:H=DeveloperShared.objects.filter(is_delete=0,user=C,developer__is_delete=0,developer=A)
				if H.count()>0:return{_B:1,_K:A}
			else:return{_B:-1,J:1}
	return{_B:-1,J:2}
def sparta_4bf3c2e1bb(json_data,user_obj):A=sparta_226d9606de(json_data[_F]);return sparta_99859b53bb(A)
def sparta_9c0bd49b07(json_data,user_obj):A=sparta_226d9606de(json_data[_F]);return sparta_f8e322f1b3(A)
def sparta_c0c099e3d9():
	try:
		if platform.system()=='Windows':subprocess.run(['where',_X],capture_output=_A,check=_A)
		else:subprocess.run(['command','-v',_X],capture_output=_A,check=_A)
		return _A
	except subprocess.CalledProcessError:return _C
	except FileNotFoundError:return _C
def sparta_aed784b426():
	try:A=subprocess.run('npm -v',shell=_A,capture_output=_A,text=_A,check=_A);return A.stdout
	except:
		try:A=subprocess.run([_X,'-v'],capture_output=_A,text=_A,check=_A);return A.stdout.strip()
		except Exception as B:logger.debug(B);return
def sparta_cdd91d0d57():
	try:A=subprocess.run('node -v',shell=_A,capture_output=_A,text=_A,check=_A);return A.stdout
	except:
		try:A=subprocess.run(['node','-v'],capture_output=_A,text=_A,check=_A);return A.stdout.strip()
		except Exception as B:logger.debug(B);return
def sparta_624bfb1cd8(json_data,user_obj):
	A=sparta_226d9606de(json_data[_F]);A=os.path.join(A,_P)
	if not os.path.isdir(A):return{_B:-1,_D:f"The provided path '{A}' is not a valid directory."}
	B=os.path.join(A,'package.json');C=os.path.exists(B);D=sparta_c0c099e3d9();return{_B:1,'is_init':C,'is_npm_installed':D,'npm_version':sparta_aed784b426(),'node_version':sparta_cdd91d0d57()}
def sparta_069c710cda(json_data,user_obj):
	A=sparta_226d9606de(json_data[_F]);A=os.path.join(A,_P)
	try:C=subprocess.run('npm init -y',shell=_A,capture_output=_A,text=_A,check=_A,cwd=A);logger.debug(C.stdout);return{_B:1}
	except Exception as B:logger.debug('Error node npm init');logger.debug(B);return{_B:-1,_D:str(B)}
def sparta_d724cfce8d(json_data,user_obj):
	A=json_data;logger.debug('NODE LIS LIBS');logger.debug(A);D=sparta_226d9606de(A[_F])
	try:B=subprocess.run('npm list',shell=_A,capture_output=_A,text=_A,check=_A,cwd=D);logger.debug(B.stdout);return{_B:1,_Y:B.stdout}
	except Exception as C:logger.debug('Exception');logger.debug(C);return{_B:-1,_D:str(C)}
from django.core.management import call_command
from io import StringIO
def sparta_cc92b98ec1(project_path,python_executable=_k):
	E=python_executable;B=project_path;A=_C
	try:
		H=os.path.join(B,_O)
		if not os.path.exists(H):A=_A;return _C,f"Error: manage.py not found in {B}",A
		F=os.environ.copy();F[_l]=_m;E=sys.executable;I=[E,_O,_n,'--dry-run'];C=subprocess.run(I,cwd=B,text=_A,capture_output=_A,env=F)
		if C.returncode!=0:A=_A;return _C,f"Error: {C.stderr}",A
		G=C.stdout;J='No changes detected'not in G;return J,G,A
	except FileNotFoundError as D:A=_A;return _C,f"Error: {D}. Ensure the correct Python executable and project path.",A
	except Exception as D:A=_A;return _C,str(D),A
def sparta_c93233a885():
	A=os.environ.get('VIRTUAL_ENV')
	if A:return A
	else:return sys.prefix
def sparta_9c21ea78db():
	A=sparta_c93233a885()
	if sys.platform=='win32':B=os.path.join(A,'Scripts','pip.exe')
	else:B=os.path.join(A,'bin','pip')
	return B
def sparta_b4c5468d16(json_data,user_obj):
	A=sparta_226d9606de(json_data[_F]);A=os.path.join(A,_Z,'app');F,B,C=sparta_cc92b98ec1(A);D=1;E=''
	if C:D=-1;E=B
	return{_B:D,'has_error':C,'has_pending_migrations':F,_Y:B,_D:E}
def sparta_10401142d3(project_path,python_executable=_k):
	D=python_executable;C=project_path
	try:
		H=os.path.join(C,_O)
		if not os.path.exists(H):return _C,f"Error: manage.py not found in {C}"
		F=os.environ.copy();F[_l]=_m;D=sys.executable;G=[[D,_O,_n],[D,_O,'migrate']];logger.debug('commands');logger.debug(G);B=[]
		for I in G:
			A=subprocess.run(I,cwd=C,text=_A,capture_output=_A,env=F)
			if A.stdout is not _E:
				if len(str(A.stdout))>0:B.append(A.stdout)
			if A.stderr is not _E:
				if len(str(A.stderr))>0:B.append(f"<span style='color:red'>Stderr:\n{A.stderr}</span>")
			if A.returncode!=0:return _C,'\n'.join(B)
		return _A,'\n'.join(B)
	except FileNotFoundError as E:return _C,f"Error: {E}. Ensure the correct Python executable and project path."
	except Exception as E:return _C,str(E)
def sparta_188fdb5f72(json_data,user_obj):
	A=sparta_226d9606de(json_data[_F]);A=os.path.join(A,_Z,'app');B,C=sparta_10401142d3(A);D=1;E=''
	if not B:D=-1;E=C
	return{_B:D,'res_migration':B,_Y:C,_D:E}
def sparta_3ba7354915(json_data,user_obj):return{_B:1}
def sparta_b62a2ecf07(json_data,user_obj):return{_B:1}
def sparta_d681e862ed(json_data,user_obj):return{_B:1}
def sparta_c67b54b8fa(json_data,user_obj):logger.debug('developer_hot_reload_preview json_data');logger.debug(json_data);return{_B:1}
def sparta_3926d53a92(json_data,user_obj):
	C='baseProjectPath';A=json_data;D=sparta_226d9606de(A[C]);E=os.path.join(os.path.dirname(D),_Z);sys.path.insert(0,E);import webservices as B;importlib.reload(B);F=A['service'];G=A.copy();del A[C]
	try:return B.sparta_573f98207c(F,G,user_obj)
	except Exception as H:return{_B:-1,_D:str(H)}