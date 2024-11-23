from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=20, 
        choices=PRIORITY_CHOICES,
        default='MEDIUM'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
