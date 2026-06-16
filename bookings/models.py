from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from users.models import User
from products.models import Product


class Booking(models.Model):
    """Booking system for product rentals"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bookings')
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    is_verified = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Return & Penalty fields
    actual_return_date = models.DateField(null=True, blank=True)
    late_days = models.IntegerField(default=0)
    penalty_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])
    
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product.title} - {self.borrower.username} ({self.status})"
    
    def save(self, *args, **kwargs):
        """Calculate total days and price before saving"""
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            self.total_days = delta.days + 1
            self.total_price = self.total_days * self.product.price_per_day
        super().save(*args, **kwargs)
    
    def is_active(self):
        """Check if booking is currently active"""
        today = timezone.now().date()
        return self.status == 'active' and self.start_date <= today <= self.end_date
