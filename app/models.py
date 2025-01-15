from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta
import datetime

def default_valid_from():
    return datetime.date.today()

def default_expires_at():
    return datetime.date.today() + datetime.timedelta(days=365)
# Create your models here.
class Domain(models.Model):
    domain = models.CharField(max_length=50)
    owner = models.ForeignKey('auth.User', related_name='domain', on_delete=models.CASCADE)
    valid_from = models.DateField(default=default_valid_from)
    expires_at = models.DateField(default=default_expires_at)

class Transaction(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    card_last4 = models.CharField(max_length=4) 
    date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)
    full_name = models.CharField(max_length=30)
