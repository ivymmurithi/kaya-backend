from django.db import models
# Create your models here.

'''
 ------------------------ 
| id | username | balance|
 ------------------------
| 1  | mukami   | 120000 |
 ------------------------
'''
class Account(models.Model):
    username = models.CharField(max_length=255, null=False, blank=False, unique=True)
    balance = models.FloatField(default=0, null=False, blank=False)