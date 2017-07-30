from django.conf.urls import url
from proyecto import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^multimedia/$', views.multimedia, name='multimedia'),
	url(r'^compartido/$', views.compartido, name='compartido'),
	url(r'^favoritos/$', views.favoritos, name='favoritos'),
	url(r'^grupoTrabajo/$', views.grupoTrabajo, name='grupoTrabajo'),
	url(r'^registroHistorico/$', views.registroHistorico, name='registroHistorico'),
	url(r'^ayuda/$', views.ayuda, name='ayuda'),
	url(r'^usuario/$', views.usuario, name='usuario'),
	url(r'^upload/', views.upload, name="upload"),
	url(r'^getArchivos/$', views.getArchivos, name='getArchivos'),
	url(r'^descargarArchivo/$', views.descargarArchivo, name='descargarArchivo'),
	url(r'^verArchivo/$', views.verArchivo, name='verArchivo'),
]