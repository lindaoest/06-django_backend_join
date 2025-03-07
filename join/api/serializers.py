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
	# assignedTo_ids = ContactSerializer(many=True, read_only=True)
	# assignedTo = serializers.ListField(
	# 	child=serializers.DictField(),
	# 	write_only=True
	# )

	category = serializers.CharField()
	# category_id = serializers.IntegerField(source="category.id", read_only=True)

	def create(self, validated_data):
		# print('category', validated_data)
		contacts_data = validated_data.pop('assignedTo')
		category_data = validated_data.pop('category', '')
		# assigned_contacts = []

		# for contact in contacts_data:
		# 	contact_id = Contact.objects.get(id=contacts_data.id)
		# 	print('id', contact_id)
		# 	assigned_contacts.append(contact.get('id'))

		category = Category.objects.get(title=category_data)

		task = Task.objects.create(category=category, **validated_data)
		task.assignedTo.set(contacts_data)

		# print('assigned_contacts', assigned_contacts)
		print('task', task)

		return task
		# contact_ids = validated_data.pop('assignedTo') # Extrahiere die Market-IDs und entferne sie aus validated_data
		# tasks = Contact.objects.create(**validated_data) # Erstelle ein neues Seller-Objekt mit den restlichen Daten
		# contacts = Contact.objects.filter(id__in=contact_ids) # Hole die Market-Objekte anhand der IDs
		# seller.market.set(markets) # Weise die Märkte dem Seller zu (Many-to-Many Beziehung)
		# return seller # Gib das erstellte Seller-Objekt zurück


	class Meta:
		model = Task
		fields = '__all__'

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