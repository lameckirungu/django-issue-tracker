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

class Ticket(models.Model):
    """   
    Core ticket model for issue tracking
    """
    STATUS_CHOICES = [
        ('open', 'OPEN'),
        ('in_progress', 'iN Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    PRIORITY_CHOICES = [
        ('high', 'HIGH'),
        ('medium', 'Medium'),
        ('low', 'LOW'),
        ('critical', 'Critical'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tickets')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tickets")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')

    class Meta:
        db_table = 'tickets'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['created_by']),
            models.Index(fields=['assigned_to']),
        ]

    def __str__(self):
        return f"#{self.pk} - {self.title}"