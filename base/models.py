from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class chek(models.Model):
    date = models.DateTimeField(auto_now_add=False, blank=True, null=True)


class Topic(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    page = models.PositiveIntegerField(default=0)
    data = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class studySummary(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, null=True, on_delete=models.CASCADE)
    data = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Period(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Goal(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    goal = models.PositiveIntegerField(default=0, null=False, blank=False)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name

