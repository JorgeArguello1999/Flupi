from django.db import models

# Create your models here.
class StatusWork(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.BooleanField()

    def __str__(self) -> str:
        return f'{self.id} Estado: {self.status}'