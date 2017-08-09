from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from mongoengine import *
import datetime

class Usuario(Document):
    id_username = IntField(required=True, unique=True)
    username = StringField(required=True, unique=True)

class Directorio(Document):
	id_directorio = DecimalField()
	nombre = StringField()
	contenido = ListField()

class Archivo(Document):
	id_archivo = DecimalField()
	nombre = StringField()
	tipo_archivo = StringField()
	archivo = FileField()
	fecha_subida = StringField()
	propietario = StringField(required=True)
	tam_archivo = DecimalField()
	favorito = BooleanField()

class ArchivoCompartido(Document):
	propietario = StringField(required=True)
	destinatario = StringField(required=True)
	id_archivo_compartido = DecimalField(required=True)