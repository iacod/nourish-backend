from django.db import models
from django.contrib.auth.models import User

class Volunteer(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  pounds = models.IntegerField()