from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('employer', 'Employer'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class Job(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE)  # Работодатель
    title = models.CharField(max_length=255)  # Название вакансии
    description = models.TextField()  # Описание вакансии
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Зарплата (необязательно)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return self.title