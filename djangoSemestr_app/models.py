from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='djangoSemestr_app/static/images')
    about = models.CharField(max_length=400)


class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='followers_as_user')
    following = models.ManyToManyField(User, related_name='following_as_user', null=True)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='djangoSemestr_app/static/images/завантаження.jpg')
    about = models.CharField(max_length=300, null=True)
