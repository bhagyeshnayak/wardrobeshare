import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def show_product():
    try:
        product = Product.objects.get(pk=13)
        print("--- Product ID 13 Status ---")
        print(f"Title: {product.title}")
        print(f"Image Path: {product.image}")
        print(f"Image URL (if reachable): {product.image.url if product.image else 'No Image'}")
        print("----------------------------")
    except Product.DoesNotExist:
        print("Product 13 not found.")

if __name__ == "__main__":
    show_product()
