_Am='widget_id'
_Al='json_data'
_Ak='code_editor_notebook_cells'
_Aj='plot_library'
_Ai='has_write_rights'
_Ah='chartConfigDict'
_Ag='chartParams'
_Af='dataSourceArr'
_Ae='typeChart'
_Ad='thumbnail'
_Ac='previewImage'
_Ab='Could not retrieve the dataframe, make sure you have the appropriate rights and try again'
_Aa='is_dataframe_connector'
_AZ='previewTopMod'
_AY='is_create_connector'
_AX='Name desc'
_AW='Date desc'
_AV='shadedBackgroundArr'
_AU='radiusBubbleArr'
_AT='labelsArr'
_AS='yAxisDataArr'
_AR='xAxisDataArr'
_AQ='labels'
_AP='datasets'
_AO='date_created'
_AN='last_update'
_AM='is_static_data'
_AL='is_expose_widget'
_AK='data_preview_df'
_AJ='df_blob'
_AI='encoded_blob'
_AH='error'
_AG='success'
_AF='is_owner'
_AE='yAxisArr'
_AD='xAxisArr'
_AC='is_public_widget'
_AB='has_widget_password'
_AA='bExposeAsWidget'
_A9='plotDes'
_A8='plotName'
_A7='bStaticDataPlot'
_A6='codeEditorNotebookCells'
_A5='widgetPassword'
_A4='split'
_A3='chart_config'
_A2='chart_params'
_A1='index'
_A0='utf-8'
_z='slug'
_y='input'
_x='query_filter'
_w='trusted_connection'
_v='lib_dir'
_u='organization'
_t='token'
_s='Recently used'
_r='has_access'
_q='column'
_p='type_chart'
_o='bPublicWidget'
_n='Invalid password'
_m='data_source_list'
_l='-1'
_k='columns'
_j='bApplyFilter'
_i='You do not have the rights to access this connector'
_h='py_code_processing'
_g='redis_db'
_f='socket_url'
_e='json_url'
_d='read_only'
_c='csv_delimiter'
_b='csv_path'
_a='database_path'
_Z='library_arctic'
_Y='keyspace'
_X='oracle_service_name'
_W='driver'
_V='database'
_U='user'
_T='port'
_S='host'
_R='password'
_Q='db_engine'
_P='%Y-%m-%d'
_O='description'
_N='bWidgetPassword'
_M='table_name'
_L='plot_db_chart_obj'
_K='dispo'
_J='dynamic_inputs'
_I='connector_id'
_H='name'
_G='plot_chart_id'
_F='data'
_E='errorMsg'
_D=True
_C=False
_B=None
_A='res'
import re,os,json,math,io,sys,base64,pickle,asyncio,subprocess,traceback,tinykernel,cloudpickle,uuid,pandas as pd
from subprocess import PIPE
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime,timedelta
from pathlib import Path
import pytz
UTC=pytz.utc
from spartaqube_app.path_mapper_obf import sparta_b6a401eb72
from project.models_spartaqube import DBConnector,DBConnectorUserShared,PlotDBChart,PlotDBChartShared,PlotDBPermission,CodeEditorNotebook,NewPlotApiVariables
from project.models import ShareRights,UserProfile
from project.sparta_8345d6a892.sparta_87f32c6e97 import qube_93b4ab09a2 as qube_93b4ab09a2
from project.sparta_8345d6a892.sparta_f0696e4f00 import qube_3df3f7aa47
from project.sparta_8345d6a892.sparta_26ea98fb42 import qube_9c73ae35fa as qube_9c73ae35fa
from project.sparta_8345d6a892.sparta_950a603163 import qube_2ab426de66 as qube_2ab426de66
from project.sparta_8345d6a892.sparta_f0696e4f00.qube_668c4588b1 import Connector as Connector
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import convert_to_dataframe,convert_dataframe_to_json,sparta_ad557db230,process_dataframe_components
from project.sparta_8345d6a892.sparta_707f379a9b.qube_43327fe104 import sparta_8d863c145d
from project.logger_config import logger
INPUTS_KEYS=[_AD,_AE,_AT,_AU,'rangesAxisArr','measuresAxisArr','markersAxisArr','ohlcvArr',_AV]
def sparta_9b9e9c9338(user_obj):from project.sparta_8345d6a892.sparta_f1a366f59f.qube_137201374c import sparta_374e43cb4b as A;return A(user_obj)
def sparta_bcefba0d6f(user_obj):
	A=qube_93b4ab09a2.sparta_b0ee4cd292(user_obj)
	if len(A)>0:B=[A.user_group for A in A]
	else:B=[]
	return B
def sparta_44cf59c3f0(json_data,user_obj):
	D=user_obj;E=sparta_bcefba0d6f(D)
	if len(E)>0:B=DBConnectorUserShared.objects.filter(Q(is_delete=0,user_group__in=E,db_connector__is_delete=0)|Q(is_delete=0,user=D,db_connector__is_delete=0))
	else:B=DBConnectorUserShared.objects.filter(is_delete=0,user=D,db_connector__is_delete=0)
	F=[]
	if B.count()>0:
		C=json_data.get('orderBy',_s)
		if C==_s:B=B.order_by('-db_connector__last_date_used')
		elif C==_AW:B=B.order_by('-db_connector__last_update')
		elif C=='Date asc':B=B.order_by('db_connector__last_update')
		elif C==_AX:B=B.order_by('-db_connector__name')
		elif C=='Name asc':B=B.order_by('db_connector__name')
		elif C=='Type':B=B.order_by('db_connector__db_engine')
		for G in B:
			A=G.db_connector;H=[]
			try:H=json.loads(A.dynamic_inputs)
			except:pass
			F.append({_I:A.connector_id,_S:A.host,_T:A.port,_U:A.user,_V:A.database,_W:A.driver,_X:A.oracle_service_name,_Y:A.keyspace,_Z:A.library_arctic,_a:A.database_path,_b:A.csv_path,_c:A.csv_delimiter,_d:A.read_only,_e:A.json_url,_f:A.socket_url,_g:A.redis_db,_J:H,_h:A.py_code_processing,_Q:A.db_engine,_H:A.name,_O:A.description,_AF:G.is_owner})
	return{_A:1,'db_connectors':F}
def sparta_6f6ecf58c9():return{_A:1,'available_engines':qube_3df3f7aa47.sparta_6f6ecf58c9()}
def sparta_d87c1f97f5(json_data,user_obj):
	C=json_data[_I];A=DBConnector.objects.filter(connector_id=C,is_delete=_C).all()
	if A.count()>0:B=A[A.count()-1];D=datetime.now().astimezone(UTC);B.last_date_used=D;B.save()
	return{_A:1}
def sparta_7ce317ed2b(json_data):
	A=json_data;C='';B=Connector(db_engine=A[_Q]);B.init_with_params(host=A[_S],port=A[_T],user=A[_U],password=A[_R],database=A[_V],oracle_service_name=A[_X],csv_path=A[_b],csv_delimiter=A[_c],keyspace=A[_Y],library_arctic=A[_Z],database_path=A[_a],read_only=A[_d],json_url=A[_e],socket_url=A[_f],redis_db=A.get(_g,_B),token=A.get(_t,_B),organization=A.get(_u,_B),lib_dir=A.get(_v,_B),driver=A.get(_W,_B),trusted_connection=A.get(_w,_B),dynamic_inputs=A[_J],py_code_processing=A[_h]);D=B.test_connection()
	if not D:C=B.get_error_msg_test_connection()
	return{_A:1,'is_connector_working':D,_E:C}
