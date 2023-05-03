from django.urls import path, include
from . import  views

urlpatterns = [
    path('', views.goals, name='goals'),
    path('create-goal', views.createGoal, name='create-goal'),
    path('add-goal/<str:pk>/', views.goalprogress, name='add-goal'),
]