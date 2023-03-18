from django.urls import path
from . import views

urlpatterns = [
    path('', views.Articlespage, name='articles'),
    path('article/<str:pk>/', views.article, name="article"),
]
