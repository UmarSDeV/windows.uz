from django import forms
from django.db import models

class SearchForm(forms.ModelForm):
    query = models.CharField(max_length=100)
    category_id = forms.IntegerField()