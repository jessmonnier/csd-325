'''
Jess Monnier, CSD-325 Assignment 11.2, 9 March 2025
The urls defined in this script came from the following GitHub distro:
https://github.com/shreys7/django-todo/tree/develop
'''

from django.urls import path
from . import views

app_name='todos'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:todo_id>/delete', views.delete, name='delete'),
    path('<int:todo_id>/update', views.update, name='update'),
    path('add/', views.add, name='add'),
    path('about.html', views.about, name='about') # I added this one
]