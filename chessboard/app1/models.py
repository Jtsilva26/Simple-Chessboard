from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Board(models.Model):
 value = models.CharField(max_length=8)
 user = models.ForeignKey(User, on_delete=models.CASCADE)
 location = models.CharField(max_length=2)
 class Meta:
     unique_together = (("user", "location"))
