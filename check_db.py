import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

print("Checking Product Titles:")
for p in Product.objects.all():
    print(f"ID: {p.id} | Title: '{p.title}' | Type: {type(p.title)}")
    if "{{" in p.title:
        print(f"!!! FOUND RAW TEMPLATE VAR IN TITLE FOR ID {p.id} !!!")
