from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Role(models.Model):
    role = models.CharField(max_length=20, null=False)

    def __str__(self):
        return f"{self.role}"


class Profile(models.Model):
    """
    Extra model to be able to add params apart from Django's default one
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Email is verified
    verified = models.BooleanField(default=False)
    # User roles (user can search or upload to those roles)
    roles = models.ManyToManyField(Role)

    def __str__(self):
        return f"{self.user}, {self.verified}, {self.roles}"
