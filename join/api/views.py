from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from ..models import Contact, Category, Task
from .serializers import ContactSerializer, CategorySerializer, TaskSerializer
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

class SummaryView(APIView):
	def get(self, request):
		toDo = 0
		done = 0
		tasksInProgress = 0
		awaitingFeedback = 0

		urgent = 0

		tasksInBoard = Task.objects.count()

		tasks = Task.objects.all()

		for task in tasks:
			if task.status == 'to-do':
				toDo += 1
			elif task.status == 'done-tasks':
				done += 1
			elif task.status == 'in-progress':
				tasksInProgress += 1
			elif task.status == 'await-feedback':
				awaitingFeedback += 1

			if task.priority == 'Urgent':
				urgent += 1

		data = {
			"to-do": toDo,
			"done": done,
			"tasks-in-progress": tasksInProgress,
			"awaiting-feedback": awaitingFeedback,
			"urgent": urgent,
			"tasks-in-board": tasksInBoard
		}
		return Response(data)