from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from mongoengine import *
import datetime

class Usuario(Document):
    id_username = IntField(required=True, unique=True)
    username = StringField(required=True, unique=True)
    contenido = ListField() #Lista de directorios y archivos
    compartido_por_mi = ListField() #ID directorios y archivos
    compartido_conmigo = ListField() #ID directorios y archivos

class Directorio(Document):
	id_directorio = DecimalField()
	nombre = StringField()
	contenido = ListField()

class Archivo(Document):
	id_archivo = DecimalField()
	nombre = StringField()
	tipo_archivo = StringField()
	data = FileField()