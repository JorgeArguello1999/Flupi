from django.db import models

# Create your models here.
class ImageProfile(models.Model):
    id = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to='uploads/')
    name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.id} - {self.name}' 