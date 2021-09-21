from os import link
from django.contrib.auth import forms
from django.contrib.auth.models import User
from django.db import models
from programms.models import Programm

# Create your models here.

class Download(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    prog = models.ForeignKey(Programm, on_delete=models.SET_NULL, null=True)
    link = models.CharField(max_length=500) 

    def __str__(self):
        return self.product.title