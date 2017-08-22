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
@login_required(login_url='/accounts/login/')
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
@login_required(login_url='/accounts/login/')
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

#Añadir a favoritos
@login_required(login_url='/accounts/login/')
def addFavoritos(request):
	id_archivo = request.GET.get('id_archivo','')
	pag_actual = request.GET.get('pag_actual','')
	g_archivo.addFavoritos(id_archivo)

	#Si es llamado desde la página contenidoMultimedia.html
	if pag_actual == "contenidoMultimedia.html":
		tipo_contenido = request.GET.get('tipo_contenido','')
		tipo_contenido_titulo = ""
		
		if tipo_contenido == "archivos_musica":
			tipo_contenido_titulo = "Música"
		elif tipo_contenido == "archivos_imagen":
			tipo_contenido_titulo = "Imágenes"
		else:
			tipo_contenido_titulo = "Vídeos"

		return render(request, 'contenidoMultimedia.html', {'pagina_actual':tipo_contenido_titulo, 'tipo_contenido':tipo_contenido})
	#Si es llamado desde la página index.html
	elif pag_actual == "index.html":
		return render(request, "index.html", {'pagina_actual':'Documentos', 'usuario':usuario})
	#Si es llamado desde la página favoritos.html
	elif pag_actual == "favoritos.html":
		return render(request, "favoritos.html", {'pagina_actual':'Favoritos', 'usuario':usuario})
	#Si es llamado desde la página compartido.html
	elif pag_actual == "compartido.html":
		return render(request, "compartido.html", {'pagina_actual':'Compartido', 'usuario':usuario})

#Eliminar de favoritos
@login_required(login_url='/accounts/login/')
def delFavoritos(request):
	id_archivo = request.GET.get('id_archivo','')
	pag_actual = request.GET.get('pag_actual','')
	g_archivo.delFavoritos(id_archivo)

	#Si es llamado desde la página contenidoMultimedia.html
	if pag_actual == "contenidoMultimedia.html":
		tipo_contenido = request.GET.get('tipo_contenido','')
		tipo_contenido_titulo = ""
		
		if tipo_contenido == "archivos_musica":
			tipo_contenido_titulo = "Música"
		elif tipo_contenido == "archivos_imagen":
			tipo_contenido_titulo = "Imágenes"
		else:
			tipo_contenido_titulo = "Vídeos"

		return render(request, 'contenidoMultimedia.html', {'pagina_actual':tipo_contenido_titulo, 'tipo_contenido':tipo_contenido})
	#Si es llamado desde la página index.html
	elif pag_actual == "index.html":
		return render(request, "index.html", {'pagina_actual':'Documentos', 'usuario':usuario})
	#Si es llamado desde la página favoritos.html
	elif pag_actual == "favoritos.html":
		return render(request, "favoritos.html", {'pagina_actual':'Favoritos', 'usuario':usuario})
	#Si es llamado desde la página compartido.html
	elif pag_actual == "compartido.html":
		return render(request, "compartido.html", {'pagina_actual':'Compartido', 'usuario':usuario})

#Obtener los archivos pertenecientes al usuario y mandarlos mediante Ajax
@login_required(login_url='/accounts/login/')
def getArchivosFavoritos(request):

	archivos = g_archivo.getArchivosFavoritos(usuario.username)
	
	return HttpResponse(json.dumps(archivos), content_type="application/json")

#Compartir un archivo
@login_required(login_url='/accounts/login/')
def compartirArchivo(request):
	id_archivo = request.GET.get('id_archivo_compartir','')
	pag_actual = request.GET.get('pag_actual','')
	username_destino = request.GET.get('username_destino','')
	archivo_compartido = ArchivoCompartidoForm()
	archivo_compartido.compartirArchivo(usuario.username, username_destino, id_archivo)

	#Si es llamado desde la página contenidoMultimedia.html
	if pag_actual == "contenidoMultimedia.html":
		tipo_contenido = request.GET.get('tipo_contenido','')
		tipo_contenido_titulo = ""
		
		if tipo_contenido == "archivos_musica":
			tipo_contenido_titulo = "Música"
		elif tipo_contenido == "archivos_imagen":
			tipo_contenido_titulo = "Imágenes"
		else:
			tipo_contenido_titulo = "Vídeos"

		return render(request, 'contenidoMultimedia.html', {'pagina_actual':tipo_contenido_titulo, 'tipo_contenido':tipo_contenido})
	#Si es llamado desde la página index.html
	elif pag_actual == "index.html":
		return render(request, "index.html", {'pagina_actual':'Documentos', 'usuario':usuario})
	#Si es llamado desde la página favoritos.html
	else:
		return render(request, "favoritos.html", {'pagina_actual':'Favoritos', 'usuario':usuario})

