"""
ein eigenes User-Model gibt uns mehr Freiheit im Design.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """mein eigenes User-Model"""

    address = models.CharField(max_length=200, null=True, blank=True)
