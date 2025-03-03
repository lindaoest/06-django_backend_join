from rest_framework import serializers
from ..models import Contact, Category, Task, Summary

class ContactSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=366)
	email = serializers.EmailField(max_length=366)
	phone = serializers.IntegerField()
	color = serializers.CharField()

	def create(self, validated_data):
		return Contact.objects.create(**validated_data)

	def update(self, instance, validated_data):
		instance.name = validated_data.get('name', instance.name)
		instance.email = validated_data.get('email', instance.email)
		instance.phone = validated_data.get('phone', instance.phone)
		instance.color = validated_data.get('color', instance.color)
		instance.save()
		return instance

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):

	assignedTo = ContactSerializer(many=True, read_only=True)
	assignedTo_ids = serializers.PrimaryKeyRelatedField(
		queryset = Contact.objects.all(),
		many=True,
		write_only=True,
		source = 'assignedTo'
	)
	# assignedTo = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), many=True, write_only=True)  # Nur für die Eingabe (POST/PUT)
	# contacts = serializers.StringRelatedField(source="assignedTo", many=True, read_only=True)

	category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
	type = serializers.StringRelatedField(source="category", read_only=True)

	class Meta:
		model = Task
		fields = '__all__'

class SummarySerializer(serializers.Serializer):
	class Meta:
		model = Summary
		fields = '__all__'