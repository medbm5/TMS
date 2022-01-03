from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=150)
    longitude = models.CharField(max_length=150)
    latitude = models.CharField(max_length=50)
  
    def __str__(self):
        return self.name
