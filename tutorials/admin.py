from django.contrib import admin
from .models import courses, Video, Like, Comment, VideoWatchProgress

# Register your models here.
admin.site.register(courses)
admin.site.register(Video)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(VideoWatchProgress)