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

	#Comprobar si existe el usuario introducido
	def comprobarUsuarioCompartir(self, username, usuario_actual):
		usuario = Usuario.objects(username=username)

		if len(usuario) > 0:
			if usuario[0].username == usuario_actual:
				return False
			else:
				return True
		else:
			return False


################################################################
#Form para la clase Archivo
class ArchivoForm():

	#Guardar un nuevo archivo
	def save(self, nombre_archivo, tipo_archivo, username, path):
		a = Archivo()

		archivo = Archivo.objects.all()
		try:
			a.id_archivo = archivo[len(archivo) - 1].id_archivo + 1
		except:
			a.id_archivo = 1
			pass
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

	#Borrar un archivo
	def borrarArchivo(self, id_archivo):
		archivos = list(Archivo.objects.filter(id_archivo=id_archivo))
		archivos[0].archivo.delete()
		ArchivoCompartido.objects.filter(id_archivo_compartido=id_archivo).delete()
		Archivo.objects.filter(id_archivo=id_archivo).delete()

################################################################
#Form para la clase ArchivoCompartido
class ArchivoCompartidoForm(Document):

	def compartirArchivo(self, propietario, destinatario, id_archivo_compartido):
		a = ArchivoCompartido()

		try:
			a.propietario = propietario
			a.destinatario = destinatario
			a.id_archivo_compartido = id_archivo_compartido
			a.identificador_tupla = propietario + destinatario + str(id_archivo_compartido)
			a.save()
		except: 
			pass

	#Devolver una lista con los archivos compartidos
	def getArchivosCompartidos(self, username, opcion):
		archivos_dic = {}

		#Obtener archivos compartidos por mi o conmigo
		if opcion == "compartido_por_mi":
			archivos = list(ArchivoCompartido.objects.filter(propietario=username))
		else:
			archivos = list(ArchivoCompartido.objects.filter(destinatario=username))
			
		#Guardamos los archivos compartidos por o con el usuario
		for item in archivos:
			archivo = list(Archivo.objects.filter(id_archivo=int(item.id_archivo_compartido)))
			archivos_dic[int(item.id_archivo_compartido)] = [int(item.id_archivo_compartido), item.propietario, item.destinatario,
				archivo[0].nombre, archivo[0].tipo_archivo, str(archivo[0].fecha_subida), str(archivo[0].tam_archivo), 
				archivo[0].favorito]

		return archivos_dic

	#Obtener el número de usuarios que están compartiendo un archivo
	def getNumUsuariosCompartidos(self, id_archivo, username):
		archivos = list(ArchivoCompartido.objects.filter(propietario=username, id_archivo_compartido=id_archivo))

		return len(archivos)

	#Dejar de compartir un archivo
	def dejarCompartirArchivo(self, id_archivo, propietario, destino):
		ArchivoCompartido.objects.filter(id_archivo_compartido=id_archivo, propietario=propietario, destinatario=destino).delete()


################################################################
#Form para la clase GrupoTrabajo
class GrupoTrabajoForm():

	#Guardar un nuevo archivo
	def crearGrupoTrabajo(self, nombre_grupo, propietario):
		gt = GrupoTrabajo()

		grupos = GrupoTrabajo.objects.all()
		try:
			gt.id_grupo = grupos[len(grupos) - 1].id_grupo + 1
		except:
			gt.id_grupo = 1
			pass

		gt.nombre = nombre_grupo
		gt.save()
		GrupoTrabajo.objects(id_grupo=gt.id_grupo).update(add_to_set__usuarios=[propietario])

	#Obtener los grupos de trabajo donde esté el usuario
	def getGruposTrabajo(self, username):
		grupos = GrupoTrabajo.objects(usuarios__contains=username)
		grupos_dic = {}

		for item in grupos:
			grupos_dic[int(item.id_grupo)] = [int(item.id_grupo), item.nombre]

		return grupos_dic


################################################################
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