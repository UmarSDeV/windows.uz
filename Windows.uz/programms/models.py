
from django.forms import ModelForm
from django import db
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.db.models.aggregates import Count
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=250, unique=True)
    keywords = models.CharField(max_length=300, unique=True)
    description = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(null=False, unique=True)
    image = models.ImageField(upload_to='images/', blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug':self.slug})

class Programm(models.Model):

    STATUS =(
        ('True', 'Mavjud'),
        ('False', 'Mavjud emas')
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name='program',unique=True)
    keywords = models.CharField(max_length=300, unique=True)
    description = models.CharField(max_length=300, blank=True)
    detail = RichTextUploadingField()
    slug = models.SlugField(unique=True, null=False)    
    status = models.CharField(max_length=20, choices=STATUS)
    torrent = models.FileField()
    image = models.ImageField(upload_to='images', blank=True)
    link = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug':self.slug})

    def image_tag(self):
        return mark_safe('img< scr"={}" height="50">'.format(self.image.url))
    image_tag.short_description = 'Image'

    def averageview(self):
        reviews = Comment.objects.filter(programm=self, status='True').aggregate(Count=Count('id'))
        cnt =0
        if reviews['count'] is not None:
            cnt = int(reviews['count'])
        return cnt


class Images(models.Model):
    program = models.ForeignKey(Programm, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(blank=True, upload_to = 'images/')

    def __str__(self):
        return self.title


class Comment(models.Model):
    STATUS = {
        ('New', 'Yangi'),
        ('True', 'Mavjud'),
        ('False', 'Mavjud emas')
    }
    product = models.ForeignKey(Programm, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=300, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']    


