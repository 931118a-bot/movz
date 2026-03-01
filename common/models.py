from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=50, verbose_name='이름')
    phone = models.CharField(max_length=20, verbose_name='전화번호')
    
    def __str__(self):
        return self.user.username
