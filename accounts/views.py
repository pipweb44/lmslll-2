from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import User, StudentProfile, TeacherProfile
from .forms import CustomUserCreationForm, ProfileEditForm

class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:profile')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        
        # Create profile based on user type
        if user.user_type == 'student':
            StudentProfile.objects.create(
                user=user,
                student_id=f"STU{user.id:06d}"
            )
        elif user.user_type == 'teacher':
            TeacherProfile.objects.create(user=user)
        
        messages.success(self.request, 'Account created successfully!')
        return response

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_student:
            context['enrollments'] = user.enrollments.all()
            context['enrollment_requests'] = user.enrollment_requests.all()
        elif user.is_teacher:
            context['courses'] = user.courses_taught.all()
            context['total_students'] = sum(course.total_students for course in user.courses_taught.all())
        
        return context

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)
