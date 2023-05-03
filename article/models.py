from django.db import models

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    desc = models.TextField(null=False, blank=False)
    img = models.TextField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title