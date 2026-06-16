from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin for Review model"""
    
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__title', 'user__username', 'comment']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Review Details', {
            'fields': ('product', 'user', 'rating', 'comment')
        }),
    )
