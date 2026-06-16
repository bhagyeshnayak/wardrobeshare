
import os
import django
import sys

# Add project root to path
sys.path.append('c:\\Users\\NAYAK BHAGYESH\\Desktop\\wardrobeshare')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from products.models import Product

p = Product.objects.get(id=13)
print(f"Current Image: '{p.image}'")
print(f"Current Image Field: {p.image.name if p.image else 'None'}")

if p.image:
    print(f"URL: {p.image.url}")

# Only update if we plan to change it, but for now just inspecting.
