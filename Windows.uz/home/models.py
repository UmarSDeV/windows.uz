from programms.models import Category
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.forms import ModelForm, TextInput, Textarea, EmailInput
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.



class Setting(models.Model):
    STATUS = (
        ('True','Mavjud'),
        ('False','Mavjud emas'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=350)
    description = models.CharField(max_length=350)
    company = models.CharField(max_length=150)
    address = models.CharField(blank=True, max_length=150)
    phone = models.CharField(blank=True, max_length=30)
    fax = models.CharField(max_length=30, blank=True)
    email = models.CharField(max_length=50, blank=True)
    icon = models.ImageField(blank=True, upload_to='images/')
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    telegram = models.CharField(blank=True, max_length=50)
    youtube = models.CharField(blank=True, max_length=50)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'setting'
        verbose_name_plural = 'settings'

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    STATUS = {
        ('New', 'Yangi'),
        ('Read',"O'qilgan"),
        ('CLosed', 'Yopilgan')
    }
    selectCategory = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, blank=True)
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=300)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(max_length=100, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'selectCategory', 'message']
        widgets = {
            'name':TextInput(attrs={'class': 'input', 'placeholder':'Name $ Surname'}),
            'selectCategory':TextInput(attrs={'class':'input', 'placeholder':'Category'}),
            'email':EmailInput(attrs={'class':'input', 'placeholder':'Email Address'}),
            'message':Textarea(attrs={'class':'input', 'placeholder':'Your message will not ber more 300 symbols', 'rows':'5'}),
        }


class FAQ(models.Model):
    STATUS = {
        ('True', 'Mavjud'),
        ('False','Mavjud emas'),
    }
    ordernumber = models.IntegerField()
    question = models.CharField(max_length=200)
    answer = RichTextUploadingField()
    status = models.CharField(max_length=15, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question