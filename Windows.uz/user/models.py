from os import truncate
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils.safestring import mark_safe

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=CASCADE)
    phone = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to='images/users/', blank=True)

    def __str__(self):
        return self.user.username
    
    def username(self):
        return self.user.first_name + '' + self.user.last_name + '[' + self.user.username +']'
    
    def image_tag(self):
        return mark_safe('img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = "Image"