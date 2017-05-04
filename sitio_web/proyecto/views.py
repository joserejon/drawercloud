# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse
from django.conf import settings
import json
from django.contrib.auth.decorators import login_required

cliente_mongo = settings.CLIENT

#Base de datos
db = cliente_mongo['DrawerCloudDB']
#Colección
data = db.drawerclouddata


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