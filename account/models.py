from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):

    options = (
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others')
    )

    age          =   models.IntegerField()
    gender       =   models.CharField(max_length=100,choices=options,default='Male')
    phone        =   models.IntegerField()
    profile_pic  =   models.ImageField(upload_to='Profile_Pictures')
    user         =   models.OneToOneField(User,on_delete=models.CASCADE,related_name='p_user')


class Blogs(models.Model):
    title        =   models.CharField(max_length=100)
    description  =   models.CharField(max_length=1000)
    image        =   models.ImageField(upload_to='Blog_images')
    date         =   models.DateField(auto_now_add=True)
    user         =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='b_user')
    liked_by     =   models.ManyToManyField(User,related_name='likes',null=True)

    @property
    def like(self):
        return self.liked_by.all()
    
    @property # make this method a property so no need to call it as a function we can call it by its name 
    def liked_users(self):
        users = self.liked_by.all()
        res = [user.username for user in users] # list comprehension
        return res
    
    @property
    def like_count(self): 
        like_count = self.liked_by.all().count()
        return like_count - 1 


class Comments(models.Model):
    comment      =   models.CharField(max_length=500)
    date         =   models.DateField(auto_now_add=True)
    user         =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='c_user')
    blog         =   models.ForeignKey(Blogs,on_delete=models.CASCADE,related_name='c_blog')

class Followers(models.Model):
    follower        =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='follower',null=True) # who follow us
    following       =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='following',null=True) # whom we follow

 