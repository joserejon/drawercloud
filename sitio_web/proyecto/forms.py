from django import forms
from mongoengine import *
from requests import *
import datetime
from .models import *
from django.forms.models import model_to_dict
import json
import datetime

#Form para la clase Usuario
class UsuarioForm():

	#Guardar un nuevo usuario
	def save(self, _username):
		u = Usuario()

		u.username = _username
		u.id_username = Usuario.objects.count() + 1
		u.compartido_por_mi = []
		u.compartido_conmigo = []

		u.save()

		return u

	#Comprobar si el usuario existe
	def usuarioExiste(self, _username):
		user = Usuario.objects(username=_username)
		if len(user) == 0:
			return False
		return True

	#Devuelve el usuario actual
	def getUsuario(self, _username):
		u = Usuario()
		datos_usuario = Usuario.objects(username=_username)

		return datos_usuario[0]

#Form para la clase Archivo
class ArchivoForm():

	#Guardar un nuevo archivo
	def save(self, nombre_archivo, tipo_archivo, username, path):
		a = Archivo()

		a.id_archivo = Archivo.objects.count() + 1
		a.nombre = nombre_archivo
		a.tipo_archivo = tipo_archivo
		data = open(path, 'wb+')
		a.archivo.put(data)
		a.fecha_subida = str(datetime.datetime.now())
		a.propietario = username
		a.save()

	#Devolver una lista con los archivos del usuario
	def getArchivos(self, username):

		archivos = list(Archivo.objects.filter(propietario=username))
		archivos_dic = {}

		for item in archivos:
			archivos_dic[int(item.id_archivo)] = [int(item.id_archivo), item.nombre, item.tipo_archivo, str(item.fecha_subida)]


		print archivos_dic
		return archivos_dic