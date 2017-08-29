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
		u.img_perfil = -1

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
	# 0 == no existe; -1 == es el propio usuario; 1 == éxito
	def comprobarUsuarioCompartir(self, username, usuario_actual):
		usuario = Usuario.objects(username=username)

		if len(usuario) > 0:
			if usuario[0].username == usuario_actual:
				return -1
			else:
				return 1
		else:
			return 0

	#Cargar la imagen de perfil
	def cargarImgPerfil(self, nombre_archivo, tipo_archivo, username, path):
		a = ArchivoForm()
		#Subir el archivo a la base de datos
		id_archivo = a.save(nombre_archivo, tipo_archivo, "", path, 0)
		#Añadir fichero al grupo de trabajo
		Usuario.objects(username=username).update(set__img_perfil=id_archivo)

	#Obtener la imagen de perfil
	def getImgPerfil(self, username):
		usuario = Usuario.objects(username=username)
		nombre_img_perfil = ""

		if usuario[0].img_perfil >= 0:
			a = ArchivoForm()
			nombre_img_perfil = "/static/images/" + a.getNombreArchivo(usuario[0].img_perfil)
		else:
			nombre_img_perfil = "/static/images/img_perfil.png"

		return nombre_img_perfil

	#Obtener el espacio ocupado por los archivos del usuario
	def getEspacioOcupado(self, username):
		mis_archivos = Archivo.objects(propietario=username)

		espacio_ocupado = 0
		for archivo in mis_archivos:
			espacio_ocupado += archivo.tam_archivo

		mis_grupos = GrupoTrabajo.objects(usuarios__contains=username)
		for grupo in mis_grupos:
			for id_archivo in grupo.archivos:
				archivo = Archivo.objects(id_archivo=id_archivo)[0]
				espacio_ocupado += archivo.tam_archivo

		return float(espacio_ocupado)

	#Eliminar la cuenta de usuario
	def eliminarCuenta(self, username):

		#Eliminar los directorios y sus archivos desde la raíz
		d = DirectorioForm()
		d.borrarDirectorio(0, username)

		#Eliminar usuario de los grupos de trabajo
		gt = GrupoTrabajoForm()
		mis_grupos = GrupoTrabajo.objects(usuarios__contains=username)
		for grupo in mis_grupos:
			gt.salirGrupo(username, grupo.id_grupo)

		#Eliminar el usuario
		Usuario.objects(username=username).delete()


