from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Rating
from .forms import RatingForm
from courses.models import Course
from enrollments.models import Enrollment

class RateCourseView(LoginRequiredMixin, CreateView):
    model = Rating
    form_class = RatingForm
    template_name = 'ratings/rate_course.html'
    
    def dispatch(self, request, *args, **kwargs):
        course_slug = self.kwargs['course_slug']
        course = get_object_or_404(Course, slug=course_slug)
        
        # Check if user is enrolled in the course
        if not Enrollment.objects.filter(student=request.user, course=course).exists():
            messages.error(request, 'You must be enrolled in this course to rate it.')
            return redirect('courses:course_detail', slug=course_slug)
        
        # Check if user has already rated this course
        if Rating.objects.filter(student=request.user, course=course).exists():
            messages.warning(request, 'You have already rated this course.')
            return redirect('courses:course_detail', slug=course_slug)
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_slug = self.kwargs['course_slug']
        context['course'] = get_object_or_404(Course, slug=course_slug)
        return context
    
    def form_valid(self, form):
        course_slug = self.kwargs['course_slug']
        course = get_object_or_404(Course, slug=course_slug)
        
        form.instance.student = self.request.user
        form.instance.course = course
        messages.success(self.request, 'Thank you for rating this course!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={'slug': self.kwargs['course_slug']})
