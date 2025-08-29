from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import Course

class EnrollmentRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollment_requests'
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollment_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Contact information for enrollment
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField(blank=True, null=True)
    
    # Admin fields
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_enrollments'
    )
    admin_notes = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title} ({self.status})"

class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_request = models.OneToOneField(
        EnrollmentRequest,
        on_delete=models.CASCADE,
        related_name='enrollment'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress_percentage = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
    
    @property
    def is_completed(self):
        return self.completed_at is not None

class VideoProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='video_progress')
    video = models.ForeignKey('courses.Video', on_delete=models.CASCADE)
    watched_duration = models.PositiveIntegerField(default=0)  # in seconds
    is_completed = models.BooleanField(default=False)
    last_watched = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['enrollment', 'video']
    
    def __str__(self):
        return f"{self.enrollment.student.username} - {self.video.title}"

# Signal to automatically create enrollment when request is approved
@receiver(post_save, sender=EnrollmentRequest)
def create_enrollment_on_approval(sender, instance, **kwargs):
    """
    Automatically create an Enrollment when EnrollmentRequest status changes to 'approved'
    """
    if instance.status == 'approved':
        # Check if enrollment doesn't already exist
        enrollment, created = Enrollment.objects.get_or_create(
            student=instance.student,
            course=instance.course,
            defaults={'enrollment_request': instance}
        )
        
        if created:
            print(f"🎓 Auto-enrolled: {instance.student.username} in {instance.course.title}")
            # Here you could add email notification or other actions
            # send_enrollment_confirmation_email(instance.student, instance.course)
