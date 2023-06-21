from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('articles/', include('article.urls')),
    path('goals/', include('goals.urls')),
    path('tutorials/', include('tutorials.urls')),

]