################################################################
#Form para la clase Directorio
class DirectorioForm():

	#Crear el directorio raíz
	def crearDirectorioRaiz(self, propietario):
		d = Directorio()

		d.id_directorio = 0
		d.nombre = "Documentos"
		d.id_padre = -1
		d.propietario = propietario
		d.identificador_tupla = propietario + str(d.id_directorio)
		d.save()

		return d

	#Comprobar si existe el directorio raíz
	def comprobarExisteDirectorioRaiz(self, propietario):
		directorio = Directorio.objects(id_directorio=0, propietario=propietario)
		if len(directorio) == 0:
			self.crearDirectorioRaiz(propietario)

	#Comprobar si existe el directorio a crear
	def comprobarExisteDirectorio(self, nombre_directorio, directorio_actual, propietario):
		directorio = list(Directorio.objects.filter(id_directorio=directorio_actual, propietario=propietario))

		#Recorrer el contenido para directorio_actual
		for contenido in directorio[0].contenido:
			#Escoger la tupla que es directorio
			if contenido[1] == "directorio":
				#Comprobar, con el id del directorio, su nombre
				d = Directorio.objects(id_directorio=contenido[0])
				if d[0].nombre == nombre_directorio:
					return True

		return False


	#Crear un nuevo directorio
	def crearDirectorio(self, nombre_directorio, id_padre, propietario):
		d = Directorio()

		directorio = Directorio.objects(propietario=propietario)
		d.id_directorio = directorio[len(directorio) - 1].id_directorio + 1

		d.nombre = nombre_directorio
		d.id_padre = id_padre
		d.propietario = propietario
		d.identificador_tupla = propietario + str(d.id_directorio)

		contenido = (int(d.id_directorio), 'directorio')
		self.actualizarContenidoDirectorio(id_padre, contenido, propietario)
		d.save()

		return d

	#Actualizar contenido de un directorio
	#nuevo contenido -> tupla con la forma ( id_contenido , tipo_contenido )
	#tipo contenido indica si es directorio o archivo
	def actualizarContenidoDirectorio(self, id_directorio, nuevo_contenido, propietario):
		Directorio.objects(id_directorio=id_directorio, propietario=propietario).update(add_to_set__contenido=[nuevo_contenido])

	#Obtener los directorios del usuario posibles para mover un archivo
	def getDirectoriosMoverArchivo(self, propietario, directorio_actual):
		directorios = list(Directorio.objects.filter(propietario=propietario))
		directorios_dic = {}

		for directorio in directorios:
			#Cuando el directorio sea distinto del actual
			if int(directorio.id_directorio) != int(directorio_actual):
				path = directorio.nombre
				directorio_aux = directorio
				#Recorremos los padres del directorio para añadirlos al path
				while directorio_aux.id_padre >= 0:
					directorio_aux = Directorio.objects(id_directorio=directorio_aux.id_padre, propietario=propietario)
					directorio_aux = directorio_aux[0]
					path = directorio_aux.nombre + "/" + path
				
				#Añadir al diccionario el id_directorio y el path
				directorios_dic[int(directorio.id_directorio)] = [int(directorio.id_directorio), path]

		return directorios_dic

	#Obtener los directorios del usuario posibles para mover un directorio
	def getDirectoriosMoverDirectorio(self, propietario, directorio_actual, directorio_seleccionado):
		directorios = list(Directorio.objects.filter(propietario=propietario))
		directorios_dic = {}

		for directorio in directorios:
			#Cuando el directorio sea distinto del actual
			if int(directorio.id_directorio) != int(directorio_actual) and int(directorio.id_directorio) != int(directorio_seleccionado):
				path = directorio.nombre
				directorio_aux = directorio
				#Recorremos los padres del directorio para añadirlos al path
				while directorio_aux.id_padre >= 0:
					directorio_aux = Directorio.objects(id_directorio=directorio_aux.id_padre, propietario=propietario)
					directorio_aux = directorio_aux[0]
					path = directorio_aux.nombre + "/" + path
				
				#Añadir al diccionario el id_directorio y el path
				directorios_dic[int(directorio.id_directorio)] = [int(directorio.id_directorio), path]

		return directorios_dic

	#Mover un archivo a otro directorio
	def moverArchivo(self, id_archivo_mover, directorio_actual, id_directorio_dest, propietario):
		directorio = list(Directorio.objects.filter(id_directorio=directorio_actual, propietario=propietario))

		#Eliminar el archivo del directorio actual
		contador = 0
		#Recorrer el contenido para directorio_actual
		for contenido in directorio[0].contenido:
			#Escoger la tupla que es archivo
			if contenido[1] == "archivo" and contenido[0] == int(id_archivo_mover):
				del directorio[0].contenido[contador]
				directorio[0].save()
				break

			contador += 1

		#Añadir el archivo a su nuevo directorio
		contenido = (int(id_archivo_mover), 'archivo')
		self.actualizarContenidoDirectorio(id_directorio_dest, contenido, propietario)

	#Mover un directorio
	def moverDirectorio(self, id_directorio_mover, id_directorio_destino, propietario, directorio_actual):
		directorio = list(Directorio.objects.filter(id_directorio=directorio_actual, propietario=propietario))
		#Eliminar directorio del directorio actual
		contador = 0
		#Recorrer el contenido para directorio_actual
		for contenido in directorio[0].contenido:
			#Escoger la tupla que es directorio
			if contenido[1] == "directorio" and contenido[0] == int(id_directorio_mover):
				del directorio[0].contenido[contador]
				directorio[0].save()
				break

			contador += 1
		#Añadir directorio al directorio destino
		contenido = (int(id_directorio_mover), 'directorio')
		self.actualizarContenidoDirectorio(id_directorio_destino, contenido, propietario)
		#Actualizar directorio padre
		#Directorio.objects(id_directorio=id_directorio_mover, propietario=propietario).update_one(set__id_padre=id_directorio_destino)

	#Obtener los directorios del usuario posibles para copiar un archivo
	def getDirectoriosCopiar(self, propietario):
		directorios = list(Directorio.objects.filter(propietario=propietario))
		directorios_dic = {}

		for directorio in directorios:
			path = directorio.nombre
			directorio_aux = directorio
			#Recorremos los padres del directorio para añadirlos al path
			while directorio_aux.id_padre >= 0:
				directorio_aux = Directorio.objects(id_directorio=directorio_aux.id_padre, propietario=propietario)
				directorio_aux = directorio_aux[0]
				path = directorio_aux.nombre + "/" + path
			
			#Añadir al diccionario el id_directorio y el path
			directorios_dic[int(directorio.id_directorio)] = [int(directorio.id_directorio), path]

		return directorios_dic

	#Copiar un archivo
	def copiarArchivo(self, id_archivo_copiar, directorio_actual, id_directorio_dest, propietario):
		archivo_original = Archivo.objects(id_archivo=id_archivo_copiar)
		archivo_original = archivo_original[0]
		a = ArchivoForm()

		#Añadir "copia" al nombre si se copia en el mismo directorios
		nombre_archivo = ""
		if int(directorio_actual) != int(id_directorio_dest):
			nombre_archivo = archivo_original.nombre
		else:
			nombre_archivo = "copia " + archivo_original.nombre

		#Crear copia física del archivo
		file = open('upload/' + archivo_original.nombre, 'rb+')
		with open('upload/' + nombre_archivo, 'wb+') as destination:
			while True:
			    piece = file.read(1024)  
			    if not piece:
			        break
			    destination.write(piece)
			file.close()

		#Crear copia en la BD
		a.save(nombre_archivo, archivo_original.tipo_archivo, propietario, 'upload/' + archivo_original.nombre, id_directorio_dest)

	#Copiar un directorio
	def copiarDirectorio(self, id_directorio_copiar, id_directorio_destino, propietario, directorio_actual):
		directorios = Directorio.objects(propietario=propietario).order_by('id_directorio')
		directorio_original = Directorio.objects(id_directorio=id_directorio_copiar, propietario=propietario)
		directorio_nuevo = Directorio()

		directorio_nuevo.id_directorio = directorios[len(directorios) - 1].id_directorio + 1
		directorio_nuevo.identificador_tupla = propietario + str(directorio_nuevo.id_directorio)
		directorio_nuevo.id_padre = id_directorio_destino
		directorio_nuevo.propietario = propietario
		if int(directorio_actual) == int(id_directorio_destino):
			directorio_nuevo.nombre = "copia " + directorio_original[0].nombre
		else:
			directorio_nuevo.nombre = directorio_original[0].nombre

		directorio_nuevo.contenido = directorio_original[0].contenido

		for contenido in directorio_original[0].contenido:
			if contenido[1] == "archivo":
				self.copiarArchivo(int(contenido[0]), directorio_actual, directorio_nuevo.id_directorio, propietario)

		contenido = (int(directorio_nuevo.id_directorio), 'directorio')
		self.actualizarContenidoDirectorio(id_directorio_destino, contenido, propietario)
		directorio_nuevo.save()

	#Borrar un directorio
	def borrarDirectorio(self, id_directorio_eliminar, propietario):
		directorio = Directorio.objects(id_directorio=id_directorio_eliminar, propietario=propietario)[0]
		a = ArchivoForm()

		#Borrar contenido del directorio a eliminar
		for contenido in directorio.contenido:
			if contenido[1] == "archivo":
				a.borrarArchivo(contenido[0], id_directorio_eliminar, propietario)
			elif contenido[1] == "directorio":
				self.borrarDirectorio(contenido[0], propietario)


		#Borrar directorio del contenido del padre
		if directorio.id_padre != -1:
			directorio_padre = Directorio.objects(id_directorio=directorio.id_padre, propietario=propietario)[0]
			contador = 0
			for contenido in directorio_padre.contenido:
				#Escoger la tupla que es directorio
				if contenido[1] == "directorio" and contenido[0] == int(id_directorio_eliminar):
					del directorio_padre.contenido[contador]
					directorio_padre.save()
					break

				contador += 1

		#Borrar la tupla en la BD correspondiente al directorio
		Directorio.objects(id_directorio=id_directorio_eliminar, propietario=propietario).delete()

	#Cambiar nombre a un directorio/archivo
	def cambiarNombre(self, nuevo_nombre, id_contenido_cambiar_nombre, directorio_actual, tipo_contenido, propietario):

		#Si se está cambiando el nombre desde la página principal
		if int(directorio_actual) >= 0:
			directorio = Directorio.objects(id_directorio=directorio_actual, propietario=propietario)[0]
			for contenido in directorio.contenido:
				if contenido[0] == int(id_contenido_cambiar_nombre) and contenido[1] == tipo_contenido:
					if tipo_contenido == "archivo":
						Archivo.objects(id_archivo=id_contenido_cambiar_nombre).update_one(set__nombre=nuevo_nombre)
					else:
						Directorio.objects(id_directorio=id_contenido_cambiar_nombre).update_one(set__nombre=nuevo_nombre)
					break
		else:
			Archivo.objects(id_archivo=id_contenido_cambiar_nombre).update_one(set__nombre=nuevo_nombre)

	#Obtener los datos del breadcrumb
	def actualizarBreadcrumb(self, id_directorio, propietario):
		directorio = Directorio.objects(id_directorio=id_directorio, propietario=propietario)[0]
		directorios_dic = {}

		directorios_dic[int(directorio.id_directorio)] = [int(directorio.id_directorio), directorio.nombre]
		while directorio.id_padre != -1:
			directorio = Directorio.objects(id_directorio=directorio.id_padre, propietario=propietario)[0]
			directorios_dic[int(directorio.id_directorio)] = [int(directorio.id_directorio), directorio.nombre]
		
		return directorios_dic


