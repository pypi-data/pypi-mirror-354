from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_3ac03f635b.sparta_915d77f7e0.qube_cc88537447.sparta_bf9dde3d9b'
handler500='project.sparta_3ac03f635b.sparta_915d77f7e0.qube_cc88537447.sparta_6c26f566ad'
handler403='project.sparta_3ac03f635b.sparta_915d77f7e0.qube_cc88537447.sparta_6adcddecbd'
handler400='project.sparta_3ac03f635b.sparta_915d77f7e0.qube_cc88537447.sparta_cb70dd10ea'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]