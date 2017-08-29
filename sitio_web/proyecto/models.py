from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from mongoengine import *
import datetime

class Usuario(Document):
    id_username = IntField(required=True, unique=True)
    username = StringField(required=True, unique=True)
    img_perfil = IntField()

class Directorio(Document):
	identificador_tupla = StringField(required=True, unique=True)
	id_directorio = DecimalField(required=True)
	nombre = StringField(required=True)
	id_padre = DecimalField(required=True)
	contenido = ListField()
	propietario = StringField()

class DirectorioContenidoMultimedia(Document):
	identificador_tupla = StringField(required=True, unique=True)
	id_directorio = DecimalField(required=True)
	nombre = StringField(required=True)
	id_padre = DecimalField(required=True)
	contenido = ListField()
	propietario = StringField()

class Archivo(Document):
	id_archivo = DecimalField()
	nombre = StringField()
	tipo_archivo = StringField()
	archivo = FileField()
	fecha_subida = StringField()
	propietario = StringField()
	tam_archivo = DecimalField()
	favorito = BooleanField()

class ArchivoCompartido(Document):
	propietario = StringField(required=True)
	destinatario = StringField(required=True)
	id_archivo_compartido = DecimalField(required=True)
	identificador_tupla = StringField(required=True, unique=True)

class GrupoTrabajo(Document):
	id_grupo = DecimalField(required=True, unique=True)
	nombre = StringField(required=True)
	usuarios = ListField()
	archivos = ListField()