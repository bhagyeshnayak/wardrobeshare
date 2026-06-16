import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def check_black_suit():
    try:
        product = Product.objects.filter(title__icontains='Black Suit').first()
        if product:
            print(f"Product: {product.title} (ID: {product.id})")
            print(f"Image Field: '{product.image}'")
            print(f"Image URL: {product.image.url if product.image else 'None'}")
            print(f"Stock: {product.stock_quantity}")
        else:
            print("Classic Black Suit not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_black_suit()
