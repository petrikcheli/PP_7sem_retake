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
    
class Response(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено')
    ]
        
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responses")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="responses")
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'job')  # Один студент может откликнуться только один раз