from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class courses(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField()
    img = models.TextField()
    price = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Video(models.Model):
    tutorial = models.ForeignKey(courses, on_delete=models.CASCADE)
    desc = models.TextField(default='')
    title = models.CharField(max_length=100)
    length = models.CharField(max_length=100, default='00:02:13')
    video_url = models.TextField()

    def __str__(self):
        return self.title
    # Add other fields as needed

class Comment(models.Model):
    courses = models.ForeignKey(courses, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content[0:50]
class Like(models.Model):
    tutorial = models.ForeignKey(courses, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Add other fields as needed


class VideoWatchProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    progress = models.CharField(max_length=20)
    created = models.DateTimeField()

    def __str__(self):
        return self.video.title
