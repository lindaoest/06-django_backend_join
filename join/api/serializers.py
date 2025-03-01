from rest_framework import serializers
from ..models import Contact, Category, Task, Summary

class ContactSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=366)
	email = serializers.EmailField(max_length=366)
	phone = serializers.IntegerField()

	def create(self, validated_data):
		return Contact.objects.create(**validated_data)

	def update(self, instance, validated_data):
		instance.name = validated_data.get('name', instance.name)
		instance.email = validated_data.get('email', instance.email)
		instance.phone = validated_data.get('phone', instance.phone)
		instance.save()
		return instance

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = Task
		fields = '__all__'

class SummarySerializer(serializers.Serializer):
	class Meta:
		model = Summary
		fields = '__all__'