def sparta_77d1631c64(json_data):
	A=json_data;B=1;C='';D='';E=_B
	try:F=Connector(db_engine=A[_Q]);F.init_with_params(host=A[_S],port=A[_T],user=A[_U],password=A[_R],database=A[_V],oracle_service_name=A[_X],csv_path=A[_b],csv_delimiter=A[_c],keyspace=A[_Y],library_arctic=A[_Z],database_path=A[_a],read_only=A[_d],json_url=A[_e],socket_url=A[_f],redis_db=A[_g],token=A.get(_t,''),organization=A.get(_u,''),lib_dir=A.get(_v,''),driver=A.get(_W,''),trusted_connection=A.get(_w,_D),dynamic_inputs=A[_J],py_code_processing=A[_h]);H,D=F.preview_output_connector_bowler();G=io.StringIO();sys.stdout=G;print(H);E=G.getvalue();sys.stdout=sys.__stdout__
	except Exception as I:C=str(I);B=-1
	return{_A:B,'preview_json':E,'print_buffer_content':D,_E:C}
def sparta_d871473883(json_data,user_obj):A=json_data;B=datetime.now().astimezone(UTC);C=str(uuid.uuid4());D=DBConnector.objects.create(connector_id=C,host=A[_S],port=A[_T],user=A[_U],password_e=qube_3df3f7aa47.sparta_f70c8bace8(A[_R]),database=A[_V],oracle_service_name=A[_X],keyspace=A[_Y],library_arctic=A[_Z],database_path=A[_a],csv_path=A[_b],csv_delimiter=A[_c],read_only=A[_d],json_url=A[_e],socket_url=A[_f],redis_db=A[_g],token=A[_t],organization=A[_u],lib_dir=A[_v],driver=A[_W],trusted_connection=A[_w],dynamic_inputs=json.dumps(A[_J]),py_code_processing=A[_h],db_engine=A[_Q],name=A[_H],description=A[_O],date_created=B,last_update=B,last_date_used=B);E=ShareRights.objects.create(is_admin=_D,has_write_rights=_D,has_reshare_rights=_D,last_update=B);DBConnectorUserShared.objects.create(db_connector=D,user=user_obj,date_created=B,share_rights=E,is_owner=_D);return{_A:1}
def sparta_c04664d9de(json_data,user_obj):
	C=user_obj;B=json_data;logger.debug('update connector');logger.debug(B);I=B[_I];D=DBConnector.objects.filter(connector_id=I,is_delete=_C).all()
	if D.count()>0:
		A=D[D.count()-1];F=sparta_bcefba0d6f(C)
		if len(F)>0:E=DBConnectorUserShared.objects.filter(Q(is_delete=0,user_group__in=F,db_connector__is_delete=0,db_connector=A)|Q(is_delete=0,user=C,db_connector__is_delete=0,db_connector=A))
		else:E=DBConnectorUserShared.objects.filter(is_delete=0,user=C,db_connector__is_delete=0,db_connector=A)
		if E.count()>0:
			J=E[0];G=J.share_rights
			if G.is_admin or G.has_write_rights:H=datetime.now().astimezone(UTC);A.host=B[_S];A.port=B[_T];A.user=B[_U];A.password_e=qube_3df3f7aa47.sparta_f70c8bace8(B[_R]);A.database=B[_V];A.oracle_service_name=B[_X];A.keyspace=B[_Y];A.library_arctic=B[_Z];A.database_path=B[_a];A.csv_path=B[_b];A.csv_delimiter=B[_c];A.read_only=B[_d];A.json_url=B[_e];A.socket_url=B[_f];A.redis_db=B[_g];A.token=B.get(_t,'');A.organization=B.get(_u,'');A.lib_dir=B.get(_v,'');A.driver=B.get(_W,'');A.trusted_connection=B.get(_w,_D);A.dynamic_inputs=json.dumps(B[_J]);A.py_code_processing=B[_h];A.db_engine=B[_Q];A.name=B[_H];A.description=B[_O];A.last_update=H;A.last_date_used=H;A.save()
	return{_A:1}
def sparta_978c08f48a(json_data,user_obj):
	B=user_obj;F=json_data[_I];C=DBConnector.objects.filter(connector_id=F,is_delete=_C).all()
	if C.count()>0:
		A=C[C.count()-1];E=sparta_bcefba0d6f(B)
		if len(E)>0:D=DBConnectorUserShared.objects.filter(Q(is_delete=0,user_group__in=E,db_connector__is_delete=0,db_connector=A)|Q(is_delete=0,user=B,db_connector__is_delete=0,db_connector=A))
		else:D=DBConnectorUserShared.objects.filter(is_delete=0,user=B,db_connector__is_delete=0,db_connector=A)
		if D.count()>0:
			G=D[0];H=G.share_rights
			if H.is_admin:A.is_delete=_D;A.save()
	return{_A:1}
def sparta_8cad244f5b(package_name):
	A=subprocess.Popen([sys.executable,'-m','pip','install',package_name],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=_D);B,C=A.communicate()
	if A.returncode==0:return{_AG:_D,'output':B}
	else:return{_AG:_C,_AH:C}
def sparta_c7ad1dd0e4(json_data,user_obj):
	B=_C;C=[];D=json_data['pip_cmds']
	for E in D:
		A=sparta_8cad244f5b(E)
		if A[_AG]:logger.debug('Installation succeeded:',A['output'])
		else:logger.debug('Installation failed:',A[_AH]);B=_D;C.append(A[_AH])
	return{_A:1,'has_error':B,'errors':C}
def sparta_ba196c0b8c(connector_id,user_obj):
	B=user_obj;C=DBConnector.objects.filter(connector_id__startswith=connector_id,is_delete=_C).all()
	if C.count()==1:
		A=C[0];D=sparta_bcefba0d6f(B)
		if len(D)>0:E=DBConnectorUserShared.objects.filter(Q(is_delete=0,user_group__in=D,db_connector__is_delete=0,db_connector=A)|Q(is_delete=0,user=B,db_connector__is_delete=0,db_connector=A))
		else:E=DBConnectorUserShared.objects.filter(is_delete=0,user=B,db_connector__is_delete=0,db_connector=A)
		if E.count()>0:return A
class DotDict(dict):
	def __getattr__(A,name):return A.get(name,_B)
	def __setattr__(A,name,value):A[name]=value
	def __delattr__(A,name):del A[name]
def sparta_7bd58dc01f(obj):
	A=obj
	if isinstance(A,dict):
		B=DotDict()
		for(C,D)in A.items():B[C]=sparta_7bd58dc01f(D)
		return B
	elif isinstance(A,list):return[sparta_7bd58dc01f(A)for A in A]
	else:return A
def sparta_b790a8e18b(json_data,user_obj):
	B=json_data;D=B.get(_AY,_C)
	if D:A=sparta_7bd58dc01f(B)
	else:
		E=B[_I];A=sparta_ba196c0b8c(E,user_obj)
		if A is _B:return{_A:-1,_E:_i}
	C=Connector(db_engine=A.db_engine);C.init_with_model(A);F=C.get_available_tables();G=C.get_available_views();return{_A:1,'tables_explorer':F,'views_explorer':G}
def sparta_76d5372734(json_data,user_obj):
	A=json_data;G=A[_I];E=A[_M];H=int(A.get(_j,'0'))==1;B=[];C=sparta_ba196c0b8c(G,user_obj)
	if C is _B:return{_A:-1,_E:_i}
	D=Connector(db_engine=C.db_engine);D.init_with_model(C)
	if H:
		I=A[_x]
		try:F=D.get_data_table_query(I,E)
		except Exception as J:logger.debug(traceback.format_exc());return{_A:-1,_E:str(J)}
		K=list(K.columns)
		for(L,M)in zip(F.columns,F.dtypes):N={_H:L,'type':str(M)};B.append(N)
	else:B=D.get_table_columns(E)
	return{_A:1,'table_columns':B}
def sparta_e571152166(json_data,db_connector_obj):
	B=db_connector_obj
	if B.db_engine is not _B:
		if B.db_engine in['json_api','python','wss_api']:
			A=B.dynamic_inputs
			if A is not _B:
				try:A=json.loads(A)
				except:A=[]
			C=json_data.get(_J,[]);E=[A[_y]for A in A]
			for D in A:
				if D[_y]not in E:C.append(D)
			B.dynamic_inputs=json.dumps(C)
