from django.urls import path
from . import views

app_name = 'ratings'

urlpatterns = [
    path('rate/<slug:course_slug>/', views.RateCourseView.as_view(), name='rate_course'),
]
