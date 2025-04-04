from rest_framework import serializers
from ..models import Contact, Category, Task

class ContactSerializer(serializers.ModelSerializer):

	class Meta:
		model = Contact
		fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):

	assignedTo = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), many=True, write_only=True)
	contacts = serializers.SerializerMethodField(read_only=True)
	category = serializers.CharField()

	def create(self, validated_data):
		contacts_data = validated_data.pop('assignedTo', '')
		category_data = validated_data.pop('category', '')

		category, _ = Category.objects.get_or_create(title=category_data)

		task = Task.objects.create(category=category, **validated_data)
		task.assignedTo.set(contacts_data)

		return task

	def update(self, instance, validated_data):
		contacts_data = validated_data.pop('assignedTo', '')
		category_data = validated_data.pop('category', '')

		category = Category.objects.get(title=category_data)

		instance.title = validated_data.get('title', instance.title)
		instance.description = validated_data.get('description', instance.description)
		instance.date = validated_data.get('date', instance.date)
		instance.priority = validated_data.get('priority', instance.priority)
		instance.category = category
		instance.subtasks = validated_data.get('subtasks', instance.subtasks)
		instance.finishedSubtasks = validated_data.get('finishedSubtasks', instance.finishedSubtasks)
		instance.status = validated_data.get('status', instance.status)

		instance.assignedTo.set(contacts_data)

		instance.save()
		return instance

	class Meta:
		model = Task
		fields = ['id', 'category', 'title', 'description', 'date', 'priority', 'finishedSubtasks', 'subtasks', 'status', 'contacts', 'assignedTo']

	def get_contacts(self, obj):
		return [contact.name for contact in obj.assignedTo.all()]