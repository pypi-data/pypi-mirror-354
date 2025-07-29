import importlib.metadata
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import re_path as url
from django.conf import settings
from project.sparta_312a90fa32.sparta_11e219c6e8 import qube_8093016689,qube_a24cc3ce98,qube_0f2ddb9c82,qube_3a8ff6ce8e,qube_7ed3d409f5,qube_91475f07dd,qube_8dfeee642c,qube_7801244211,qube_221c2062ce
from channels.auth import AuthMiddlewareStack
import channels
channels_ver=importlib.metadata.version('channels')
channels_major=int(channels_ver.split('.')[0])
def sparta_abecde45b4(this_class):
	A=this_class
	if channels_major<=2:return A
	else:return A.as_asgi()
urlpatterns=[url('ws/statusWS',sparta_abecde45b4(qube_8093016689.StatusWS)),url('ws/notebookWS',sparta_abecde45b4(qube_a24cc3ce98.NotebookWS)),url('ws/wssConnectorWS',sparta_abecde45b4(qube_0f2ddb9c82.WssConnectorWS)),url('ws/pipInstallWS',sparta_abecde45b4(qube_3a8ff6ce8e.PipInstallWS)),url('ws/gitNotebookWS',sparta_abecde45b4(qube_7ed3d409f5.GitNotebookWS)),url('ws/xtermGitWS',sparta_abecde45b4(qube_91475f07dd.XtermGitWS)),url('ws/hotReloadLivePreviewWS',sparta_abecde45b4(qube_8dfeee642c.HotReloadLivePreviewWS)),url('ws/apiWebserviceWS',sparta_abecde45b4(qube_7801244211.ApiWebserviceWS)),url('ws/apiWebsocketWS',sparta_abecde45b4(qube_221c2062ce.ApiWebsocketWS))]
application=ProtocolTypeRouter({'websocket':AuthMiddlewareStack(URLRouter(urlpatterns))})
for thisUrlPattern in urlpatterns:
	try:
		if len(settings.DAPHNE_PREFIX)>0:thisUrlPattern.pattern._regex='^'+settings.DAPHNE_PREFIX+'/'+thisUrlPattern.pattern._regex
	except Exception as e:print(e)