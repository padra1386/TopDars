from django.db import models

# Create your models here.
class studySummary(models.Model):
    title = models.CharField
    data = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
