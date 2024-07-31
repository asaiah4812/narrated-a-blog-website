from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django_countries.fields import CountryField

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    realname = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    location = CountryField(blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('images/default.jpg')
        return avatar
    
    @property
    def name(self):
        if self.realname:
            name = self.realname
        else:
            name = self.user.username
        return name
    

