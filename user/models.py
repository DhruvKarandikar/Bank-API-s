from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=16)
    gender = models.CharField(max_length=1)
    age = models.IntegerField(default=1)




