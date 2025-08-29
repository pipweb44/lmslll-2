from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import EnrollmentRequest, Enrollment
from .forms import EnrollmentRequestForm
from courses.models import Course

class EnrollmentRequestView(LoginRequiredMixin, CreateView):
    model = EnrollmentRequest
    form_class = EnrollmentRequestForm
    template_name = 'enrollments/request_enrollment.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_student:
            messages.error(request, 'Only students can request enrollment.')
            return redirect('courses:course_list')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_slug = self.kwargs['course_slug']
        context['course'] = get_object_or_404(Course, slug=course_slug)
        return context
    
    def form_valid(self, form):
        course_slug = self.kwargs['course_slug']
        course = get_object_or_404(Course, slug=course_slug)
        
        # Check if already requested or enrolled
        existing_request = EnrollmentRequest.objects.filter(
            student=self.request.user,
            course=course
        ).first()
        
        if existing_request:
            messages.warning(self.request, 'You have already requested enrollment for this course.')
            return redirect('courses:course_detail', slug=course.slug)
        
        form.instance.student = self.request.user
        form.instance.course = course
        messages.success(self.request, 'Enrollment request submitted successfully! We will contact you soon.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={'slug': self.kwargs['course_slug']})

class MyEnrollmentRequestsView(LoginRequiredMixin, ListView):
    model = EnrollmentRequest
    template_name = 'enrollments/my_requests.html'
    context_object_name = 'requests'
    
    def get_queryset(self):
        return EnrollmentRequest.objects.filter(student=self.request.user).select_related('course')

class MyCoursesView(LoginRequiredMixin, ListView):
    model = Enrollment
    template_name = 'enrollments/my_courses.html'
    context_object_name = 'enrollments'
    
    def get_queryset(self):
        return Enrollment.objects.filter(
            student=self.request.user,
            enrollment_request__status='approved'
        ).select_related('course', 'enrollment_request')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add user ratings to context to check if user has rated each course
        from ratings.models import Rating
        user_ratings = Rating.objects.filter(student=self.request.user).values_list('course_id', flat=True)
        context['user_rated_courses'] = list(user_ratings)
        return context