def sparta_423d3e6af7(json_data,user_obj):
	J=user_obj;A=json_data;print('json_data load_table_preview_explorer');print(A);G=A[_Q];print('db_engine >> '+str(G))
	if G=='spartaqube-data-store':
		A[_z]=A[_I];A[_M]=A['connector_name']
		if A.get(_j,_C):A[_K]=sparta_d8865dd244(A[_x])
		F=qube_2ab426de66.sparta_56b6ba7925(A,J)
		if F[_A]==1:
			try:
				if F['is_encoded_blob']:M=pickle.loads(base64.b64decode(F[_AI].encode(_A0)));N=[pickle.loads(A[_AJ]).assign(dispo=A[_K])for A in M];B=pd.concat(N);O=O.sort_index(ascending=_C);B.sort_values(by=_K,inplace=_D)
				else:B=F[_AK]
				return{_A:1,_F:convert_dataframe_to_json(B)}
			except Exception as H:print('Error load dataframe');print(H)
		return{_A:-1,_E:'Error loading this dataframe...'}
	if G=='clipboard_paste':I=json.loads(A[_F]);B=pd.DataFrame(I[_F],columns=I[_k],index=I[_A1]);return{_A:1,_F:convert_dataframe_to_json(B)}
	P=A[_I];Q=A.get(_AY,_C);D=A.get(_M,_B);K=int(A.get(_j,'0'))==1;L=int(A.get(_AZ,'0'))==0
	if Q:E=sparta_7bd58dc01f(A)
	else:
		E=sparta_ba196c0b8c(P,J)
		if E is _B:return{_A:-1,_E:_i}
	sparta_e571152166(A,E);C=Connector(db_engine=E.db_engine);C.init_with_model(E)
	if K is not _B:
		if K:
			R=A[_x]
			try:B=C.get_data_table_query(R,D)
			except Exception as H:logger.debug(traceback.format_exc());return{_A:-1,_E:str(H)}
		elif L:B=C.get_data_table_top(D)
		else:B=C.get_data_table(D)
	elif L:B=C.get_data_table_top(D)
	else:B=C.get_data_table(D)
	return{_A:1,_F:convert_dataframe_to_json(B)}
def sparta_30651cf3a3(json_data,user_obj):
	B=qube_2ab426de66.sparta_9213552ac5({},user_obj);A=[]
	if B[_A]==1:A=B['available_df']
	return{_A:1,'dataframes_explorer':A,'dataframes_explorer_name':[A[_H]for A in A]}
def sparta_c8e00abfa8(json_data,user_obj):
	S='config';R='dataframe_model_name';N='dispos';F=user_obj;C=json_data;print('load_spartaqube_data_store_preview_explorer json_data');print(C)
	if C.get(_R,_B)is not _B:A=qube_2ab426de66.sparta_9642817a5b(C,F)
	else:C[_M]=C.get(_H,_B);A=qube_2ab426de66.sparta_56b6ba7925(C,F)
	if A[_A]==1:
		G=qube_2ab426de66.sparta_cf2be782ae(C,F);H=dict();I=_l;J=_B;K=_B;L=_B
		if G is not _B:
			H=G.dataframe_config;D=G.plot_db_chart
			if D is not _B:I=D.plot_chart_id;J=D.data_source_list,;K=D.chart_params,;L=D.chart_config,
		if A[_Aa]:B=A[_AK];O=datetime.now().strftime(_P);B[_K]=O;M=A[R];B=process_dataframe_components(B);return{_A:1,_H:M,_F:convert_dataframe_to_json(B),N:[O],S:H,_G:I,_m:J,_A2:K,_A3:L}
		else:
			try:
				M=A[R];P=pickle.loads(base64.b64decode(A[_AI].encode(_A0)));T=[pickle.loads(A[_AJ]).assign(dispo=A[_K])for A in P];Q=sorted(list(set([str(A[_K])for A in P])))
				try:B=pd.concat(T);B=process_dataframe_components(B);return{_A:1,_H:M,_F:convert_dataframe_to_json(B),N:Q,S:H,_G:I,_m:J,_A2:K,_A3:L}
				except Exception as E:return{_A:-1,_E:str(E),'bRequireDispo':1,N:Q}
			except Exception as E:print('Except');print(E);return{_A:-1,_E:str(E)}
	if A[_A]==3:import time;time.sleep(2);return{_A:-1,_R:_n,_E:_n}
	return{_A:-1,_E:_Ab}
def sparta_d8865dd244(dispo):A=pickle.dumps(dispo);return base64.b64encode(A).decode(_A0)
def sparta_81932ddbf4(json_data,user_obj):
	E=user_obj;A=json_data;print('load_spartaqube_data_store_preview_explorer json_data 123');print(A);A[_K]=sparta_d8865dd244(A[_K])
	if A.get(_R,_B)is not _B:C=qube_2ab426de66.sparta_9642817a5b(A,E)
	else:A[_M]=A.get(_H,_B);C=qube_2ab426de66.sparta_56b6ba7925(A,E)
	if C[_A]==1:
		try:
			if C[_Aa]:B=C[_AK];F=datetime.now().strftime(_P);B[_K]=F;B=process_dataframe_components(B);return{_A:1,_F:convert_dataframe_to_json(B)}
			else:
				G=pickle.loads(base64.b64decode(C[_AI].encode(_A0)));H=[pickle.loads(A[_AJ]).assign(dispo=A[_K])for A in G]
				try:B=pd.concat(H,ignore_index=_D);B=B.sort_index(ascending=_C);return{_A:1,_F:convert_dataframe_to_json(B)}
				except Exception as D:return{_A:-1,_E:str(D)}
		except Exception as D:return{_A:-1,_E:str(D)}
	return{_A:-1,_E:_Ab}
def sparta_e5cc09b078(json_data,user_obj):
	A=json_data;F=A[_I];D=A.get(_M,'');G=int(A.get(_j,'0'))==1;K=A.get(_Q,_B);B=sparta_ba196c0b8c(F,user_obj)
	if B is _B:return{_A:-1,_E:_i}
	sparta_e571152166(A,B);C=Connector(db_engine=B.db_engine);C.init_with_model(B)
	if G:
		H=A[_x]
		try:E=C.get_data_table_query(H,D)
		except Exception as I:logger.debug(traceback.format_exc());return{_A:-1,_E:str(I)}
	else:E=C.get_data_table(D)
	J=E.describe();return{_A:1,_F:J.to_json(orient=_A4)}
def sparta_1edb6b5f56(json_data,user_obj):
	E=json_data
	def F(df):A=df;return pd.DataFrame({_H:A.columns,'non-nulls':len(A)-A.isnull().sum().values,'nulls':A.isnull().sum().values,'type':A.dtypes.values})
	A=json.loads(E[_F]);G=int(E['mode']);B=A[_k]
	if isinstance(B[0],list)or isinstance(B[0],tuple):H=[tuple(A)for A in B];C=pd.DataFrame(data=A[_F],columns=pd.MultiIndex.from_tuples(H),index=A[_A1])
	else:C=pd.DataFrame(data=A[_F],columns=B,index=A[_A1])
	D=''
	if G==1:I=F(C);D=I.to_html()
	else:J=C.describe();D=J.to_html()
	return{_A:1,'table':D}
def sparta_f3723d6abc(json_data,user_obj):
	A=json_data;D=A[_I];F=A.get(_M,_B);G=int(A.get(_j,'0'))==1;B=sparta_ba196c0b8c(D,user_obj)
	if B is _B:return{_A:-1,_E:_i}
	sparta_e571152166(A,B);C=Connector(db_engine=B.db_engine);C.init_with_model(B);E=C.get_db_connector().get_wss_structure();return{_A:1,_F:convert_dataframe_to_json(E)}
