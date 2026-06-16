from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model with role-based access"""
    
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('customer', 'Customer'),
        ('both', 'Both'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_owner(self):
        """Check if user has owner privileges"""
        return self.role in ['owner', 'both']
    
    def is_customer(self):
        """Check if user has customer privileges"""
        return self.role in ['customer', 'both']
        
    def can_lend(self):
        return self.is_owner()
        
    def can_borrow(self):
        return self.is_customer()


class OTP(models.Model):
    """OTP Model for Email Verification"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_valid(self):
        from django.utils import timezone
        import datetime
        # Check if OTP is less than 5 minutes old
        return timezone.now() < self.created_at + datetime.timedelta(minutes=5)
    
    def __str__(self):
        return f"OTP for {self.user.username} - {self.otp_code}"
