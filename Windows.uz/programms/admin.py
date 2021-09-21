from django.contrib import admin
from .models import Programm, Category, Images, Comment
# Register your models here.

admin.site.register(Programm)
admin.site.register(Category)
admin.site.register(Images)
admin.site.register(Comment)