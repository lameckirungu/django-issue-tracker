from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model extending Django's AbstractUser"""
    ROLES_CHOICES = [
        ('manager', 'Manager'),
        ('developer', 'Developer'),
        ('admin', 'Administrator'),
        ('user', 'Regular User'),
    ]

    id = models.UUIDField(primary_key=True, editable=False, auto_created=True)
    role = models.CharField(
        max_length=20,
        choices=ROLES_CHOICES,
        default='user',
        help_text="User role for permission management"
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        help_text='User profile picture',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_manager(self):
        return self.role in ['admin', 'manager']
