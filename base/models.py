from django.db import models
from django.contrib.auth import get_user_model
import uuid
# Create your models here.

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimage = models.ImageField(upload_to='profileimages' , default='default.jpg')
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username 
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='postimage')
    caption = models.CharField(max_length=500)
    no_of_likes = models.IntegerField(default=0)
    no_of_comments = models.IntegerField(default=0)

    
    def __str__(self):
        return self.user

    
class LikePost(models.Model):
    post_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class FollowCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user




class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]

class Message(models.Model):
    sender = models.CharField(max_length=100)
    reciver = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile , on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.body[0:50]