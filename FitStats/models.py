from django.db import models

# Create your models here.
class User(models.Model):
    email=models.CharField(max_length=200, primary_key=True)
    password=models.CharField(max_length=200)
    username = models.CharField(max_length=100)