from django.db import models

class Account(models.Model):
    username = models.CharField(max_length=255, null=False, blank=False, unique=True)
    balance = models.FloatField(default=0, null=False, blank=False)

    def __str__(self):
        return self.username
class Transaction(models.Model):
    action = models.CharField(max_length=255, null=False, blank=False)
    source = models.CharField(max_length=255, null=False, blank=False)
    target = models.CharField(max_length=255, null=True, blank=True)
    amount = models.FloatField(default=0, null=False, blank=False)

    def __str__(self):
        if self.action == 'TRANSFER':
            return f"{self.action}:{self.source}:{self.target}:{self.amount}"
        return f"{self.action}:{self.source}:{self.amount}"