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
	url(r'^contenidoMultimedia/$', views.contenidoMultimedia, name='contenidoMultimedia'),
	url(r'^contenidoMultimediaAjax/$', views.contenidoMultimediaAjax, name='contenidoMultimediaAjax'),
	url(r'^addFavoritos/$', views.addFavoritos, name='addFavoritos'),
	url(r'^getArchivosFavoritos/$', views.getArchivosFavoritos, name='getArchivosFavoritos'),
	url(r'^delFavoritos/$', views.delFavoritos, name='delFavoritos'),
	url(r'^compartirArchivo/$', views.compartirArchivo, name='compartirArchivo'),
	url(r'^getArchivosCompartidos/$', views.getArchivosCompartidos, name='getArchivosCompartidos'),
	url(r'^borrarArchivo/$', views.borrarArchivo, name='borrarArchivo'),
	url(r'^comprobarUsuarioCompartir/$', views.comprobarUsuarioCompartir, name='comprobarUsuarioCompartir'),
	url(r'^dejarCompartirArchivo/$', views.dejarCompartirArchivo, name='dejarCompartirArchivo'),
	url(r'^crearGrupoTrabajo/$', views.crearGrupoTrabajo, name='crearGrupoTrabajo'),
	url(r'^getGruposTrabajo/$', views.getGruposTrabajo, name='getGruposTrabajo'),
]