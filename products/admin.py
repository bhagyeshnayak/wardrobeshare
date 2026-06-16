from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin for Category model"""
    
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin for Product model"""
    
    list_display = ['title', 'owner', 'category', 'size', 'stock_quantity', 'price_per_day', 'is_available', 'created_at']
    list_filter = ['category', 'size', 'condition', 'is_available', 'created_at']
    search_fields = ['title', 'description', 'brand', 'owner__username']
    list_editable = ['is_available', 'stock_quantity']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('owner', 'category', 'title', 'description')
        }),
        ('Product Details', {
            'fields': ('size', 'condition', 'brand', 'color', 'image')
        }),
        ('Pricing & Availability', {
            'fields': ('price_per_day', 'is_available', 'stock_quantity')
        }),
    )
