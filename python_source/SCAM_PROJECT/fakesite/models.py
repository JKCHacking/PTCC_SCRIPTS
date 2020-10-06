from django.db import models


# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=10, default="No email")


class Visitor(models.Model):
    pub_ip = models.CharField(max_length=10, default="No Public IP")
    priv_ip = models.CharField(max_length=10, default="No Private IP")
