# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#Mostrar la página principal
@login_required(login_url='/accounts/login/')
def index(request):
	return render(request, 'index.html', {'pagina_actual':'Documentos'})

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
		'email':request.user.email, 'nombre':request.user.first_name})