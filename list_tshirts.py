import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def list_tshirts():
    products = Product.objects.filter(title__icontains='T-Shirt')
    print(f"Found {products.count()} T-Shirt product(s):")
    for p in products:
        print(f"ID: {p.id}, Title: '{p.title}', Image: '{p.image}', Has Image: {bool(p.image)}")

if __name__ == "__main__":
    list_tshirts()