def sparta_2b881f82a4(json_data,user_obj,b_return_model=_C):
	A=json_data;print('save_plot');O=A[_N];D=_B
	if O:D=A[_A5];D=qube_9c73ae35fa.sparta_331d5499ac(D)
	P=A[_A6];Q=str(uuid.uuid4());B=datetime.now().astimezone(UTC);R=CodeEditorNotebook.objects.create(notebook_id=Q,cells=P,date_created=B,last_update=B);G=str(uuid.uuid4());H=A[_A7];I=A['is_gui_plot']
	if I:H=_D
	S=A.get('is_created_from_dataframe',_C);C=A['plotSlug']
	if len(C)==0:C=A[_A8]
	J=slugify(C);C=J;K=1
	while PlotDBChart.objects.filter(slug=C).exists():C=f"{J}-{K}";K+=1
	F=_B;E=A.get(_Ac,_B)
	if E is not _B:
		try:
			E=E.split(',')[1];T=base64.b64decode(E);U=os.path.dirname(__file__);V=os.path.dirname(os.path.dirname(os.path.dirname(U)));L=os.path.join(V,'static',_Ad,'widget');os.makedirs(L,exist_ok=_D);F=str(uuid.uuid4());W=os.path.join(L,f"{F}.png")
			with open(W,'wb')as X:X.write(T)
		except:pass
	print('CREATE plotDBChart');M=PlotDBChart.objects.create(plot_chart_id=G,type_chart=A[_Ae],name=A[_A8],slug=C,description=A[_A9],is_expose_widget=A[_AA],is_public_widget=A[_o],is_static_data=H,has_widget_password=A[_N],widget_password_e=D,data_source_list=A[_Af],chart_params=A[_Ag],chart_config=A[_Ah],code_editor_notebook=R,state_params=A.get('stateParamsDict',_B),is_created_from_api=I,is_created_from_dataframe=S,thumbnail_path=F,date_created=B,last_update=B,last_date_used=B,spartaqube_version=sparta_8d863c145d());Y=ShareRights.objects.create(is_admin=_D,has_write_rights=_D,has_reshare_rights=_D,last_update=B);PlotDBChartShared.objects.create(plot_db_chart=M,user=user_obj,share_rights=Y,is_owner=_D,date_created=B);N={_A:1,_G:G}
	if b_return_model:N[_L]=M
	return N
def sparta_73f7d5eb5b(json_data,user_obj):
	G=user_obj;A=json_data;K=A[_G];H=PlotDBChart.objects.filter(plot_chart_id=K,is_delete=_C).all()
	if H.count()>0:
		B=H[H.count()-1];L=sparta_bcefba0d6f(G)
		if len(L)>0:I=PlotDBChartShared.objects.filter(Q(is_delete=0,user_group__in=L,plot_db_chart__is_delete=0,plot_db_chart=B)|Q(is_delete=0,user=G,plot_db_chart__is_delete=0,plot_db_chart=B))
		else:I=PlotDBChartShared.objects.filter(is_delete=0,user=G,plot_db_chart__is_delete=0,plot_db_chart=B)
		if I.count()>0:
			O=I[0];M=O.share_rights
			if M.is_admin or M.has_write_rights:
				P=A.get(_N,_C);C=_B
				if P:C=A[_A5];C=qube_9c73ae35fa.sparta_331d5499ac(C)
				D=_B;E=A.get(_Ac,_B)
				if E is not _B:
					E=E.split(',')[1];R=base64.b64decode(E)
					try:
						S=os.path.dirname(__file__);T=os.path.dirname(os.path.dirname(os.path.dirname(S)));N=os.path.join(T,'static',_Ad,'widget');os.makedirs(N,exist_ok=_D)
						if B.thumbnail_path is _B:D=str(uuid.uuid4())
						else:D=B.thumbnail_path
						U=os.path.join(N,f"{D}.png")
						with open(U,'wb')as V:V.write(R)
					except:pass
				J=datetime.now().astimezone(UTC);B.type_chart=A[_Ae];B.name=A[_A8]
				if _A9 in A:B.description=A[_A9]
				if _AA in A:B.is_expose_widget=A[_AA]
				if _A7 in A:B.is_static_data=A[_A7]
				if _N in A:B.has_widget_password=A[_N];B.widget_password_e=C
				if _o in A:B.is_public_widget=A[_o]
				B.data_source_list=A[_Af];B.chart_params=A[_Ag];B.chart_config=A[_Ah];B.thumbnail_path=D;B.last_update=J;B.last_date_used=J;B.save();F=B.code_editor_notebook
				if F is not _B:
					if _A6 in A:F.cells=A[_A6];F.last_update=J;F.save()
	return{_A:1,_G:K}
def sparta_f1b1c871c4(json_data,user_obj):0
def sparta_45a6ac7b8d(json_data,user_obj):
	D=user_obj;F=sparta_bcefba0d6f(D)
	if len(F)>0:A=PlotDBChartShared.objects.filter(Q(is_delete=0,user_group__in=F,plot_db_chart__is_delete=0)|Q(is_delete=0,user=D,plot_db_chart__is_delete=0))
	else:A=PlotDBChartShared.objects.filter(is_delete=0,user=D,plot_db_chart__is_delete=0)
	if A.count()>0:
		C=json_data.get('orderBy',_s)
		if C==_s:A=A.order_by('-plot_db_chart__last_date_used')
		elif C==_AW:A=A.order_by('-plot_db_chart__last_update')
		elif C=='Date asc':A=A.order_by('plot_db_chart__last_update')
		elif C==_AX:A=A.order_by('-plot_db_chart__name')
		elif C=='Name asc':A=A.order_by('plot_db_chart__name')
		elif C=='Type':A=A.order_by('plot_db_chart__type_chart')
	G=[]
	for E in A:
		B=E.plot_db_chart;J=E.share_rights;H=_B
		try:H=str(B.last_update.strftime(_P))
		except:pass
		I=_B
		try:I=str(B.date_created.strftime(_P))
		except Exception as K:logger.debug(K)
		def L(x):
			try:float(x);return _D
			except ValueError:return _C
		G.append({_G:B.plot_chart_id,_p:B.type_chart,_H:B.name,_z:B.slug,_O:B.description,_AL:B.is_expose_widget,_AM:B.is_static_data,_AB:B.has_widget_password,_AC:B.is_public_widget,_AF:E.is_owner,_Ai:J.has_write_rights,'thumbnail_path':B.thumbnail_path,_AN:H,_AO:I,'is_developer_plot_db':not L(B.type_chart)})
	return{_A:1,_Aj:G}
def exec_notebook_and_get_workspace_variables(full_code,data_source_variables,workspace_variables,api_key):
	B=full_code;F=sparta_b6a401eb72()['project'];G=sparta_b6a401eb72()['project/core/api'];A='import sys, os\n';A+=f'sys.path.insert(0, r"{str(F)}")\n';A+=f'sys.path.insert(0, r"{str(G)}")\n';A+=f'os.environ["api_key"] = "{api_key}"\n';B=A+'\n'+B;D=dict();C=tinykernel.TinyKernel()
	for(H,I)in data_source_variables.items():C.glb[H]=I
	C(B)
	for E in workspace_variables:D[E]=C(E)
	return D
