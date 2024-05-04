from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    image = models.ImageField(upload_to='post/')
    caption = models.CharField(max_length=200) 
    like_count = models.IntegerField(default = 0)
    comment_count = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    fk_user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

class profile(models.Model):
    fk_user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile/') 
    bio = models.CharField(max_length=250) 
    favorite = models.ManyToManyField(Post,blank=True)


class story(models.Model):
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='story/',blank=True)

class comment(models.Model):
    fk_user = models.ForeignKey(User,on_delete=models.CASCADE)
    fk_post = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment = models.CharField(max_length = 30)
    created_at = models.DateTimeField(auto_now_add = True)

class Like(models.Model):
    fk_user = models.ForeignKey(User,on_delete=models.CASCADE)
    fk_post = models.ForeignKey(Post,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add = True)

class follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'following')

# class stream(models.Model):
#     following = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'stream_following') 
#     fk_user = models.ForeignKey(User,on_delete=models.CASCADE)
#     fk_post = models.ForeignKey(Post,on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add = True)

class otp(models.Model):
    otp = models.CharField(max_length=6)
    fk_user = models.OneToOneField(User,on_delete=models.CASCADE)


