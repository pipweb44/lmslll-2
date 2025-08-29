from django.contrib import admin
from django.utils import timezone
from .models import EnrollmentRequest, Enrollment, VideoProgress

@admin.register(EnrollmentRequest)
class EnrollmentRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'status', 'phone_number', 'email', 'created_at', 'reviewed_by']
    list_filter = ['status', 'created_at', 'course__category', 'reviewed_by']
    search_fields = ['student__username', 'course__title', 'email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']  # Allow direct editing of status from list view
    
    actions = ['approve_requests', 'reject_requests']
    
    def save_model(self, request, obj, form, change):
        """Override save to handle status changes and auto-create enrollments"""
        if change and 'status' in form.changed_data:
            if obj.status == 'approved':
                obj.reviewed_by = request.user
                obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)
    
    def approve_requests(self, request, queryset):
        approved_count = 0
        for enrollment_request in queryset.filter(status='pending'):
            # Update request status
            enrollment_request.status = 'approved'
            enrollment_request.reviewed_by = request.user
            enrollment_request.reviewed_at = timezone.now()
            enrollment_request.save()
            
            # Create enrollment to give student access to course
            enrollment, created = Enrollment.objects.get_or_create(
                student=enrollment_request.student,
                course=enrollment_request.course,
                defaults={'enrollment_request': enrollment_request}
            )
            
            if created:
                approved_count += 1
                # Send notification to student (can be enhanced later)
                print(f"✅ Student {enrollment_request.student.username} enrolled in {enrollment_request.course.title}")
        
        if approved_count > 0:
            self.message_user(request, f"✅ {approved_count} enrollment requests approved successfully! Students now have access to their courses.")
        else:
            self.message_user(request, "No new enrollments created (students may already be enrolled).")
    approve_requests.short_description = "Approve selected enrollment requests"
    
    def reject_requests(self, request, queryset):
        queryset.update(
            status='rejected',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f"{queryset.count()} enrollment requests rejected.")
    reject_requests.short_description = "Reject selected enrollment requests"

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'progress_percentage', 'enrolled_at', 'is_completed']
    list_filter = ['enrolled_at', 'completed_at', 'course__category']
    search_fields = ['student__username', 'course__title']
    readonly_fields = ['enrolled_at']

@admin.register(VideoProgress)
class VideoProgressAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'video', 'watched_duration', 'is_completed', 'last_watched']
    list_filter = ['is_completed', 'last_watched']
    search_fields = ['enrollment__student__username', 'video__title']
