from django import forms
from mongoengine import *
from requests import *
import datetime
from .models import *

#Form para la clase Usuario
class UsuarioForm():

	#Guardar un nuevo usuario
	def save(self, _username):
		u = Usuario()

		u.username = _username
		u.id_username = Usuario.objects.count() + 1
		u.mis_directorios = []
		u.mis_archivos = []
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
	def save(self, nombre_archivo, tipo_archivo, usuario, path):
		a = Archivo()

		a.id_archivo = Archivo.objects.count() + 1
		a.nombre = nombre_archivo
		a.tipo_archivo = tipo_archivo
		data = open(path, 'wb+')
		a.archivo.put(data)
		a.fecha_subida = a.archivo.uploadDate
		a.save()
		#Actualizar la bd para el usuario
		usuario.mis_archivos.append(a.id_archivo)
		usuario.update(mis_archivos=usuario.mis_archivos)