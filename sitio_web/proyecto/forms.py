# -*- coding: utf-8 -*-

from django import forms
from mongoengine import *
import datetime
from .models import *

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
		a.fecha_subida = str(datetime.datetime.now().replace(microsecond=0))
		a.propietario = username
		data = open(path, 'rb')
		ct = getContentType(tipo_archivo)
		a.archivo.put(data, content_type = ct)
		a.tam_archivo = a.archivo.length
		a.favorito = False
		a.save()

	#Devolver una lista con los archivos del usuario
	def getArchivos(self, username):

		archivos = list(Archivo.objects.filter(propietario=username))
		archivos_dic = {}

		for item in archivos:
			archivos_dic[int(item.id_archivo)] = [int(item.id_archivo), item.nombre, item.tipo_archivo, 
			str(item.fecha_subida), str(item.tam_archivo), item.favorito]

		return archivos_dic

	#Devolver una lista con los archivos del usuario buscando por extension
	def getArchivosPorExtension(self, username, extension):

		archivos = list(Archivo.objects.filter(propietario=username, tipo_archivo__in=extension))
		archivos_dic = {}

		for item in archivos:
			archivos_dic[int(item.id_archivo)] = [int(item.id_archivo), item.nombre, item.tipo_archivo,
			str(item.fecha_subida), str(item.tam_archivo), item.favorito]

		return archivos_dic

	#Añadir un archivo a favoritos
	def addFavoritos(self, id_archivo):
		Archivo.objects(id_archivo=id_archivo).update_one(set__favorito=True)

	#Eliminar un archivo de favoritos
	def delFavoritos(self, id_archivo):
		Archivo.objects(id_archivo=id_archivo).update_one(set__favorito=False)	

	#Devolver una lista con los archivos favoritos del usuario
	def getArchivosFavoritos(self, username):
		archivos = list(Archivo.objects.filter(propietario=username, favorito=True))
		archivos_dic = {}

		for item in archivos:
			archivos_dic[int(item.id_archivo)] = [int(item.id_archivo), item.nombre, item.tipo_archivo,
			str(item.fecha_subida), str(item.tam_archivo), item.favorito]

		return archivos_dic

	#Compartir un archivo
	def compartirArchivo(self, username, username_destino, id_archivo):
		#Copiar archivo para el usuario de destino
		#archivo_a_compartir = Archivo.objects(id_archivo=id_archivo)
		#self.save(archivo_a_compartir[0].nombre, archivo_a_compartir[0].tipo_archivo, username_destino, 'upload/' + archivo_a_compartir[0].nombre)

		#Actualizar los vectores de archivos compartidos en los usuarios involucrados
		Usuario.objects(username=username).update_one(compartido_por_mi=[id_archivo])
		Usuario.objects(username=username_destino).update_one(compartido_conmigo=[id_archivo])

	#Devolver una lista con los archivos compartidos
	def getArchivosCompartidos(self, username, opcion):
		usuario = Usuario.objects(username=username)
		archivos = []
		archivos_dic = {}
		datos = None

		#Obtener archivos compartidos por mi o conmigo
		if opcion == "compartido_por_mi":
			datos = usuario[0].compartido_por_mi
		else:
			datos = usuario[0].compartido_conmigo

		for id_archivo in datos:
			archivos += list(Archivo.objects.filter(id_archivo=id_archivo))

		for item in archivos:
			archivos_dic[int(item.id_archivo)] = [int(item.id_archivo), item.nombre, item.tipo_archivo,
			str(item.fecha_subida), str(item.tam_archivo), item.favorito]

		print "*++++++++++++++++++++++++++++++++++++++"
		print archivos_dic
		print len(archivos_dic)
		print username
		print opcion
		print "*++++++++++++++++++++++++++++++++++++++"
		return archivos_dic


def getContentType(tipo_archivo):
	ct = ""
	if tipo_archivo == 'odt':
		ct = 'application/vnd.oasis.opendocument.text'
	elif tipo_archivo == 'jpeg' or tipo_archivo == 'jpg':
		ct = 'image/jpeg'
	elif tipo_archivo == 'mp3':
		ct = 'audio/mpeg'
	elif tipo_archivo == 'txt':
		ct = 'text/plain'
	elif tipo_archivo == 'pdf':
		ct = 'application/pdf'
	else:
		ct = 'application/octet-stream'

	return ct