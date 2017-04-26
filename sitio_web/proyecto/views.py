# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse

#Mostrar la página principal
def index(request):
	return render(request, 'index.html')

#Mostrar multimedia
def multimedia(request):
	return render(request, 'multimedia.html')

#Mostrar compartido
def compartido(request):
	return render(request, 'compartido.html')

#Mostrar favoritos
def favoritos(request):
	return render(request, 'favoritos.html')

#Mostrar grupo de trabajo
def grupoTrabajo(request):
	return render(request, 'grupoTrabajo.html')

#Mostrar registro histórico
def registroHistorico(request):
	return render(request, 'registroHistorico.html')

#Mostrar ayuda
def ayuda(request):
	return render(request, 'ayuda.html')