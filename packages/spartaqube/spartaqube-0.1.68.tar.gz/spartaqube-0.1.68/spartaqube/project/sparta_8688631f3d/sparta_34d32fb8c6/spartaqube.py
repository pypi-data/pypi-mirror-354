_P='append'
_O='connector_id'
_N='Invalid chart type. Use an ID found in the DataFrame get_plot_types()'
_M='You do not have the rights to access this object'
_L='utf-8'
_K='data'
_J=False
_I='slug'
_H='dispo'
_G='table_name'
_F='100%'
_E='widget_id'
_D=True
_C='res'
_B='api_service'
_A=None
import os,json,uuid,base64,pickle,pandas as pd,urllib.parse
from IPython.core.display import display,HTML
import warnings
warnings.filterwarnings('ignore',message='Consider using IPython.display.IFrame instead',category=UserWarning)
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from project.models import UserProfile,PlotDBChart,PlotDBChartShared,PlotDBPermission,DataFrameShared,DataFramePermission
from project.sparta_8688631f3d.sparta_34d32fb8c6.qube_cbe6ad2077 import sparta_ec47a28c7f
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_8f0cad92aa import convert_to_dataframe,convert_dataframe_to_json,process_dataframe_components
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_5063fc4ff2 import sparta_6d633ad2e5
from project.sparta_8688631f3d.sparta_8c6a44fbc0 import qube_d70996b7fa as qube_d70996b7fa
class Spartaqube:
	_instance=_A
	def __new__(A,*B,**C):
		if A._instance is _A:A._instance=super().__new__(A);A._instance._initialized=_J
		return A._instance
	def __init__(A,api_token_id=_A):
		B=api_token_id
		if A._initialized:return
		A._initialized=_D
		if B is _A:
			try:B=os.environ['api_key']
			except:pass
		A.api_token_id=B;A.user_obj=UserProfile.objects.get(api_key=B).user
	def test(A):print('test')
	def get_widget_data(A,widget_id):B={_B:'get_widget_data',_E:widget_id};return sparta_ec47a28c7f(B,A.user_obj)
	def sparta_a92e0ee4e8(A,widget_id):B={_B:'has_widget_id',_E:widget_id};return sparta_ec47a28c7f(B,A.user_obj)
	def get_widget(C,widget_id,width=_F,height=500):
		A=PlotDBChartShared.objects.filter(is_delete=0,user=C.user_obj,plot_db_chart__is_delete=0,plot_db_chart__plot_chart_id=widget_id)
		if A.count()>0:B=str(uuid.uuid4());D=datetime.now().astimezone(UTC);PlotDBPermission.objects.create(plot_db_chart=A[0].plot_db_chart,token=B,date_created=D);return HTML(f'<iframe src="/plot-widget-token/{B}" width="{width}" height="{height}" frameborder="0" allow="clipboard-write"></iframe>')
		return _M
	def iplot(I,*B,width=_F,height=550):
		if len(B)==0:raise Exception('You must pass at least one input variable to plot')
		else:
			C=dict()
			for(E,D)in enumerate(B):
				if D is _A:continue
				F=convert_to_dataframe(D);C[E]=convert_dataframe_to_json(F)
			G=json.dumps(C);A=str(uuid.uuid4());H=f'''
                <form id="dataForm_{A}" action="plot-gui" method="POST" target="{A}">
                    <input type="hidden" name="data" value=\'{G}\' />
                </form>
                <iframe 
                    id="{A}"
                    name="{A}"
                    width="{width}" 
                    height="{height}" 
                    frameborder="0" 
                    allow="clipboard-write"></iframe>

                <script>
                    // Submit the form automatically to send data to the iframe
                    document.getElementById(\'dataForm_{A}\').submit();
                </script>
                ''';return HTML(H)
	def plot(V,*W,**A):
		I='width';H='chart_type';D=dict()
		for(J,F)in A.items():
			if F is _A:continue
			K=convert_to_dataframe(F);D[J]=convert_dataframe_to_json(K)
		E=_A
		if H not in A:
			if _E not in A:raise Exception("Missing chart_type parameter. For instance: chart_type='line'")
			else:E=0
		if E is _A:
			L=sparta_6d633ad2e5(b_return_type_id=_D)
			try:M=json.loads(D[H])[_K][0][0];E=[A for A in L if A['ID']==M][0]['type_plot']
			except:raise Exception(_N)
		N=A.get(I,_F);O=A.get(I,'500');P=A.get('interactive',_D);G=A.get(_E,_A);Q={'interactive_api':1 if P else 0,'is_api_template':1 if G is not _A else 0,_E:G};R=json.dumps(Q);S=urllib.parse.quote(R);B=dict();B[_C]=1;B['notebook_variables']=D;B['type_chart']=E;B['override_options']=D.get('options',dict());print('data_res_dict');print(B);T=json.dumps(B);C=str(uuid.uuid4());U=f'''
            <form id="dataForm_{C}" action="plot-api/{S}" method="POST" target="{C}">
                <input type="hidden" name="data" value=\'{T}\' />
            </form>
            <iframe 
                id="{C}"
                name="{C}"
                width="{N}" 
                height="{O}" 
                frameborder="0" 
                allow="clipboard-write"></iframe>

            <script>
                // Submit the form automatically to send data to the iframe
                document.getElementById(\'dataForm_{C}\').submit();
            </script>
            ''';return HTML(U)
	def plot_documentation(B,chart_type='line'):
		A=chart_type;C=B.get_plot_types()
		if len([B for B in C if B['ID']==A])>0:D=f"api#plot-{A}";return D
		else:raise Exception(_N)
	def plot_template(B,*C,**A):
		if _E in A:return B.plot(*C,**A)
		raise Exception('Missing widget_id')
	def get_connector_tables(A,connector_id):B={_B:'get_connector_tables',_O:connector_id};return sparta_ec47a28c7f(B,A.user_obj)
	def get_data_from_connector(I,connector_id,table=_A,sql_query=_A,output_format=_A,dynamic_inputs=_A):
		G=dynamic_inputs;F=output_format;E=sql_query;A={_B:'get_data_from_connector'};A[_O]=connector_id;A[_G]=table;A['query_filter']=E;A['bApplyFilter']=1 if E is not _A else 0;H=[]
		if G is not _A:
			for(J,K)in G.items():H.append({'input':J,'default':K})
		A['dynamic_inputs']=H;B=sparta_ec47a28c7f(A,I.user_obj);C=_J
		if F is _A:C=_D
		elif F=='DataFrame':C=_D
		if C:
			if B[_C]==1:D=json.loads(B[_K])
			return pd.DataFrame(D[_K],index=D['index'],columns=D['columns'])
		return B
	def apply_method(B,method_name,*D,**C):A=C;A[_B]=method_name;return sparta_ec47a28c7f(A,B.user_obj)
	def __getattr__(A,name):return lambda*B,**C:A.apply_method(name,*B,**C)
	def sparta_126dfbb816(B,dispo):A=pickle.dumps(dispo);return base64.b64encode(A).decode(_L)
	def sparta_8b8da00f6d(C,df,table_name,dispo=_A,mode=_P):
		A=dispo;B={_B:'put_df'};E=pickle.dumps(df);F=base64.b64encode(E).decode(_L);B['df']=F;B[_G]=table_name;B['mode']=mode;B[_H]=C.format_dispo(A)
		if mode not in[_P,'replace']:raise Exception("Mode should be: 'append' or 'replace'")
		if isinstance(A,pd.Series)or isinstance(A,pd.DatetimeIndex)or type(A).__name__=='ndarray'and type(A).__module__=='numpy':A=list(A);B[_H]=C.format_dispo(A)
		if isinstance(A,list):
			if len(A)!=len(df):raise Exception('If you want to use a list of dispo, it must have the same length at the dataframe')
		D=qube_d70996b7fa.sparta_8b8da00f6d(B,C.user_obj)
		if D[_C]==1:print('Dataframe inserted successfully!')
		return D
	def sparta_521aed69f1(C,table_name,slug=_A):
		A={_B:'drop_df'};A[_G]=table_name;A[_I]=slug;B=qube_d70996b7fa.sparta_521aed69f1(A,C.user_obj)
		if B[_C]==1:print('Dataframe dropped successfully!')
		return B
	def sparta_e5b146daee(C,id):
		A={_B:'drop_df_by_id'};A['id']=id;B=qube_d70996b7fa.sparta_e5b146daee(A,C.user_obj)
		if B[_C]==1:print(f"Dataframe dropped successfully for dispo!")
		return B
	def sparta_89abaa23b9(B,table_name,dispo,slug=_A):
		C=dispo;A={_B:'drop_dispo_df'};A[_G]=table_name;A[_H]=B.format_dispo(C);A[_I]=slug;D=qube_d70996b7fa.sparta_89abaa23b9(A,B.user_obj)
		if D[_C]==1:print(f"Dataframe dropped successfully for dispo {C} !")
		return D
	def sparta_b9341eb929(A):B={_B:'get_available_df'};return qube_d70996b7fa.sparta_b9341eb929(B,A.user_obj)
	def sparta_db94f6cb87(D,table_name,dispo=_A,slug=_A,b_concat=_D):
		A={_B:'get_df'};A[_G]=table_name;A[_H]=D.format_dispo(dispo);A[_I]=slug;B=qube_d70996b7fa.sparta_db94f6cb87(A,D.user_obj)
		if B[_C]==1:
			F=pickle.loads(base64.b64decode(B['encoded_blob'].encode(_L)));E=[pickle.loads(A['df_blob']).assign(dispo=A[_H])for A in F]
			if b_concat:
				try:C=pd.concat(E);C=process_dataframe_components(C);return C
				except Exception as G:print('Could not concatenate all dataframes together with following error message:');raise str(G)
			else:return E
		return B
	def open_df(C,dataframe_id,width=_F,height=500):
		A=DataFrameShared.objects.filter(is_delete=0,user=C.user_obj,plot_db_chart__is_delete=0,plot_db_chart__plot_chart_id=widget_id)
		if A.count()>0:B=str(uuid.uuid4());D=datetime.now().astimezone(UTC);DataFramePermission.objects.create(dataframe_model=A[0].plot_db_chart,token=B,date_created=D);return HTML(f'<iframe src="/plot-dataframe-token/{B}" width="{width}" height="{height}" frameborder="0" allow="clipboard-write"></iframe>')
		return _M
	def sparta_b6ad0dd8e2(A,slug):B={_B:'has_dataframe_slug',_I:slug};return sparta_ec47a28c7f(B,A.user_obj)
	def open_data_df(F,data_df,name='',width=_F,height=600,detached=_J):
		A=str(uuid.uuid4());C=convert_dataframe_to_json(data_df);D=json.dumps(C);B=A
		if detached:B=name
		E=f'''
        <form id="dataForm_{A}" action="/plot-gui-df" method="POST" target="{A}">
            <input type="hidden" name="data" value=\'{D}\' />
            <input type="hidden" name="name" value=\'{name}\' />
        </form>
        <iframe 
            id="{A}"
            name="{B}"
            width="{width}" 
            height="{height}" 
            frameborder="0" 
            allow="clipboard-write"></iframe>
        <script>
            // Submit the form automatically to send data to the iframe
            document.getElementById(\'dataForm_{A}\').submit();
        </script>
        ''';return HTML(E)