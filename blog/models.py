import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField



class BaseModel(models.Model):
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    avatar = models.ImageField(upload_to='media/profile_pictures', default='static/user.png')
    contact = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class Post(BaseModel):
    title = models.CharField(max_length=255)
    content = RichTextUploadingField(config_name='editor', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    author = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(BaseModel):
    text = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)



