_C=True
_B=False
_A=None
import os,json,platform,websocket,threading,time,pandas as pd
from pathlib import Path
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from project.logger_config import logger
from project.sparta_312a90fa32.sparta_6696c7e57c import qube_52d8b82b2d as qube_52d8b82b2d
from project.sparta_8345d6a892.sparta_952c41e91e import qube_41685030f2 as qube_41685030f2
from project.sparta_8345d6a892.sparta_b7018498c9.qube_5119bc741a import sparta_b73a88c789
from project.sparta_8345d6a892.sparta_b7018498c9.qube_9f327d0231 import sparta_eca660fb82
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import convert_to_dataframe,convert_dataframe_to_json,sparta_ad557db230
from project.sparta_8345d6a892.sparta_490625ab5b.qube_dc2c1eaf05 import SenderKernel
from project.sparta_8345d6a892.sparta_f1a366f59f.qube_137201374c import sparta_8fe31d66cd,sparta_374e43cb4b,get_api_key_async
class NotebookWS(AsyncWebsocketConsumer):
	channel_session=_C;http_user_and_session=_C
	async def connect(A):logger.debug('Connect Now');await A.accept();A.user=A.scope['user'];A.json_data_dict=dict();A.sender_kernel_obj=_A
	async def disconnect(A,close_code=_A):
		logger.debug('Disconnect')
		if A.sender_kernel_obj is not _A:A.sender_kernel_obj.zmq_close()
		try:await A.close()
		except:pass
	async def notebook_permission_code_exec(A,json_data):from project.sparta_8345d6a892.sparta_b5395e1261 import qube_a357901b33 as B;return await coreNotebook.notebook_permission_code_exec(json_data)
	async def prepare_sender_kernel(A,kernel_manager_uuid):
		from project.models import KernelProcess as C;B=await sync_to_async(lambda:list(C.objects.filter(kernel_manager_uuid=kernel_manager_uuid)),thread_sensitive=_B)()
		if len(B)>0:
			D=B[0];E=D.port
			if A.sender_kernel_obj is _A:A.sender_kernel_obj=SenderKernel(A,E)
			A.sender_kernel_obj.zmq_connect()
	async def get_kernel_type(D,kernel_manager_uuid):
		from project.models import KernelProcess as B;A=await sync_to_async(lambda:list(B.objects.filter(kernel_manager_uuid=kernel_manager_uuid)),thread_sensitive=_B)()
		if len(A)>0:C=A[0];return C.type
		return 1
	async def receive(B,text_data):
		AM='kernel_variable_arr';AL='workspace_variables_to_update';AK='repr_data';AJ='raw_data';AI='cellTitleVarName';AH='execCodeTitle';AG='cellId';AF='cell_id';AE='cellCode';AD='activate_venv';AC='venv_name';AB='import json\n';v=text_data;u='updated_variables';t='output';s='defaultDashboardVars';l='assignGuiComponentVariable';k='variable';j='get_workspace_variable';i='value';b='get_kernel_variable_repr';a='code';Z='json_data';U='errorMsg';R='dashboardVenv';P='\n';O='';N='execute_code';M='kernel_variable';L='cmd';F='res';D='service'
		if len(v)>0:
			A=json.loads(v);E=A[D];w=A['kernelManagerUUID'];await B.prepare_sender_kernel(w);AN=await B.get_kernel_type(w)
			def X(code_to_exec,json_data):
				D=json_data;B=code_to_exec;A=AB
				if s in D:
					E=D[s]
					for(C,F)in E.items():
						if len(C)>0:G=F['outputDefaultValue'];A+=f'if "{C}" in globals():\n    pass\nelse:\n    {C} = {repr(G)}\n'
				H=json.dumps({i:_A,'col':-1,'row':-1});A+=f"if \"last_action_state\" in globals():\n    pass\nelse:\n    last_action_state = json.loads('{H}')\n"
				if len(A)>0:B=f"{A}\n{B}"
				return B
			async def S(json_data):
				E='projectSysPath';C=json_data
				if E in C:
					if len(C[E])>0:A=sparta_ad557db230(C[E]);A=Path(A).resolve();F=f'import sys, os\nsys.path.insert(0, r"{str(A)}")\nos.chdir(r"{str(A)}")\n';await B.sender_kernel_obj.send_zmq_request({D:N,L:F})
			async def c(json_data):
				A=json_data
				if R in A:
					if A[R]is not _A:
						if len(A[R])>0:C=A[R];await B.sender_kernel_obj.send_zmq_request({D:AD,AC:C})
			if E=='init-socket'or E=='reconnect-kernel'or E=='reconnect-kernel-run-all':
				G={F:1,D:E}
				if s in A:J=X(O,A);await B.sender_kernel_obj.send_zmq_request({D:N,L:J})
				await S(A);await c(A);C=json.dumps(G);await B.send(text_data=C);return
			elif E=='disconnect':B.disconnect()
			elif E=='exec':
				await S(A);AO=time.time();logger.debug('='*50);d=A[AE];J=d
				if AN==5:logger.debug('Execute for the notebook Execution Exec case');logger.debug(A);J=await B.notebook_permission_code_exec(A)
				J=X(J,A);x=_B
				if d is not _A:
					if len(d)>0:
						if d[0]=='!':x=_C
				if x:await B.sender_kernel_obj.send_zmq_request({D:'execute_shell',L:J,Z:json.dumps(A)})
				else:await B.sender_kernel_obj.send_zmq_request({D:'execute',L:J,Z:json.dumps(A)})
				try:y=sparta_b73a88c789(A[AE])
				except:y=[]
				logger.debug('='*50);AP=time.time()-AO;C=json.dumps({F:2,D:E,'elapsed_time':round(AP,2),AF:A[AG],'updated_plot_variables':y,'input':json.dumps(A)});await B.send(text_data=C)
			elif E=='trigger-code-gui-component-input':
				S(A)
				try:
					try:m=json.loads(A[AH]);I=P.join([A[a]for A in m])
					except:I=O
					AQ=json.loads(A['execCodeInput']);z=P.join([A[a]for A in AQ]);V=X(z,A);V+=P+I;await B.sender_kernel_obj.send_zmq_request(sender_dict={D:N,L:V},b_send_websocket_msg=_B);W=sparta_b73a88c789(z);A0=A['guiInputVarName'];AR=A['guiOutputVarName'];AS=A[AI];n=[A0,AR,AS];Y=[]
					for T in n:
						try:Q=await B.sender_kernel_obj.send_zmq_request({D:b,M:T})
						except:Q=json.dumps({F:1,t:O})
						o=convert_dataframe_to_json(convert_to_dataframe(await B.sender_kernel_obj.send_zmq_request({D:j,M:T}),A0));Y.append({k:T,AJ:o,AK:Q})
				except Exception as H:C=json.dumps({F:-1,D:E,U:str(H)});logger.debug('Error',C);await B.send(text_data=C);return
				C=json.dumps({F:1,D:E,u:W,AL:Y});await B.send(text_data=C)
			elif E=='trigger-code-gui-component-output':
				S(A)
				try:
					A1=O;e=O
					if l in A:f=A[l];A2=sparta_eca660fb82(f);A1=A2['assign_state_variable'];e=A2['assign_code']
					AT=json.loads(A['execCodeOutput']);A3=P.join([A[a]for A in AT]);V=e+P;V+=A1+P;V+=A3;await B.sender_kernel_obj.send_zmq_request(sender_dict={D:N,L:V},b_send_websocket_msg=_B);W=sparta_b73a88c789(A3)
					try:W.append(A[l][k])
					except Exception as H:pass
				except Exception as H:C=json.dumps({F:-1,D:E,U:str(H)});await B.send(text_data=C);return
				C=json.dumps({F:1,D:E,u:W});logger.debug(f"return final here {C}");await B.send(text_data=C)
			elif E=='assign-kernel-variable-from-gui':
				try:f=A[l];AU=f[i];e=f"{f[k]} = {AU}";await B.sender_kernel_obj.send_zmq_request({D:N,L:e})
				except Exception as H:C=json.dumps({F:-1,D:E,U:str(H)});await B.send(text_data=C);return
				C=json.dumps({F:1,D:E});await B.send(text_data=C)
			elif E=='exec-main-dashboard-notebook-init':
				await S(A);await c(A);J=A['dashboardFullCode'];J=X(J,A)
				try:await B.sender_kernel_obj.send_zmq_request({D:N,L:J},b_send_websocket_msg=_B)
				except Exception as H:C=json.dumps({F:-1,D:E,U:str(H)});await B.send(text_data=C);return
				A4=A['plotDBRawVariablesList'];AV=A4;A5=[];A6=[]
				for p in A4:
					try:A5.append(convert_dataframe_to_json(convert_to_dataframe(await B.sender_kernel_obj.send_zmq_request({D:j,M:p}),p)));A6.append(await B.sender_kernel_obj.send_zmq_request({D:b,M:p}))
					except Exception as H:logger.debug('Except get var');logger.debug(H)
				C=json.dumps({F:1,D:E,'variables_names':AV,'variables_raw':A5,'variables_repr':A6});await B.send(text_data=C)
			elif E=='trigger-action-plot-db':
				logger.debug('TRIGGER CODE ACTION PLOTDB');logger.debug(A)
				try:
					g=AB;g+=f"last_action_state = json.loads('{A['actionDict']}')\n"
					try:AW=json.loads(A['triggerCode']);q=P.join([A[a]for A in AW])
					except:q=O
					g+=P+q;logger.debug('cmd to execute');logger.debug('cmd_to_exec');logger.debug(g);await B.sender_kernel_obj.send_zmq_request({D:N,L:g});W=sparta_b73a88c789(q)
				except Exception as H:C=json.dumps({F:-1,D:E,U:str(H)});await B.send(text_data=C);return
				C=json.dumps({F:1,D:E,u:W});await B.send(text_data=C)
			elif E=='dynamic-title':
				try:m=json.loads(A[AH]);I=P.join([A[a]for A in m])
				except:I=O
				if len(I)>0:
					I=X(I,A);await S(A);await c(A)
					try:
						await B.sender_kernel_obj.send_zmq_request({D:N,L:I});A7=A[AI];n=[A7];Y=[]
						for T in n:
							try:Q=await B.sender_kernel_obj.send_zmq_request({D:b,M:T})
							except:Q=json.dumps({F:1,t:O})
							o=convert_dataframe_to_json(convert_to_dataframe(await B.sender_kernel_obj.send_zmq_request({D:j,M:T}),A7));Y.append({k:T,AJ:o,AK:Q})
						C=json.dumps({F:1,D:E,AL:Y});await B.send(text_data=C)
					except Exception as H:C=json.dumps({F:-1,D:E,U:str(H)});logger.debug('Error',C);logger.debug(I);await B.send(text_data=C);return
			elif E=='dashboard-map-dataframe-python':AX=A['notebookVar'];AY=A['jsonDataFrame'];I=f"jsonDataFrameDictTmp = json.loads('{AY}')\n";I+=f"{AX} = pd.DataFrame(index=jsonDataFrameDictTmp['index'], columns=jsonDataFrameDictTmp['columns'], data=jsonDataFrameDictTmp['data'])";await B.sender_kernel_obj.send_zmq_request({D:N,L:I});C=json.dumps({F:1,D:E});await B.send(text_data=C)
			elif E=='reset':await B.sender_kernel_obj.send_zmq_request({D:'reset_kernel_workspace'});await c(A);G={F:1,D:E};C=json.dumps(G);await B.send(text_data=C)
			elif E=='workspace-list':AZ=await B.sender_kernel_obj.send_zmq_request({D:'list_workspace_variables'});G={F:1,D:E,'workspace_variables':AZ};G.update(A);C=json.dumps(G);await B.send(text_data=C)
			elif E=='workspace-get-variable-as-df':
				A8=[];A9=[];AA=[]
				for h in A[AM]:
					Aa=await B.sender_kernel_obj.send_zmq_request({D:j,M:h});Ab=convert_to_dataframe(Aa,variable_name=h)
					try:A8.append(convert_dataframe_to_json(Ab));A9.append(h)
					except:pass
					try:Q=await B.sender_kernel_obj.send_zmq_request({D:b,M:h})
					except:Q=json.dumps({F:1,t:O})
					AA.append(Q)
				G={F:1,D:E,AM:A9,'workspace_variable_arr':A8,'kernel_variable_repr_arr':AA};C=json.dumps(G);await B.send(text_data=C)
			elif E=='workspace-get-variable'or E=='workspace-get-variable-preview':Ac=await B.sender_kernel_obj.send_zmq_request({D:b,M:A[M]});G={F:1,D:E,AF:A.get(AG,_A),'workspace_variable':Ac};C=json.dumps(G);await B.send(text_data=C)
			elif E=='workspace-set-variable-from-datasource':
				if i in list(A.keys()):await B.sender_kernel_obj.send_zmq_request({D:'set_workspace_variable_from_datasource',Z:json.dumps(A)});G={F:1,D:E};C=json.dumps(G);await B.send(text_data=C)
			elif E=='workspace-set-variable':
				if i in list(A.keys()):await B.sender_kernel_obj.send_zmq_request({D:'set_workspace_variable',Z:json.dumps(A)});G={F:1,D:E};C=json.dumps(G);await B.send(text_data=C)
			elif E=='workspace-set-variable-from-paste-modal':
				K=pd.DataFrame(A['clipboardData']);r=A['delimiters']
				if r is not _A:
					if len(r)>0:Ad=K.columns;K=K[Ad[0]].str.split(r,expand=_C)
				if A['bFirstRowHeader']:K.columns=K.iloc[0];K=K[1:].reset_index(drop=_C)
				if A['bFirstColIndex']:K=K.set_index(K.columns[0])
				Ae={'name':A['name'],'df_json':K.to_json(orient='split')};await B.sender_kernel_obj.send_zmq_request({D:'set_workspace_variable_from_paste_modal',Z:json.dumps(Ae)});G={F:1,D:E};C=json.dumps(G);await B.send(text_data=C)
			elif E=='set-sys-path-import':
				if'projectPath'in A:await S(A)
				G={F:1,D:E};C=json.dumps(G);await B.send(text_data=C)
			elif E=='set-kernel-venv':
				if R in A:
					if A[R]is not _A:
						if len(A[R])>0:Af=A[R];await B.sender_kernel_obj.send_zmq_request({D:AD,AC:Af})
				G={F:1,D:E};C=json.dumps(G);await B.send(text_data=C)
			elif E=='deactivate-venv':await B.sender_kernel_obj.send_zmq_request({D:'deactivate_venv'});G={F:1,D:E};C=json.dumps(G);await B.send(text_data=C)
			elif E=='get-widget-iframe':
				logger.debug('Deal with iframe here');from IPython.core.display import display,HTML;import warnings as Ag;Ag.filterwarnings('ignore',message='Consider using IPython.display.IFrame instead',category=UserWarning)
				try:Ah=A['widget_id'];Ai=await get_api_key_async(B.user);Aj=await sync_to_async(lambda:HTML(f'<iframe src="/plot-widget/{Ah}/{Ai}" width="100%" height="500" frameborder="0" allow="clipboard-write"></iframe>').data)();G={F:1,D:E,'widget_iframe':Aj};C=json.dumps(G);await B.send(text_data=C)
				except Exception as H:G={F:-1,U:str(H)};C=json.dumps(G);await B.send(text_data=C)