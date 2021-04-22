from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    """
    Extra model to be able to add params apart from Django's default one
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Email is verified
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}, {self.verified}"