################################################################
#Form para la clase Archivo
class ArchivoForm():

	#Guardar un nuevo archivo
	def save(self, nombre_archivo, tipo_archivo, username, path, id_directorio):
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

		d = DirectorioForm()
		contenido = (int(a.id_archivo), 'archivo')
		d.actualizarContenidoDirectorio(id_directorio, contenido, username)

		return a.id_archivo

	#Devolver una lista con los archivos del usuario
	def getArchivos(self, username, id_directorio):
		archivos_dic = {}
		subdirectorios_dic = {}
		directorio = list(Directorio.objects.filter(id_directorio=id_directorio, propietario=username))

		#Recorrer el contenido para directorio_actual
		for contenido in directorio[0].contenido:
			#Escoger la tupla que es archivo
			if contenido[1] == "archivo":
				archivo = Archivo.objects(id_archivo=contenido[0])
				archivo = archivo[0]
				archivos_dic[int(archivo.id_archivo)] = [int(archivo.id_archivo), archivo.nombre, archivo.tipo_archivo, 
				str(archivo.fecha_subida), str(archivo.tam_archivo), archivo.favorito]
			else:
				subdirectorio = Directorio.objects(id_directorio=contenido[0])
				subdirectorio = subdirectorio[0]

				subdirectorios_dic[int(subdirectorio.id_directorio)] = [int(subdirectorio.id_directorio), subdirectorio.nombre]

		contenido = (subdirectorios_dic, archivos_dic)

		return contenido

	def getNombreArchivo(self, id_archivo):
		archivo = list(Archivo.objects.filter(id_archivo=id_archivo))

		return archivo[0].nombre

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
	def borrarArchivo(self, id_archivo, id_directorio, propietario):
		archivos = list(Archivo.objects.filter(id_archivo=id_archivo))
		archivos[0].archivo.delete()
		ArchivoCompartido.objects.filter(id_archivo_compartido=id_archivo).delete()
		Archivo.objects.filter(id_archivo=id_archivo).delete()
		contenido = (id_archivo, 'archivo')
		directorio = list(Directorio.objects.filter(id_directorio=id_directorio, propietario=propietario))

		contador = 0
		#Recorrer el contenido para directorio_actual
		for contenido in directorio[0].contenido:
			#Escoger la tupla que es directorio
			if contenido[1] == "archivo" and contenido[0] == int(id_archivo):
				del directorio[0].contenido[contador]
				directorio[0].save()
				break

			contador += 1


