from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomePage, name='main'),
    path('tutorial/<int:tutorial_id>/', views.tutorial_detail, name='tutorial_detail'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('update_video_progress/<int:video_id>/', views.update_video_progress, name='update_video_progress'),
    path('excel-export/', views.export_users_xls, name='export-excel'),
]
