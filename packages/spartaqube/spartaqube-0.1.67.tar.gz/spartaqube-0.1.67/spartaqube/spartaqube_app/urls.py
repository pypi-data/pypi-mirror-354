from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_b16f09cf2c.sparta_183195ea40.qube_c0da5e02a3.sparta_8a4daf76c5'
handler500='project.sparta_b16f09cf2c.sparta_183195ea40.qube_c0da5e02a3.sparta_0d94f66ce1'
handler403='project.sparta_b16f09cf2c.sparta_183195ea40.qube_c0da5e02a3.sparta_b110768232'
handler400='project.sparta_b16f09cf2c.sparta_183195ea40.qube_c0da5e02a3.sparta_18c0c0a649'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]