################################################################
#Form para la clase ArchivoCompartido
class ArchivoCompartidoForm(Document):

	#Compartir un archivo
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

	#Comprobar si existe el usuario- y no pertenece ya al grupo
	# 0 == no existe; -1 == el usuario ya forma parte del grupo; 1 == éxito
	def comprobarParticipante(self, id_grupo, participante):
		participantes = GrupoTrabajo.objects(usuarios__contains=participante)

		if len(participantes) > 0:
			return -1
		else:
			usuario = Usuario.objects(username=participante)
			if len(usuario) > 0:
				return 1
			else:
				return 0

	#Añadir un participante al grupo
	def addParticipante(self, id_grupo, participante):
		GrupoTrabajo.objects(id_grupo=id_grupo).update(add_to_set__usuarios=[participante])

	#Obtener los archivos de un grupo de trabajo
	def getArchivosGrupoTrabajo(self, id_grupo):
		grupo = list(GrupoTrabajo.objects.filter(id_grupo=id_grupo))
		archivos_dic = {}

		#Almacenar los archivos del grupo X en un diccionario
		for id_archivo in grupo[0].archivos:
			#Obtener el archivo por ID
			archivo = Archivo.objects(id_archivo=id_archivo)
			archivo = archivo[0]
			#Añadir el archivo al diccionario
			archivos_dic[id_archivo] = [int(archivo.id_archivo), archivo.nombre, archivo.tipo_archivo, 
			str(archivo.fecha_subida), str(archivo.tam_archivo), archivo.favorito]

		return archivos_dic


	#Subir un archivo a un grupo
	def subirArchivoGrupo(self, id_grupo, nombre_archivo, tipo_archivo, path):
		a = ArchivoForm()
		#Subir el archivo a la base de datos
		id_archivo = a.save(nombre_archivo, tipo_archivo, "", path, 0)
		#Añadir fichero al grupo de trabajo
		GrupoTrabajo.objects(id_grupo=id_grupo).update(add_to_set__archivos=[int(id_archivo)])

	#Borrar un archivo
	def borrarArchivo(self, id_archivo, id_grupo):
		archivos = list(Archivo.objects.filter(id_archivo=id_archivo))
		archivos[0].archivo.delete()
		ArchivoCompartido.objects.filter(id_archivo_compartido=id_archivo).delete()
		Archivo.objects.filter(id_archivo=id_archivo).delete()

		GrupoTrabajo.objects(id_grupo=id_grupo).update(pull__archivos=int(id_archivo))

	#Obtener los participantes de un grupo
	def getParticipantes(self, id_grupo):
		grupo = list(GrupoTrabajo.objects.filter(id_grupo=id_grupo))
		participantes_dic = {}

		#Almacenar los usuarios del grupo X en un diccionario
		cont = 0
		for username in grupo[0].usuarios:
			#Añadir el usuario al diccionario
			u = UsuarioForm()
			participantes_dic[cont] = [username, u.getImgPerfil(username)]
			cont += 1

		return participantes_dic

	#Salir de un grupo de trabajo
	def salirGrupo(self, username, id_grupo):
		grupo = GrupoTrabajo.objects(id_grupo=id_grupo)[0]
		grupo.usuarios.remove(username)
		grupo.save()

		if len(grupo.usuarios) == 0:
			for id_archivo in grupo.archivos:
				self.borrarArchivo(id_archivo, id_grupo)

			GrupoTrabajo.objects(id_grupo=id_grupo).delete()

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