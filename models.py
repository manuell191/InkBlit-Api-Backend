from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.TextField(max_length=64)
    email = models.EmailField()
    bio = models.TextField(default='', blank=True, max_length=126)

class Follow(models.Model):
    account = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followings')

class Post(models.Model):
    account = models.ForeignKey(Profile, on_delete=models.CASCADE)
    username = models.TextField(max_length=64)
    content = models.TextField(max_length=252)
    room = models.TextField(max_length=6, default='global')

class Room(models.Model):
    title = models.TextField(max_length=128)
    code = models.TextField(max_length=6)
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE)

class RoomMember(models.Model):
    account = models.ForeignKey(Profile, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)