from django import forms
from mongoengine import *
from requests import *
import datetime
from .models import *

class User():

	def save(self, _username):
		u = Usuario()

		u.username = _username
		u.id_username = Usuario.objects.count() + 1
		u.contenido = []
		u.compartido_por_mi = []
		u.compartido_conmigo = []

		u.save()

		return u

	def usuarioExiste(self, _username):
		user = Usuario.objects(username=_username)
		if len(user) == 0:
			return False
		return True