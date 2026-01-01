from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q

ALLOWED_RE = r'^[\w.@#$%^&+=!_.\-/?*()]+$'

class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин',
        help_text='Латиница, цифры и @#$%^&+=!_.-/?*()',
    )

    @property
    def is_student(self):
        return hasattr(self, 'student')
    
    @property
    def is_teacher(self):
        return hasattr(self, 'teacher')
    
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                name='username_allowed_chars',
                check=Q(username__regex=ALLOWED_RE),
            ),
        ]
