# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from igraph import *

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
	g = Graph(directed=True)
	g.add_vertices(4)
	g.add_edges([(0,1), (0,2), (3,0)])
	names = {"Jose": "red", "Juan":"#72A7CF", "Pepe":"#72A7CF", "Manu":"#72A7CF"}
	g.vs["name"] = ["Jose", "Juan", "Pepe", "Manu"]
	layout = g.layout("fr")
	visual_style = {}
	visual_style["vertex_color"] = [names[name] for name in g.vs["name"]]
	#visual_style["vertex_color"] = "#72A7CF"
	visual_style["vertex_size"] = 30
	visual_style["edge_arrow_size"] = 1
	visual_style["vertex_label"] = g.vs["name"]
	plot(g, "proyecto/static/images/grafo.png", **visual_style)
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
	return render(request, 'usuario.html', {'pagina_actual':'Mi perfil'})