def sparta_df4344ecda(json_data,user_obj):
	b='kernelVariableName';a='isNotebook';Z='password_widget';C=json_data;D=C.get('token_permission','')
	if len(D)==0:D=_B
	I=C[_G];P=_B
	if Z in C:P=C[Z]
	c=C.get('dataSourceListOverride',[]);J=PlotDBChart.objects.filter(plot_chart_id__startswith=I,is_delete=_C).all()
	if J.count()==1:
		A=J[J.count()-1];I=A.plot_chart_id;E=_C
		if D is not _B:
			d=sparta_9f46127e8e(D)
			if d[_A]==1:E=_D
		if not E:
			if has_permission_widget_or_shared_rights(A,user_obj,password_widget=P):E=_D
		if E:
			Q=PlotDBChartShared.objects.filter(is_delete=0,plot_db_chart__is_delete=0,plot_db_chart=A)
			if Q.count()>0:
				K=Q[0];e=K.user;f=sparta_9b9e9c9338(e);R=K.user;L=[];A=K.plot_db_chart;g=A.is_static_data
				if g:0
				else:
					for B in A.data_source_list:
						M=B.get(a,_C)
						if M:L.append(B[b])
						else:
							if _J in B:
								h=B[_I];S=sparta_ba196c0b8c(h,R);T=[]
								if S.dynamic_inputs is not _B:
									try:T=json.loads(S.dynamic_inputs)
									except:pass
								N=B[_J];i=[A[_y]for A in N]
								for U in T:
									j=U[_y]
									if j not in i:N.append(U)
								B[_J]=N
								for F in c:
									if _I in F:
										if F[_I]==B[_I]:
											if F[_M]==B[_M]:B[_J]=F[_J]
							B[_AZ]=1;V=sparta_423d3e6af7(B,R)
							if V[_A]==1:k=V[_F];B[_F]=k
				W=A.code_editor_notebook
				if W is not _B:G=W.cells
				else:G=_B
				if len(L)>0:
					if G is not _B:
						l='\n'.join([A['code']for A in json.loads(G)]);X=dict()
						for H in A.data_source_list:
							if H.get('isDataSource',_C)or H.get('isClipboardPaste',_C):O=json.loads(H[_F]);X[H['table_name_workspace']]=pd.DataFrame(O[_F],index=O[_A1],columns=O[_k])
						m=exec_notebook_and_get_workspace_variables(l,X,L,f)
						for B in A.data_source_list:
							M=B[a]
							if M:Y=B[b];n=m[Y];B[_F]=convert_dataframe_to_json(convert_to_dataframe(n,variable_name=Y))
				def o(s):s=s.lower();A='-_.() %s%s'%(re.escape('/'),re.escape('\\'));B=re.sub('[^A-Za-z0-9%s]'%A,'_',s);return B
				return{_A:1,_G:I,_p:A.type_chart,_H:A.name,_z:A.slug,'name_file':o(A.name),_O:A.description,_AL:A.is_expose_widget,_AM:A.is_static_data,_AB:A.has_widget_password,_AC:A.is_public_widget,_m:A.data_source_list,_A2:A.chart_params,_A3:A.chart_config,_Ak:G,'state_params':A.state_params}
		else:return{_A:-1,_E:_n}
	return{_A:-1,_E:'Unexpected error, please try again'}
def sparta_d939df94fd(json_data,user_obj):
	B=json_data;logger.debug(_Al);logger.debug(B);D=B[_G];A=PlotDBChart.objects.filter(plot_chart_id=D,is_delete=_C).all()
	if A.count()>0:C=A[A.count()-1];E=datetime.now().astimezone(UTC);C.last_date_used=E;C.save()
	return{_A:1}
def sparta_4a2265c0f2(user_obj,widget_id):
	F='options';D=user_obj;C=_C;E=PlotDBChart.objects.filter(plot_chart_id__startswith=widget_id,is_delete=_C).all()
	if E.count()>0:
		A=E[E.count()-1]
		if A.is_expose_widget:
			if A.is_public_widget:C=_D
		if not C:
			G=sparta_bcefba0d6f(D)
			if len(G)>0:H=PlotDBChartShared.objects.filter(Q(is_delete=0,user_group__in=G,plot_db_chart__is_delete=0,plot_db_chart=A)|Q(is_delete=0,user=D,plot_db_chart__is_delete=0,plot_db_chart=A))
			else:H=PlotDBChartShared.objects.filter(is_delete=0,user=D,plot_db_chart__is_delete=0,plot_db_chart=A)
			if H.count()>0:C=_D
	if C:
		B=A.chart_params
		if F in B:B[F]=json.loads(B[F])
		if _F in B:B[_AP]=json.loads(B[_F])[_AP]
		I=A.type_chart;return{_A:1,'override_options':B,_p:I}
	else:return{_A:-1,_E:'You do not have the rights to access this template'}
def sparta_11d129b200(json_data,user_obj):
	X='is_index';R=json_data;K=user_obj;J='uuid'
	try:
		S=R[_G];Y=R['session_id'];L=PlotDBChart.objects.filter(plot_chart_id=S,is_delete=_C).all()
		if L.count()>0:
			A=L[L.count()-1];T=sparta_bcefba0d6f(K)
			if len(T)>0:M=PlotDBChartShared.objects.filter(Q(is_delete=0,user_group__in=T,plot_db_chart__is_delete=0,plot_db_chart=A)|Q(is_delete=0,user=K,plot_db_chart__is_delete=0,plot_db_chart=A))
			else:M=PlotDBChartShared.objects.filter(is_delete=0,user=K,plot_db_chart__is_delete=0,plot_db_chart=A)
			if M.count()>0:
				Z=M[0];A=Z.plot_db_chart;U=NewPlotApiVariables.objects.filter(session_id=Y).all()
				if U.count()>0:
					a=U[0];b=a.pickled_variables;E=cloudpickle.loads(b.encode('latin1'));F=dict()
					for G in A.data_source_list:C=G[J];F[C]=pd.DataFrame()
					H=json.loads(A.chart_config)
					for B in H.keys():
						if B in INPUTS_KEYS:
							if B=='xAxis':
								N=H[B];C=N[J];O=N[X];P=N[_q];D=F[C]
								if O:D.index=E[B]
								else:D[P]=E[B]
							elif H[B]is not _B:
								c=H[B]
								for(V,I)in enumerate(c):
									if I is not _B:
										C=I[J];O=I[X];P=I[_q];D=F[C]
										if O:D.index=E[B][V]
										else:D[P]=E[B][V]
					for G in A.data_source_list:C=G[J];G[_F]=F[C].to_json(orient=_A4)
				return{_A:1,_G:S,_p:A.type_chart,_H:A.name,_O:A.description,_AL:A.is_expose_widget,_AM:A.is_static_data,_AB:A.has_widget_password,_AC:A.is_public_widget,_m:A.data_source_list,_A2:A.chart_params,_A3:A.chart_config,_Ak:_B}
	except Exception as W:logger.debug('Error exception > '+str(W));return{_A:-1,_E:str(W)}
def sparta_601967adb3(json_data,user_obj):
	A=user_obj;G=json_data[_G];B=PlotDBChart.objects.filter(plot_chart_id=G,is_delete=_C).all()
	if B.count()>0:
		C=B[B.count()-1];E=sparta_bcefba0d6f(A)
		if len(E)>0:D=PlotDBChartShared.objects.filter(Q(is_delete=0,user_group__in=E,plot_db_chart__is_delete=0,plot_db_chart=C)|Q(is_delete=0,user=A,plot_db_chart__is_delete=0,plot_db_chart=C))
		else:D=PlotDBChartShared.objects.filter(is_delete=0,user=A,plot_db_chart__is_delete=0,plot_db_chart=C)
		if D.count()>0:F=D[0];F.is_delete=_D;F.save();print('Deleted plotDB')
	return{_A:1}
def sparta_9f46127e8e(token_permission):
	A=PlotDBPermission.objects.filter(token=token_permission)
	if A.count()>0:B=A[A.count()-1];return{_A:1,_L:B.plot_db_chart}
	return{_A:-1}
def has_permission_widget_or_shared_rights(plot_db_chart_obj,user_obj,password_widget=_B):
	B=user_obj;A=plot_db_chart_obj;F=A.has_widget_password;C=_C
	if B.is_authenticated:
		D=sparta_bcefba0d6f(B)
		if len(D)>0:E=PlotDBChartShared.objects.filter(Q(is_delete=0,user_group__in=D,plot_db_chart__is_delete=0,plot_db_chart=A)|Q(is_delete=0,user=B,plot_db_chart__is_delete=0,plot_db_chart=A))
		else:E=PlotDBChartShared.objects.filter(is_delete=0,user=B,plot_db_chart__is_delete=0,plot_db_chart=A)
		if E.count()>0:C=_D
	if C:return _D
	if A.is_expose_widget:
		if A.is_public_widget:
			if not F:return _D
			else:
				try:
					if qube_9c73ae35fa.sparta_201801731a(A.widget_password_e)==password_widget:return _D
					else:return _C
				except:return _C
		else:return _C
	return _C
