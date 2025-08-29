from django.urls import path
from . import views

app_name = 'enrollments'

urlpatterns = [
    path('request/<slug:course_slug>/', views.EnrollmentRequestView.as_view(), name='request_enrollment'),
    path('my-requests/', views.MyEnrollmentRequestsView.as_view(), name='my_requests'),
    path('my-courses/', views.MyCoursesView.as_view(), name='my_courses'),
]
