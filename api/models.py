from django.db import models

# Create your models here.
class Contextos(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self) -> str:
        return f'{self.id} - Context name: {self.name}'