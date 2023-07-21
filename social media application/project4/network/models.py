from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class Posts(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_name = models.CharField(null=True, max_length=30)    
    name = models.CharField(max_length=64)
    likes = models.IntegerField()
    picture_link = models.ImageField(null=True, upload_to="images/")
    timestamp = models.DateTimeField(null=True)
    liked_by = models.ManyToManyField(User,symmetrical=False, blank=True, related_name='liked')


class Comments(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.CharField(max_length=600)


class FFowers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, symmetrical=False, blank=True, related_name='followers')
    followers = models.ManyToManyField(User, symmetrical=False, blank=True, related_name='following')