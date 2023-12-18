from django.db import models

# Create your models here.
class Contextos:
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    content = models.TextField()