from django.db.models import fields
from django.forms import ModelForm
from .models import *

class CreateCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'description', 'create_at']

class EditProgrammForm(ModelForm):
    class Meta:
        model = Programm
        fields = ['title', 'keywords', 'description', 'detail', 'torrent', 'image', 'link']

class CreateProgrammForm(ModelForm):
    class Meta:
        model = Programm
        fields = ['category', 'title', 'keywords', 'description', 'detail', 'torrent', 'image', 'link', 'create_at']


