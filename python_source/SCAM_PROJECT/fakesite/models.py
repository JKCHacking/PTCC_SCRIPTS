from django.db import models


# Create your models here.
class User(models.Model):
    pc_name = models.CharField(max_length=10, default="No Name")
    pub_ip = models.CharField(max_length=10, default="No Public IP")
    priv_ip = models.CharField(max_length=10, default="No Private IP")
