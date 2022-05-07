from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Account(models.Model):
    balance = models.FloatField(default=0, null=False, blank=False)
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)