#Obtener los archivos compartidos por el usuario o con el usuario (según opción)
@login_required(login_url='/accounts/login/')
def getArchivosCompartidos(request):
	opcion = request.GET.get('opcion','')
	archivo_compartido = ArchivoCompartidoForm()
	archivos = archivo_compartido.getArchivosCompartidos(usuario.username, opcion)
	
	return HttpResponse(json.dumps(archivos), content_type="application/json")

#Borrar un archivo
@login_required(login_url='/accounts/login/')
def borrarArchivo(request):
	id_archivo = request.GET.get('id_archivo','')
	pag_actual = request.GET.get('pag_actual','')

	if pag_actual == "index.html":
		g_archivo.borrarArchivo(id_archivo)
		return render(request, "index.html", {'pagina_actual':'Documentos', 'usuario':usuario})
	elif pag_actual == "grupoTrabajo.html":
		id_grupo = request.GET.get('id_grupo','')
		gt = GrupoTrabajoForm()
		gt.borrarArchivo(id_archivo, id_grupo)
		return render(request, "grupoTrabajo.html", {'pagina_actual':'Grupo de Trabajo'})


#Comprobar si existe el usuario introducido
@login_required(login_url='/accounts/login/')
def comprobarUsuarioCompartir(request):
	username = request.GET.get('username','')
	u = UsuarioForm()
	resultado = u.comprobarUsuarioCompartir(username, usuario.username)

	return HttpResponse(json.dumps(resultado), content_type="application/json")

#Dejar de compartir un archivo
@login_required(login_url='/accounts/login/')
def dejarCompartirArchivo(request):
	id_archivo = request.GET.get('id_archivo', '')
	propietario = request.GET.get('username_propietario', '')
	destino = request.GET.get('username_destino', '')

	archivo_compartido = ArchivoCompartidoForm()
	archivo_compartido.dejarCompartirArchivo(id_archivo, propietario, destino)

	return render(request, 'compartido.html', {'pagina_actual':'Compartido'})

#Crear un grupo de trabajo
@login_required(login_url='/accounts/login/')
def crearGrupoTrabajo(request):
	nombre_grupo = request.GET.get('nombre_grupo', '')

	grupo = GrupoTrabajoForm()
	grupo.crearGrupoTrabajo(nombre_grupo, usuario.username)

	return render(request, 'grupoTrabajo.html', {'pagina_actual':'Grupo de Trabajo'})

#Obtener los grupos de trabajo
@login_required(login_url='/accounts/login/')
def getGruposTrabajo(request):

	grupo = GrupoTrabajoForm()
	grupos = grupo.getGruposTrabajo(usuario.username)

	return HttpResponse(json.dumps(grupos), content_type="application/json")

#Comprobar si existe el usuario introducido
@login_required(login_url='/accounts/login/')
def comprobarParticipante(request):
	id_grupo = request.GET.get('id_grupo','')
	participante = request.GET.get('participante','')
	gt = GrupoTrabajoForm()
	resultado = gt.comprobarParticipante(id_grupo, participante)

	return HttpResponse(json.dumps(resultado), content_type="application/json")

#Añadir un participante al grupo
@login_required(login_url='/accounts/login/')
def addParticipante(request):
	id_grupo = request.GET.get('id_grupo','')
	participante = request.GET.get('participante','')
	gt = GrupoTrabajoForm()
	gt.addParticipante(id_grupo, participante)

	return render(request, 'grupoTrabajo.html', {'pagina_actual':'Grupo de Trabajo'})

#Obtener los archivos de un grupo de trabajo
@login_required(login_url='/accounts/login/')
def getArchivosGrupoTrabajo(request):
	id_grupo = request.GET.get('id_grupo','')
	gt = GrupoTrabajoForm()
	resultado = gt.getArchivosGrupoTrabajo(id_grupo)

	return HttpResponse(json.dumps(resultado), content_type="application/json")

#Subir un archivo a un grupo
@login_required(login_url='/accounts/login/')
def subirArchivoGrupo(request):
	if request.method == 'POST':
		id_grupo = request.POST.get('id_grupo_upload','')
		handle_uploaded_file(request.FILES['file'], request, id_grupo)
		return render(request, 'grupoTrabajo.html', {'pagina_actual':'Grupo de Trabajo'})

	return render(request, 'index.html', {'pagina_actual':'Documentos', 'usuario':usuario})

def handle_uploaded_file(file, request, id_grupo):
	if not os.path.exists('upload/'):
		os.mkdir('upload/')

	gt = GrupoTrabajoForm()		
	filename = str(file)
	with open('upload/' + filename, 'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)

		gt.subirArchivoGrupo(id_grupo, filename, getTipoArchivo(filename), 'upload/' + filename)

#Obtener los participantes de un grupo
@login_required(login_url='/accounts/login/')
def getParticipantes(request):
	id_grupo = request.GET.get('id_grupo', '')
	gt = GrupoTrabajoForm()
	resultado = gt.getParticipantes(id_grupo)

	return HttpResponse(json.dumps(resultado), content_type="application/json")