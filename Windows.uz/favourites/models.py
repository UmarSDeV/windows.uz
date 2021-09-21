from django.core.exceptions import MiddlewareNotUsed
from django.db import models
from django.contrib.auth.models import User
from django.db.models import fields
from django.forms import ModelForm

from programms.models import Programm
# Create your models here.

class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    programm = models.ForeignKey(Programm, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.programm.title

class FavouriteForm(ModelForm):
    class Meta:
        model = Favourite
        fields = ['quantity']
    

