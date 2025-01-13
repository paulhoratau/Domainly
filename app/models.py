from django.db import models


# Create your models here.
class Domain(models.Model):
    domain = models.CharField(max_length=50)
    owner = models.ForeignKey('auth.User', related_name='domain', on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)
    full_name = models.CharField(max_length=30)
