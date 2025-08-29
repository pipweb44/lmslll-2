from django.contrib import admin
from .models import Rating

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'score', 'created_at']
    list_filter = ['score', 'created_at', 'course__category']
    search_fields = ['student__username', 'course__title']
    readonly_fields = ['created_at', 'updated_at']
