from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class Category(models.Model):
    """Product categories for wardrobe items"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
  

    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Wardrobe items available for sharing"""
    stock_quantity = models.PositiveIntegerField(default=1)
    
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]
    
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    title = models.CharField(max_length=200)
    description = models.TextField()
    size = models.CharField(max_length=3, choices=SIZE_CHOICES)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='good')
    brand = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.owner.username}"
    
    def get_average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0

    @property
    def is_out_of_stock(self):
        return self.stock_quantity == 0

    @property
    def is_low_stock(self):
        return 0 < self.stock_quantity <= 2
