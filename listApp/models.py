from django.db import models
from django.db.models import CharField, Model
from django.contrib.auth.models import User
from django.urls import reverse
from django_mysql.models import ListCharField
#from listApp.models import List

class List(models.Model):
	title = models.CharField(max_length = 500)
	description = models.CharField(max_length = 5000, help_text = 'Add a short description of your list')
	viewers = ListCharField(base_field = CharField(max_length = 500), max_length = 5000, help_text = 'Enter the usernames of the users that will have access to your list (separated with semicolons)', blank=True)
	author = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('list-detail', kwargs = {'pk': self.pk})


class Element(models.Model):
	theList = models.ForeignKey(List, on_delete = models.CASCADE)
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	name = models.CharField(max_length = 500)
	links = models.TextField(help_text = '[Optional] Add one or more useful links (separated with semicolons)', blank=True)
	images = models.TextField(help_text = '[Optional] Enter the URLs of one or more images (separated with semicolons)', blank=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('element-detail', kwargs = {'pk': self.pk})


class Viewer(models.Model):
	theList = models.ForeignKey(List, on_delete = models.CASCADE)
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	viewer = models.CharField(max_length = 500, help_text = 'Enter the username or the email adress of the user that you want to share your list with')

	def __str__(self):
		return self.viewer

	def get_absolute_url(self):
		return reverse('viewer-detail', kwargs = {'pk': self.pk})
