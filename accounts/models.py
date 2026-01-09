from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ('author', 'Author'),
        ('admin', 'Admin'),
    )

    name = models.CharField(max_length=255, blank=True)
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
    phone_number = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def is_author(self):
        return self.role == 'author'
