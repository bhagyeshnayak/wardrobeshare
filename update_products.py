
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def update_products():
    print("Updating products...")
    
    # 1. Ensure Jacket is correct
    try:
        jacket = Product.objects.get(title='Test Jacket')
        jacket.image = 'products/leather_jacket.jpg'
        jacket.save()
        print("✅ Updated 'Test Jacket' image")
    except Product.DoesNotExist:
        print("⚠️ Product 'Test Jacket' not found")

    # 2. Change "OTP Test Product" (Black Suit) to "Red Evening Dress" (closest to 'red suit')
    # User asked for "red suit", but we only have "red_evening_dress.jpg". 
    # Converting the black suit placeholder to the red dress item.
    try:
        otp_prod = Product.objects.get(title='OTP Test Product')
        otp_prod.title = 'Red Evening Dress'
        otp_prod.description = 'Elegant red evening dress for special occasions.'
        otp_prod.image = 'products/red_evening_dress.jpg'
        otp_prod.save()
        print("✅ Updated 'OTP Test Product' to 'Red Evening Dress'")
    except Product.DoesNotExist:
        # Try finding by ID 12 if title changed
        try:
            p = Product.objects.get(id=12)
            p.title = 'Red Evening Dress'
            p.image = 'products/red_evening_dress.jpg'
            p.save()
            print("✅ Updated Product ID 12 to 'Red Evening Dress'")
        except Product.DoesNotExist:
             print("⚠️ Product 'OTP Test Product' not found")

if __name__ == "__main__":
    update_products()
