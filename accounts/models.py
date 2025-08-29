from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('student', _('Student')),
        ('teacher', _('Teacher')),
        ('admin', _('Admin')),
    ]
    
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='student'
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    @property
    def is_student(self):
        return self.user_type == 'student'
    
    @property
    def is_teacher(self):
        return self.user_type == 'teacher'
    
    @property
    def is_admin(self):
        return self.user_type == 'admin'

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    education_level = models.CharField(max_length=100, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Student: {self.user.username}"

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    specialization = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField(default=0)
    qualifications = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Teacher: {self.user.username}"
