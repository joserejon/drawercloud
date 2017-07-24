# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import *
import json
import os

usuario = None

#Mostrar la página principal
@login_required(login_url='/accounts/login/')
def index(request):
	global usuario
	usuario = UsuarioForm()
	if not usuario.usuarioExiste(request.user.username):
		usuario.save(request.user.username)
	#Usuario actual
	usuario = usuario.getUsuario(request.user.username)

	return render(request, 'index.html', {'pagina_actual':'Documentos', 'usuario':usuario})

#Mostrar multimedia
@login_required(login_url='/accounts/login/')
def multimedia(request):
	return render(request, 'multimedia.html', {'pagina_actual':'Multimedia'})

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

#Mostrar ayuda
@login_required(login_url='/accounts/login/')
def usuario(request):
	return render(request, 'usuario.html', {'pagina_actual':'Mi perfil', 'username':request.user.username,
		'email':request.user.email, 'nombre':request.user.first_name, 'apellidos':request.user.last_name})

#Subir un archivo
def subidaArchivo(request):
	global usuario
	usuario.getUsuario(request.user.username)

	nombre_archivo = request.GET.get('filename', '')
	archivo = ArchivoForm()
	archivo.save(nombre_archivo, getTipoArchivo(nombre_archivo), usuario)

	return HttpResponse(json.dumps(nombre_archivo + " subido"), content_type="application/json")


def upload(request):
	if request.method == 'POST':
		handle_uploaded_file(request.FILES['file'], str(request.FILES['file']), request)
		return render(request, 'index.html', {'pagina_actual':'Documentos'})

	return render(request, 'index.html', {'pagina_actual':'Documentos'})

def handle_uploaded_file(file, filename, request):
	if not os.path.exists('upload/'):
		os.mkdir('upload/')

	with open('upload/' + filename, 'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)

		archivo = ArchivoForm()
		archivo.save(filename, getTipoArchivo(filename), usuario, 'upload/' + filename)



#Obtener la extensión de un archivo
def getTipoArchivo(nombre_archivo):

	for i, caracter in reversed(list(enumerate(nombre_archivo))):
		if caracter == '.':
			return nombre_archivo[(i+1):len(nombre_archivo)]

	return ''