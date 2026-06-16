
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

print("\n--- Product Image Inspection ---")
for p in Product.objects.all():
    print(f"ID: {p.id}")
    print(f"Title: {p.title}")
    if p.image:
        print(f"Image Field: {p.image}")
        print(f"Image URL: {p.image.url}")
        # Check if file exists
        full_path = p.image.path
        exists = os.path.exists(full_path)
        print(f"File Path: {full_path}")
        print(f"Exists on Disk: {'✅ YES' if exists else '❌ NO'}")
    else:
        print("Image Field: None")
    print("-" * 30)