def sparta_2901e6f78f(plot_chart_id,user_obj,password_widget=_B):
	F=password_widget;E=plot_chart_id;C=user_obj;logger.debug('CHECK NOW has_widget_access:');B=PlotDBChart.objects.filter(plot_chart_id__startswith=E,is_delete=_C).all();D=_C
	if B.count()==1:D=_D
	else:
		I=E;B=PlotDBChart.objects.filter(slug__startswith=I,is_delete=_C).all()
		if B.count()==1:D=_D
	if D:
		A=B[B.count()-1];J=A.has_widget_password
		if A.is_expose_widget:
			if A.is_public_widget:
				if not J:return{_A:1,_L:A}
				elif F is _B:return{_A:2,_E:'Require password',_L:A}
				else:
					try:
						if qube_9c73ae35fa.sparta_201801731a(A.widget_password_e)==F:return{_A:1,_L:A}
						else:return{_A:3,_E:_n,_L:A}
					except:return{_A:3,_E:_n,_L:A}
			elif C.is_authenticated:
				G=sparta_bcefba0d6f(C)
				if len(G)>0:H=PlotDBChartShared.objects.filter(Q(is_delete=0,user_group__in=G,plot_db_chart__is_delete=0,plot_db_chart=A)|Q(is_delete=0,user=C,plot_db_chart__is_delete=0,plot_db_chart=A))
				else:H=PlotDBChartShared.objects.filter(is_delete=0,user=C,plot_db_chart__is_delete=0,plot_db_chart=A)
				if H.count()>0:return{_A:1,_L:A}
			else:return{_A:-1}
	return{_A:-1}
def sparta_933c6bec3f(plot_chart_id,user_obj):
	F=plot_chart_id;C=user_obj;A=PlotDBChart.objects.filter(plot_chart_id__startswith=F,is_delete=_C).all();D=_C
	if A.count()==1:D=_D
	else:
		H=F;A=PlotDBChart.objects.filter(slug__startswith=H,is_delete=_C).all()
		if A.count()==1:D=_D
	if D:
		B=A[A.count()-1];G=sparta_bcefba0d6f(C)
		if len(G)>0:E=PlotDBChartShared.objects.filter(Q(is_delete=0,user_group__in=G,plot_db_chart__is_delete=0,plot_db_chart=B)|Q(is_delete=0,user=C,plot_db_chart__is_delete=0,plot_db_chart=B))
		else:E=PlotDBChartShared.objects.filter(is_delete=0,user=C,plot_db_chart__is_delete=0,plot_db_chart=B)
		if E.count()>0:I=E[0];B=I.plot_db_chart;return{_A:1,_r:_D,_L:B}
	return{_A:1,_r:_C}
def sparta_2e67d0450d(plot_db_chart_obj):
	B=json.loads(plot_db_chart_obj.chart_config);C=dict();E={_AD:'x',_AE:'y',_AU:'r',_AT:_AQ,'ohlcvArr':'ohlcv',_AV:'shaded_background'}
	for A in B.keys():
		if A in INPUTS_KEYS:
			try:
				F=E[A]
				if B[A]is not _B:
					D=len([A for A in B[A]if A is not _B])
					if D>0:C[F]=D
			except Exception as G:logger.debug('Except input struct');logger.debug(G)
	return C
def sparta_14000e12c7(json_data,user_obj):
	B=user_obj;D=sparta_bcefba0d6f(B)
	if len(D)>0:E=PlotDBChartShared.objects.filter(Q(is_delete=0,user_group__in=D,plot_db_chart__is_delete=0,plot_db_chart=A,plot_db_chart__is_expose_widget=_D)|Q(is_delete=0,user=B,plot_db_chart__is_delete=0,plot_db_chart__is_expose_widget=_D))
	else:E=PlotDBChartShared.objects.filter(is_delete=0,user=B,plot_db_chart__is_delete=0,plot_db_chart__is_expose_widget=_D)
	F=[]
	for C in E:
		A=C.plot_db_chart;I=C.share_rights;G=_B
		try:G=str(A.last_update.strftime(_P))
		except:pass
		H=_B
		try:H=str(A.date_created.strftime(_P))
		except Exception as J:logger.debug(J)
		F.append({_G:A.plot_chart_id,_p:A.type_chart,_AB:A.has_widget_password,_AC:A.is_public_widget,_H:A.name,_z:A.slug,_O:A.description,_AF:C.is_owner,_Ai:I.has_write_rights,_AN:G,_AO:H})
	return{_A:1,_Aj:F}
def sparta_1fa5156f98(json_data,user_obj):
	E=user_obj;B=json_data;K=B[_G];L=B['isCalledFromLibrary'];F=PlotDBChart.objects.filter(plot_chart_id=K,is_delete=_C).all()
	if F.count()>0:
		A=F[F.count()-1];H=sparta_bcefba0d6f(E)
		if len(H)>0:G=PlotDBChartShared.objects.filter(Q(is_delete=0,user_group__in=H,plot_db_chart__is_delete=0,plot_db_chart=A)|Q(is_delete=0,user=E,plot_db_chart__is_delete=0,plot_db_chart=A))
		else:G=PlotDBChartShared.objects.filter(is_delete=0,user=E,plot_db_chart__is_delete=0,plot_db_chart=A)
		if G.count()>0:
			M=G[0];I=M.share_rights
			if I.is_admin or I.has_write_rights:
				N=B[_N];C=_B
				if N:C=B[_A5];C=qube_9c73ae35fa.sparta_331d5499ac(C)
				J=datetime.now().astimezone(UTC);A.has_widget_password=B[_N];A.widget_password_e=C;A.name=B[_A8];A.plotDes=B[_A9];A.is_expose_widget=B[_AA];A.is_public_widget=B[_o];A.is_static_data=B[_A7];A.last_update=J;A.save()
				if L:0
				else:
					D=A.code_editor_notebook
					if D is not _B:D.cells=B[_A6];D.last_update=J;D.save()
	return{_A:1}
def sparta_e8212eebf7(json_data,user_obj):
	D=user_obj;B=json_data;I=B[_G];E=PlotDBChart.objects.filter(plot_chart_id=I,is_delete=_C).all()
	if E.count()>0:
		A=E[E.count()-1];G=sparta_bcefba0d6f(D)
		if len(G)>0:F=PlotDBChartShared.objects.filter(Q(is_delete=0,user_group__in=G,plot_db_chart__is_delete=0,plot_db_chart=A)|Q(is_delete=0,user=D,plot_db_chart__is_delete=0,plot_db_chart=A))
		else:F=PlotDBChartShared.objects.filter(is_delete=0,user=D,plot_db_chart__is_delete=0,plot_db_chart=A)
		if F.count()>0:
			J=F[0];H=J.share_rights
			if H.is_admin or H.has_write_rights:
				K=B[_N];C=_B
				if K:C=B[_A5];C=qube_9c73ae35fa.sparta_331d5499ac(C)
				L=datetime.now().astimezone(UTC);A.has_widget_password=B[_N];A.is_public_widget=B[_o];A.widget_password_e=C;A.last_update=L;A.save()
	return{_A:1}
def sparta_522bebb076(json_data,user_obj):
	B=json_data['plotDBId'];A=PlotDBChart.objects.filter(plot_chart_id=B,is_delete=_C).all()
	if A.count()>0:C=A[A.count()-1];return{_A:1,_H:C.name}
	return{_A:-1,_E:'Widget not found'}
def sparta_f20459a0d5(json_data,user_obj):
	B=user_obj;G=json_data[_G];C=PlotDBChart.objects.filter(plot_chart_id=G,is_delete=_C).all()
	if C.count()>0:
		A=C[C.count()-1];E=sparta_bcefba0d6f(B)
		if len(E)>0:D=PlotDBChartShared.objects.filter(Q(is_delete=0,user_group__in=E,plot_db_chart__is_delete=0,plot_db_chart=A)|Q(is_delete=0,user=B,plot_db_chart__is_delete=0,plot_db_chart=A))
		else:D=PlotDBChartShared.objects.filter(is_delete=0,user=B,plot_db_chart__is_delete=0,plot_db_chart=A)
		if D.count()>0:
			H=D[0];F=H.share_rights
			if F.is_admin or F.has_write_rights:I=datetime.now().astimezone(UTC);A.is_expose_widget=_C;A.last_update=I;A.save()
	return{_A:1}
