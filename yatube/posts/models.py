from tokenize import group
from turtle import title
from django.db import models
from django.contrib.auth import get_user_model
# Обращение к пользовалям делается через метод в соответствии с документацией
User = get_user_model()
# Create your models here.


class Group(models.Model):
    title = models.CharField(max_length = 200)
    slug = models.SlugField(unique = True)
    description = models.TextField()

class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='posts')
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.CASCADE)