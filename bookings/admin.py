
from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin for Booking model"""
    
    list_display = ['product', 'borrower', 'start_date', 'end_date', 'status', 'is_verified', 'late_days', 'penalty_amount']
    list_filter = ['status', 'is_verified', 'start_date', 'end_date', 'created_at']
    search_fields = ['product__title', 'borrower__username', 'notes']
    list_editable = ['status']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Booking Details', {
            'fields': ('product', 'borrower', 'start_date', 'end_date')
        }),
        ('Pricing', {
            'fields': ('total_days', 'total_price')
        }),
        ('Status & Notes', {
            'fields': ('status', 'is_verified', 'notes')
        }),
        ('Return & Penalty', {
            'fields': ('actual_return_date', 'late_days', 'penalty_amount')
        }),
    )
    
    readonly_fields = ['total_days', 'total_price']
