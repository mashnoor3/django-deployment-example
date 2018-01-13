from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo (models.Model):
    # make one to one relationship instead of inheriting. Want to add to User
    # so in general don't wanna inherit from models in order to prevent database from screwing up
     user = models.OneToOneField(User)

     # additional attributes
     #portfolio
     portfolio_site = models.URLField(blank=True) #make black=True to make it an optional field

     # image
     profile_pic = models.ImageField(upload_to='profile_pics', blank=True) # want to upload it to profile_pics

     def __str__ (self):
         return self.user.username
