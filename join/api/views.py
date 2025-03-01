from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from ..models import Contact, Category, Task, Summary
from .serializers import ContactSerializer, CategorySerializer, TaskSerializer, SummarySerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.http import Http404

# Create your views here.
class ContactsListView(APIView):
	def get(self, request):
		contacts = Contact.objects.all()
		serializer = ContactSerializer(contacts, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = ContactSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactsDetailView(APIView):
    def get_object(self, pk):
        try:
            return Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        contact = self.get_object(pk)
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    def put(self, request, pk):
        contact = self.get_object(pk)
        serializer = ContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contact = self.get_object(pk)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryListView(generics.ListCreateAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer

class TaskViewSet(viewsets.ModelViewSet):
	queryset = Task.objects.all()
	serializer_class = TaskSerializer

class SummaryViewSet(viewsets.ViewSet):
	queryset = Summary.objects.all()

	def list(self, request):
		serializer = SummarySerializer(self.queryset, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk=None):
		task = get_object_or_404(self.queryset, pk=pk)
		serializer = SummarySerializer(task)
		return Response(serializer.data)

	def create(self, request):
		serializer = SummarySerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def update(self, request, pk=None):
		task = self.queryset.get(pk=pk)
		serializer = SummarySerializer(task, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def destroy(self, request, pk=None):
		task = self.queryset.get(pk=pk)
		task.delete()
		return Response(task)