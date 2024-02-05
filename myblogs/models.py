from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils import timezone 

# Create your models here.
class blog_category(models.Model):
    blog_cat = models.CharField(max_length=60,unique=True)
    blogcat_img = models.ImageField(upload_to='images/')
    blogcat_description=models.CharField(max_length=1000)
    def __str__(self):
        return self.blog_cat
    # (self):
    #     return self.blog_cat
    
class contact_info(models.Model):
    u_email = models.EmailField()
    u_message = models.CharField(max_length=200)
    def __str__(self):
        return self.u_email
    
class Subscription(models.Model):
    u_email = models.EmailField()
    u_membership = models.CharField(max_length=200)
    def __str__(self):
        return self.u_email
    
class blog_post(models.Model):
    blog_name = models.CharField(max_length=100)
    cover_img = models.ImageField(upload_to='images/')
    blog_description = RichTextField()
    blog_cat = models.ForeignKey(blog_category,on_delete=models.CASCADE)
    like_count = models.IntegerField(default=0, null=True)
    views_count = models.IntegerField(default=0,null=True)
    def __str__(self):
            return self.blog_name
    
class Comment(models.Model):
    post = models.ForeignKey(blog_post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def str(self):
        return self.text

