# models.py
from django.db import models

class clients(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    code = models.CharField(max_length=6, blank=True, null=True)  # <-- Add this line
