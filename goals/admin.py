from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Goal)
admin.site.register(models.goal_mode)
admin.site.register(models.Period)

