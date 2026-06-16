from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model"""
    
    list_display = ['username', 'email', 'role', 'first_name', 'last_name', 'is_staff', 'created_at']
    list_filter = ['role', 'is_staff', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'address', 'profile_picture')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'address', 'profile_picture')
        }),
    )


from .models import OTP

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp_code', 'is_verified', 'created_at', 'is_valid']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['user__username', 'user__email', 'otp_code']
    readonly_fields = ['created_at']
