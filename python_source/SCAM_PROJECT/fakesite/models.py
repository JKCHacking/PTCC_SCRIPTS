from django.db import models


# Create your models here.
class User(models.Model):
    pc_name = models.CharField(max_length=10)
    ip_add = models.CharField(max_length=10)
