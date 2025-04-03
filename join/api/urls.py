from django.urls import path
from .views import ContactsListView, ContactsDetailView, TaskListView, TaskDetailView, SummaryView, CategoryListView, CategoryDetailView

urlpatterns = [
    path('contacts/', ContactsListView.as_view()),
    path('contacts/<int:pk>/', ContactsDetailView.as_view()),
    path('summary/', SummaryView.as_view()),
    path('tasks/', TaskListView.as_view()),
    path('tasks/<int:pk>/', TaskDetailView.as_view()),
	path('categories/', CategoryListView.as_view()),
    path('categories/<int:pk>/', CategoryDetailView.as_view())
]