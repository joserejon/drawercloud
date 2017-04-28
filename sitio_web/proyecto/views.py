# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse


#import pickle

#Variables globales
modo_vista = ""

#Función para obtener la vista seleccionada (lista/cuadricula)
#def getVista():
#	global modo_vista
#
#	with open("proyecto/config.dat", "rb") as f:
#		d = pickle.load(f)
#		modo_vista = d['modo_vista']
#
#	return modo_vista

#Mostrar la página principal
def index(request):
	global modo_vista
	
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