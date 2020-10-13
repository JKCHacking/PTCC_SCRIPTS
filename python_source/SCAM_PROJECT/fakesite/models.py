from django.db import models


# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=10, default="No email")


class Visitor(models.Model):
    username = models.CharField(max_length=100, default="No Username")
    pub_ip = models.CharField(max_length=10, default="No Public IP")
