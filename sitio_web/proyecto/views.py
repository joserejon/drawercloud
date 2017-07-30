# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import *
import json
import os

usuario = None
g_archivo = None

#Mostrar la página principal
@login_required(login_url='/accounts/login/')
def index(request):
	print("********************************************************")
	global usuario, g_archivo
	usuario = UsuarioForm()
	g_archivo = ArchivoForm()
	if not usuario.usuarioExiste(request.user.username):
		usuario.save(request.user.username)
	#Usuario actual
	usuario = usuario.getUsuario(request.user.username)

	return render(request, 'index.html', {'pagina_actual':'Documentos', 'usuario':usuario})

#Mostrar multimedia
@login_required(login_url='/accounts/login/')
def multimedia(request):
	return render(request, 'multimedia.html', {'pagina_actual':'Multimedia'})

#Mostrar contenido multimedia
@login_required(login_url='/accounts/login/')
def contenidoMultimedia(request):
	tipo_contenido = request.GET.get('tipo_contenido','')
	extensiones = None
	tipo_contenido_titulo = ""
	
	if tipo_contenido == "archivos_musica":
		tipo_contenido_titulo = "Música"
	elif tipo_contenido == "archivos_imagen":
		tipo_contenido_titulo = "Imágenes"
	else:
		tipo_contenido_titulo = "Vídeos"


	return render(request, 'contenidoMultimedia.html', {'pagina_actual':tipo_contenido_titulo, 'tipo_contenido':tipo_contenido})

@login_required(login_url='/accounts/login/')
def contenidoMultimediaAjax(request):
	tipo_contenido = request.GET.get('tipo_contenido','')
	g_archivo = ArchivoForm()

	if tipo_contenido == "archivos_musica":
		extensiones = ['mp3', 'wma']
	elif tipo_contenido == "archivos_imagen":
		extensiones = ['png', 'jpeg', 'jpg']
	else:
		extensiones = ['mp4', 'avi']

	archivos = g_archivo.getArchivosPorExtension(usuario.username, extensiones)
	return HttpResponse(json.dumps(archivos), content_type="application/json")

#Mostrar compartido
@login_required(login_url='/accounts/login/')
def compartido(request):
	return render(request, 'compartido.html', {'pagina_actual':'Compartido'})

#Mostrar favoritos
@login_required(login_url='/accounts/login/')
def favoritos(request):
	return render(request, 'favoritos.html', {'pagina_actual':'Favoritos'})

#Mostrar grupo de trabajo
@login_required(login_url='/accounts/login/')
def grupoTrabajo(request):
	return render(request, 'grupoTrabajo.html', {'pagina_actual':'Grupo de Trabajo'})

#Mostrar registro histórico
@login_required(login_url='/accounts/login/')
def registroHistorico(request):
	return render(request, 'registroHistorico.html', {'pagina_actual':'Registro Histórico'})

#Mostrar ayuda
@login_required(login_url='/accounts/login/')
def ayuda(request):
	return render(request, 'ayuda.html', {'pagina_actual':'Ayuda'})

#Mostrar datos usuario
@login_required(login_url='/accounts/login/')
def usuario(request):
	return render(request, 'usuario.html', {'pagina_actual':'Mi perfil', 'username':request.user.username,
		'email':request.user.email, 'nombre':request.user.first_name, 'apellidos':request.user.last_name})

#Subir un archivo
def upload(request):
	if request.method == 'POST':
		handle_uploaded_file(request.FILES['file'], request)
		return render(request, 'index.html', {'pagina_actual':'Documentos', 'usuario':usuario})

	return render(request, 'index.html', {'pagina_actual':'Documentos', 'usuario':usuario})

def handle_uploaded_file(file, request):
	if not os.path.exists('upload/'):
		os.mkdir('upload/')

	filename = str(file)
	with open('upload/' + filename, 'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)

		g_archivo.save(filename, getTipoArchivo(filename), usuario.username, 'upload/' + filename)

#Obtener la extensión de un archivo
def getTipoArchivo(nombre_archivo):

	for i, caracter in reversed(list(enumerate(nombre_archivo))):
		if caracter == '.':
			return nombre_archivo[(i+1):len(nombre_archivo)]

	return ''

#Obtener los archivos pertenecientes al usuario y mandarlos mediante Ajax
def getArchivos(request):

	archivos = g_archivo.getArchivos(usuario.username)
	
	return HttpResponse(json.dumps(archivos), content_type="application/json")

#Método para descargar un archivo
@login_required(login_url='/accounts/login/')
def descargarArchivo(request):
	id_archivo = request.GET.get('id_archivo','')
	archivo = Archivo.objects.filter(id_archivo=id_archivo)
	file = archivo[0].archivo.read()
	response = HttpResponse(file, content_type = 'application/force-download')
	response['Content-Disposition'] = 'attachment; filename=%s' % archivo[0].nombre

	return response

#Método para ver/descargar un archivo
@login_required(login_url='/accounts/login/')
def verArchivo(request):
	id_archivo = request.GET.get('id_archivo','')
	archivo = Archivo.objects.filter(id_archivo=id_archivo)
	file = archivo[0].archivo.read()
	return HttpResponse(file, content_type = archivo[0].archivo.content_type)
