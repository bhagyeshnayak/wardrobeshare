
import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def fix_product_images():
    print("Fixing product images...")
    
    # 1. Fix "Test Jacket"
    try:
        jacket = Product.objects.get(title='Test Jacket')
        # Check if it already has a valid image
        if not jacket.image:
            image_path = os.path.join(django.conf.settings.MEDIA_ROOT, 'products', 'leather_jacket.jpg')
            if os.path.exists(image_path):
                # We can just set the path relative to MEDIA_ROOT
                jacket.image = 'products/leather_jacket.jpg'
                jacket.save()
                print("✅ Assigned 'leather_jacket.jpg' to 'Test Jacket'")
            else:
                print("❌ 'leather_jacket.jpg' not found in media/products")
        else:
            print(f"ℹ️ 'Test Jacket' already has image: {jacket.image}")
    except Product.DoesNotExist:
        print("⚠️ Product 'Test Jacket' not found")

    # 2. Fix "OTP Test Product" (Give it a suit or something)
    try:
        otp_prod = Product.objects.get(title='OTP Test Product')
        if not otp_prod.image:
            image_path = os.path.join(django.conf.settings.MEDIA_ROOT, 'products', 'black_suit.jpg')
            if os.path.exists(image_path):
                otp_prod.image = 'products/black_suit.jpg'
                otp_prod.save()
                print("✅ Assigned 'black_suit.jpg' to 'OTP Test Product'")
            else:
                 print("❌ 'black_suit.jpg' not found in media/products")
    except Product.DoesNotExist:
        print("⚠️ Product 'OTP Test Product' not found")

if __name__ == "__main__":
    fix_product_images()
