from django.contrib import admin
from django.urls import path, include
from .views import ContactsListView, ContactsDetailView, CategoryListView, CategoryDetailView, TaskViewSet, SummaryViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'summary', SummaryViewSet)

urlpatterns = [
    path('contacts/', ContactsListView.as_view()),
    path('contacts/<int:pk>', ContactsDetailView.as_view()),
	path('categories/', CategoryListView.as_view()),
    path('categories/<int:pk>', CategoryDetailView.as_view()),
	path('', include(router.urls)),
]