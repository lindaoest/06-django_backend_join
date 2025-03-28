from rest_framework import serializers
from ..models import Contact, Category, Task, Summary

class ContactSerializer(serializers.ModelSerializer):

	class Meta:
		model = Contact
		fields = ['id', 'name', 'email', 'phone', 'color']
	# name = serializers.CharField(max_length=366)
	# email = serializers.EmailField(max_length=366)
	# phone = serializers.IntegerField()
	# color = serializers.CharField()

	# def create(self, validated_data):
	# 	return Contact.objects.create(**validated_data)

	# def update(self, instance, validated_data):
	# 	instance.name = validated_data.get('name', instance.name)
	# 	instance.email = validated_data.get('email', instance.email)
	# 	instance.phone = validated_data.get('phone', instance.phone)
	# 	instance.color = validated_data.get('color', instance.color)
	# 	instance.save()
	# 	return instance

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):

	assignedTo = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(),many=True, write_only=True)
	contacts = serializers.SerializerMethodField()
	category = serializers.CharField()

	def create(self, validated_data):
		contacts_data = validated_data.pop('assignedTo')
		category_data = validated_data.pop('category', '')

		category, _ = Category.objects.get_or_create(title=category_data)

		task = Task.objects.create(category=category, **validated_data)
		task.assignedTo.set(contacts_data)

		return task
	class Meta:
		model = Task
		fields = ['id', 'category', 'title', 'description', 'date', 'priority', 'finishedSubtasks', 'subtasks', 'status', 'contacts', 'assignedTo']

	def get_contacts(self, obj):
		return [contact.name for contact in obj.assignedTo.all()]

class SummarySerializer(serializers.ModelSerializer):

	toDo = serializers.SerializerMethodField()

	def get_toDo(self, obj):
		count = 0
		tasks = Task.objects.all()

		for task in tasks:
			if task.status == 'to-do':
				count += 1

		return count
	class Meta:
		model = Summary
		fields = '__all__'