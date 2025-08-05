from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='recipes/')
    ingredients = models.TextField(default="Ingredients coming soon...")
    procedure = models.TextField(blank=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')
    favourites = models.ManyToManyField(Recipe, blank=True, related_name='favourited_by')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
