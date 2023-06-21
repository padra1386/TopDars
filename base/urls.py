from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homePage, name='home'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutPage, name='logout'),
    path('login/', views.loginPage, name='login'),
    path('create-room/', views.createTopic, name="create-topic"),
    path('accounts/', include('allauth.urls')),
    path('update-user/', views.updateUser, name='update-user')
]