def sparta_ac47eaf71a(user_obj):
	B=user_obj;C=sparta_bcefba0d6f(B)
	if len(C)>0:D=PlotDBChartShared.objects.filter(Q(is_delete=0,user_group__in=C,plot_db_chart__is_delete=0,plot_db_chart=A,plot_db_chart__is_expose_widget=_D)|Q(is_delete=0,user=B,plot_db_chart__is_delete=0,plot_db_chart__is_expose_widget=_D))
	else:D=PlotDBChartShared.objects.filter(is_delete=0,user=B,plot_db_chart__is_delete=0,plot_db_chart__is_expose_widget=_D)
	E=[]
	for F in D:
		A=F.plot_db_chart;J=F.share_rights;G=_B
		try:G=str(A.last_update.strftime(_P))
		except:pass
		H=_B
		try:H=str(A.date_created.strftime(_P))
		except Exception as I:logger.debug(I)
		E.append({'id':A.plot_chart_id,_H:A.name,_O:A.description,_AN:G,_AO:H})
	return E
def sparta_b9447b9359(json_data,user_obj):
	try:A=sparta_933c6bec3f(json_data[_Am],user_obj);B=A[_r];return{_A:1,_r:B}
	except:pass
	return{_A:-1}
def sparta_1cbfc387a5(json_data,user_obj):
	B=user_obj;A=json_data;C=sparta_933c6bec3f(A[_Am],B);D=C[_r]
	if D:E=C[_L];A[_G]=E.plot_chart_id;F=sparta_df4344ecda(A,B);return{_A:1,_F:[A[_F]for A in F[_m]]}
	return{_A:-1}
def sparta_959af63763(data_df,json_data):
	H='logTransformationDict';E='differencingDict';C=json_data;B=data_df
	if H in C:
		for(A,D)in C[H].items():
			if D:B[A]=B[A].apply(lambda x:math.log(x))
	if E in C:
		for(A,D)in C[E].items():
			if D:
				F=C.get(E,_B)
				if F is not _B:
					G=F.get(A,0)
					if G!=0:B[A]=B[A]-B[A].shift(G)
	return B
def sparta_94075d5074(json_data):
	J='column_renamed';E=json_data;K=json.loads(E[_AR]);L=json.loads(E[_AS]);H=json.loads(E['chartParamsEditorDict']);B=pd.DataFrame(L).T;F=[]
	try:
		for C in H[_AE]:
			A=C.get(J,_B)
			if A is _B:A=C.get(_q,_B)
			F.append(A)
		B.columns=F
	except:pass
	D=[]
	try:
		for C in H[_AD]:
			A=C.get(J,_B)
			if A is _B:A=C.get(_q,_B)
			I=list(B.columns)
			if A in I:G=len([B for B in I if B==A])+1;A=f"{A}_{G}"
			elif A in D:G=len([B for B in D if B==A])+1;A=f"{A}_{G}"
			D.append(A)
	except:pass
	for(M,N)in enumerate(K):B[D[M]]=N
	B=sparta_959af63763(B,E);return B,D,F
