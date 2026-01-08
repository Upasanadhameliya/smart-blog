from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ('author', 'Author'),
        ('admin', 'Admin'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='reader'
    )
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    def is_author(self):
        return self.role == 'author'
