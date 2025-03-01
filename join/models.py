from django.db import models

# Create your models here.
class Contact(models.Model):
	name = models.CharField(max_length=366)
	email = models.EmailField(max_length=366)
	phone = models.IntegerField()
	color = models.CharField(max_length=366, default='')

class Category(models.Model):
	title = models.CharField(max_length=330)

class Task(models.Model):
	title = models.CharField(max_length=30)
	description = models.CharField(max_length=366, blank=True)
	date = models.DateField()
	priority = models.CharField(max_length=366)
	assignedTo = models.ManyToManyField(Contact, related_name='contact')
	category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
	subtasks = models.JSONField(null=True)
	status = models.CharField(max_length=366)

        # 'assign-to': checkedContacts,
        # 'finishedSubtasks': finishedSubtasks,

	def __str__(self):
		return self.title

class Summary(models.Model):
	toDo = models.IntegerField()
	done = models.IntegerField()
	urgent = models.IntegerField()
	tasksInBoard = models.IntegerField()
	tasksInProgress = models.IntegerField()
	awaitingFeedback = models.IntegerField()