def sparta_8b38b36fbb(json_data,user_obj):
	j='cusum';i='You must add at least two series';h='Kmean';g='n_estimators';f='Relationships explorer data_df';e='model';d='Error matpltlib';c='matplotlib';b='Error quantstats';Z='nbComponents';W=user_obj;V='bNormalizeDecisionTree';U='maxDepth';S='trainTest';P='bInSample';K='paramsDict';G='B_DARK_THEME';E='relationship_explorer';A=json_data;from project.sparta_8345d6a892.sparta_26ea98fb42 import qube_1636bd2bde as X;Q=A['service']
	if Q=='quantstats':
		try:return X.sparta_938c80fd91(A,W)
		except Exception as R:logger.debug(b);logger.debug(traceback.format_exc());logger.debug(b);return{_A:-1,_E:str(R)}
	elif Q==c:
		try:return X.sparta_37ca61e590(A,W)
		except Exception as R:logger.debug(d);logger.debug(traceback.format_exc());return{_A:-1,_E:str(R)}
	elif Q==c:
		try:return X.sparta_37ca61e590(A,W)
		except Exception as R:logger.debug(d);logger.debug(traceback.format_exc());return{_A:-1,_E:str(R)}
	elif Q=='relationshipsExplorer':
		D=A[e];C,O,L=sparta_94075d5074(A);print(f);print(C);print(_Al);print(A);print(A.keys());M=_B
		if len(O)>0:M=O[0]
		if D=='LinearRegression':from project.sparta_8345d6a892.sparta_950a603163.qube_c177a21810 import sparta_949dd74671 as k;H=M;F=L;print(f"target_y_str > {H}");print(f"x_features_list > {F}");B=k(C,H,F,int(A.get('rw_beta',30)),int(A.get('rw_corr',30)),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='PolynomialRegression':from project.sparta_8345d6a892.sparta_950a603163.qube_c177a21810 import sparta_7c8640cb86 as l;H=M;F=L;B=l(C,H,F,degree=int(A.get('degree',2)),standardize=bool(A.get('standardize',_D)),in_sample=bool(A.get(P,_D)),test_size=float(A.get('test_size',.2)),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='DecisionTreeRegression':
			from project.sparta_8345d6a892.sparta_950a603163.qube_c177a21810 import sparta_489b543342 as m;H=M;F=L;I=A.get(U,-1)
			if str(I)==_l:I=_B
			else:I=int(I)
			B=m(C,H,F,max_depth=I,in_sample=A.get(P,_C),standardize=bool(A.get(V,_D)),test_size=1-float(A.get(S,80))/100,B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='DecisionTreeRegressionGridCV':
			from project.sparta_8345d6a892.sparta_950a603163.qube_c177a21810 import sparta_c2bd1e1d38 as n;H=M;F=L;print(f"target_y_str > {H}");print(f"x_features_list > {F}");I=A.get(U,-1)
			if str(I)==_l:I=_B
			else:I=int(I)
			B=n(C,H,F,max_depth=I,in_sample=A.get(P,_C),standardize=bool(A.get(V,_D)),test_size=1-float(A.get(S,80))/100,B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='RandomForestRegression':
			from project.sparta_8345d6a892.sparta_950a603163.qube_c177a21810 import sparta_5355980d1d as o;H=M;F=L;print(f"target_y_str > {H}");print(f"x_features_list > {F}");I=A.get(U,-1)
			if str(I)==_l:I=_B
			else:I=int(I)
			B=o(C,H,F,n_estimators=A.get(g,100),max_depth=I,in_sample=A.get(P,_C),standardize=bool(A.get(V,_D)),test_size=1-float(A.get(S,80))/100,B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='RandomForestRegressionGridCV':
			from project.sparta_8345d6a892.sparta_950a603163.qube_c177a21810 import sparta_df765dc206 as p;H=M;F=L;I=A.get(U,-1)
			if str(I)==_l:I=_B
			else:I=int(I)
			B=p(C,H,F,n_estimators=A.get(g,100),max_depth=I,in_sample=A.get(P,_C),standardize=bool(A.get(V,_D)),test_size=1-float(A.get(S,80))/100,B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='clustering':
			from project.sparta_8345d6a892.sparta_950a603163.qube_c177a21810 import sparta_5344c0bf7e as q,sparta_f0b3a7f755 as r;H=M;F=L
			if A.get('clusteringModel',h)==h:
				s=int(A.get(Z,3))
				if len(F)<2:return{_A:-1,_E:'You must select at least 2 columns'}
				B=q(C,F,s,B_DARK_THEME=A.get(G,_C))
			else:B=r(C,F,float(A.get('epsilon',.5)),int(A.get('minSamples',5)),B_DARK_THEME=A.get(G,_C))
			return{_A:1,E:json.dumps(B)}
		elif D=='correlation_network':from project.sparta_8345d6a892.sparta_950a603163.qube_c177a21810 import sparta_4c2cb5bb14 as t;H=M;F=L;B=t(C,F,float(A.get('threshold',.5)),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='pca':
			from project.sparta_8345d6a892.sparta_950a603163.qube_c177a21810 import sparta_4a2b04cca4 as u;H=M;F=L;T=int(A.get(Z,3));T=min(T,len(F))
			if T==1:return{_A:-1,_E:i}
			B=u(C,F,T,float(A.get('nbComponentsVariance',90)),bool(A.get('bScalePCA',_D)),int(A.get('pcaComponentsMode',1)),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='tsne':
			from project.sparta_8345d6a892.sparta_950a603163.qube_c177a21810 import sparta_6a5d637124 as v;H=M;F=L
			if len(F)<2:return{_A:-1,_E:i}
			B=v(C,F,int(A.get(Z,2)),int(A.get('perplexity',30)),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='features_importance':from project.sparta_8345d6a892.sparta_950a603163.qube_c177a21810 import sparta_ac0156402a as w;H=M;F=L;B=w(C,H,F,B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='mutual_information':from project.sparta_8345d6a892.sparta_950a603163.qube_c177a21810 import sparta_e75321f00e as x;H=M;F=L;B=x(C,H,F,B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='QuantileRegression':from project.sparta_8345d6a892.sparta_950a603163.qube_c177a21810 import sparta_35cc9e7361 as y;H=M;F=L;B=y(C,H,F,quantiles=A.get('selectedQuantiles',[.1,.5,.9]),standardize=bool(A.get('bNormalizeQuantileReg',_D)),in_sample=bool(A.get(P,_D)),test_size=1-float(A.get(S,80))/100,B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='RollingRegression':from project.sparta_8345d6a892.sparta_950a603163.qube_c177a21810 import sparta_1e352fb3b4 as z;H=M;F=L;B=z(C,H,F,A.get('window',20),bool(A.get('bNormalizeRollingReg',_D)),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='RecursiveRegression':from project.sparta_8345d6a892.sparta_950a603163.qube_c177a21810 import sparta_c228568878 as A0;H=M;F=L;B=A0(C,H,F,standardize=bool(A.get('bNormalizeRecursiveReg',_D)),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='statisticsSummary':from project.sparta_8345d6a892.sparta_950a603163.qube_c177a21810 import sparta_e24e88fdbc as A1;a=L;print('selected_columns');print(a);B=A1(C,a,B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B),'data_df_json':C[[A for A in list(C.columns)if A!='__sq_index__']].to_json(orient=_A4)}
	elif Q=='tsa':
		D=A[e];C,O,L=sparta_94075d5074(A);M=O[0];N=M;J=L;print(f);print(C);print(f"dates_col_str > {N}");print(f"variables_list > {J}");print(f"x_col_list > {O}");print(A.get(G,'NOT DEFINED'))
		if D=='STL':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_86d23b0ace as A2;B=A2(C[J],C[N],params_dict=A.get(K,_B),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='wavelet':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_d110be9040 as A3;B=A3(C[J],C[N],params_dict=A.get(K,_B),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='hmm':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_34e8ca5bf1 as A4;B=A4(C[J],C[N],params_dict=A.get(K,_B),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='ruptures':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_a13d5adad4 as A5;B=A5(C[J],C[N],params_dict=A.get(K,_B),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D==j:from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_85d23ef7e4 as Y;B=Y(C[J],C[N],params_dict=A.get(K,_B),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D==j:from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_85d23ef7e4 as Y;B=Y(C[J],C[N],params_dict=A.get(K,_B),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='zscore':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_8abadcb359 as A6;B=A6(C[J],C[N],params_dict=A.get(K,_B),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='isolation_forest':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_895418bd18 as A7;B=A7(C[J],C[N],params_dict=A.get(K,_B),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='mad':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_0cca0ad0dc as A8;B=A8(C[J],C[N],params_dict=A.get(K,_B),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='prophet_outlier':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_3d1548248c as A9;B=A9(C[J],C[N],params_dict=A.get(K,_B),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='granger':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_54aec20094 as AA;B=AA(C[J],C[N],params_dict=A.get(K,_B),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='cointegration':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_be805ec9ca as AB;B=AB(C[J],C[N],params_dict=A.get(K,_B),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='canonical_correlation':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_5bdfd766b5 as AC;print('X data_df[x_col_list]');print(C[O]);print('Y data_df[variables_list]');print(C[J]);B=AC(C[J],C[O],params_dict=A.get(K,_B),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='sarima':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_03bc317229 as AD;B=AD(C[J],C[N],params_dict=A.get(K,_B),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='ets':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_464afe73fc as AE;B=AE(C[J],C[N],params_dict=A.get(K,_B),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='prophet_forecast':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_d0b58a562f as AF;B=AF(C[J],C[N],params_dict=A.get(K,_B),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='var':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_1587f8ceee as AG;B=AG(C[J],C[N],params_dict=A.get(K,_B),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
		elif D=='adf':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_6b024d2e5e as AH;B=AH(C[J],params_dict=A.get(K,_B));return{_A:1,E:json.dumps(B)}
		elif D=='kpss':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_de2eafd5ea as AI;B=AI(C[J],params_dict=A.get(K,_B));return{_A:1,E:json.dumps(B)}
		elif D=='perron':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_7c27c48c5e as AJ;B=AJ(C[J],params_dict=A.get(K,_B));return{_A:1,E:json.dumps(B)}
		elif D=='za':from project.sparta_8345d6a892.sparta_950a603163.qube_14d0335fd8 import sparta_9519eea6d1 as AK;B=AK(C[J],C[N],params_dict=A.get(K,_B),B_DARK_THEME=A.get(G,_C));return{_A:1,E:json.dumps(B)}
	return{_A:1}
def sparta_65c2061a4d(json_data,user_obj):
	B=json_data;import quantstats as K;B=B[_F];G=B[_AR];L=B[_AS];H=B['columnsX'];I=B[_k];F=L;C=I
	if len(H)>1:C=H[1:]+I;F=G[1:]+F
	A=pd.DataFrame(F).T;A.index=pd.to_datetime(G[0]);A.columns=C
	try:A.index=A.index.tz_localize('UTC')
	except:pass
	for E in C:
		try:A[E]=A[E].astype(float)
		except:pass
	M=A.pct_change();D=pd.DataFrame()
	for(N,E)in enumerate(C):
		J=K.reports.metrics(M[E],mode='basic',display=_C)
		if N==0:D=J
		else:D=pd.concat([D,J],axis=1)
	D.columns=C;return{_A:1,'metrics':D.to_json(orient=_A4)}
def sparta_3ca44cf0ba(json_data,user_obj):
	N='Salary';A=json_data;A=A[_F];O=A[_AR];P=A[_AS];G=A['columnsX'];H=A[_k];C=P;I=H
	if len(G)>1:I=G+H;C=O+C
	D=pd.DataFrame(C).T;D.columns=I;E=['Country','City'];J=[N,'Rent'];J=[N];D.set_index(E,inplace=_D);B=D.groupby(E).mean();logger.debug('res_group_by_df');logger.debug(B);Q=E;F=len(B.index[0]);K=sorted(list(set(B.index.get_level_values(F-2))));L=[]
	def M(this_df,level=0,previous_index_list=_B):
		D=previous_index_list;C=this_df;A=level
		if A==F-1:
			for H in J:L.append({_F:[0]*len(K),_F:C[H].tolist(),_AQ:list(C.index.get_level_values(A)),'hierarchy':D,_q:H,'label':D[-1]})
		elif A<F-1:
			I=sorted(list(set(B.index.get_level_values(A))))
			for E in I:
				if D is _B:G=[E]
				else:G=D.copy();G.append(E)
				M(C[C.index.get_level_values(A)==E],A+1,G)
	M(B);logger.debug('chart_data');return{_A:1,_AP:L,_AQ:K}