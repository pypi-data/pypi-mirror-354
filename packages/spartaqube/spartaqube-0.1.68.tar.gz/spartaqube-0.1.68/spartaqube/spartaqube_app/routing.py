import importlib.metadata
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import re_path as url
from django.conf import settings
from project.sparta_ef90090f65.sparta_d44779d5cb import qube_553eed66f6,qube_a813860b16,qube_2eb7f038ac,qube_4a87a4eb7d,qube_fa6aaab335,qube_fdefd2623b,qube_4414f37385,qube_4476575a72,qube_3b0b46d409
from channels.auth import AuthMiddlewareStack
import channels
channels_ver=importlib.metadata.version('channels')
channels_major=int(channels_ver.split('.')[0])
def sparta_a3fa03010c(this_class):
	A=this_class
	if channels_major<=2:return A
	else:return A.as_asgi()
urlpatterns=[url('ws/statusWS',sparta_a3fa03010c(qube_553eed66f6.StatusWS)),url('ws/notebookWS',sparta_a3fa03010c(qube_a813860b16.NotebookWS)),url('ws/wssConnectorWS',sparta_a3fa03010c(qube_2eb7f038ac.WssConnectorWS)),url('ws/pipInstallWS',sparta_a3fa03010c(qube_4a87a4eb7d.PipInstallWS)),url('ws/gitNotebookWS',sparta_a3fa03010c(qube_fa6aaab335.GitNotebookWS)),url('ws/xtermGitWS',sparta_a3fa03010c(qube_fdefd2623b.XtermGitWS)),url('ws/hotReloadLivePreviewWS',sparta_a3fa03010c(qube_4414f37385.HotReloadLivePreviewWS)),url('ws/apiWebserviceWS',sparta_a3fa03010c(qube_4476575a72.ApiWebserviceWS)),url('ws/apiWebsocketWS',sparta_a3fa03010c(qube_3b0b46d409.ApiWebsocketWS))]
application=ProtocolTypeRouter({'websocket':AuthMiddlewareStack(URLRouter(urlpatterns))})
for thisUrlPattern in urlpatterns:
	try:
		if len(settings.DAPHNE_PREFIX)>0:thisUrlPattern.pattern._regex='^'+settings.DAPHNE_PREFIX+'/'+thisUrlPattern.pattern._regex
	except Exception as e:print(e)