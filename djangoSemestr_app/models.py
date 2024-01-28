from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='media/profile_photo/')
    about = models.CharField(max_length=400)


class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='followers_as_user')
    following = models.ManyToManyField(User, related_name='following_as_user')


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='media/project_photo/')
    about = models.CharField(max_length=300)


class Chat(models.Model):
    members = models.ManyToManyField(User, related_name='members')


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=10000)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)