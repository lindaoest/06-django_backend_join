from django.db import models
from django.db.models import PROTECT

# Create your models here.
class Contact(models.Model):
	name = models.CharField(max_length=366)
	email = models.EmailField(max_length=366)
	phone = models.IntegerField()
	color = models.CharField(max_length=366, default='')

	def __str__(self):
		return self.name

class Category(models.Model):
	title = models.CharField(max_length=330)

	def __str__(self):
		return self.title

class Task(models.Model):
	title = models.CharField(max_length=30)
	description = models.CharField(max_length=366, blank=True)
	date = models.DateField()
	priority = models.CharField(max_length=366)
	assignedTo = models.ManyToManyField(Contact, related_name='contact')
	category = models.ForeignKey(Category, related_name='category', on_delete=PROTECT) # Category cannot be deleted
	subtasks = models.JSONField(null=True)
	finishedSubtasks = models.JSONField(default=list, blank=True)
	status = models.CharField(max_length=366)

	def __str__(self):
		return self.title