from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Period(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class goal_mode(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Goal(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    desc = models.TextField(default='', null=True, blank=True)
    goal = models.PositiveIntegerField(default=0, null=False, blank=False)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, null=False)
    mode = models.ForeignKey(goal_mode, on_delete=models.CASCADE, null=False)
    created = models.DateTimeField(auto_now_add=True)
    goal_done = models.PositiveIntegerField(default=0, null=True, blank=True)
    progress = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

