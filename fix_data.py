import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category
from bookings.models import Booking

def is_bad(text):
    return text and ("{{" in str(text) or "}}" in str(text) or "product." in str(text))

print("Starting Data Fix...")

# Fix Categories
for cat in Category.objects.all():
    if is_bad(cat.name):
        print(f"Fixing Category {cat.id}: {cat.name}")
        cat.name = f"Category {cat.id}"
        cat.save()

# Fix Products
titles = [
    "Classic Black Suit", "Red Evening Dress", "Leather Jacket", 
    "Designer Handbag", "Summer Floral Dress", "Denim Jacket",
    "Wool Coat", "Silk Scarf", "Running Shoes", "Evening Gown"
]

for p in Product.objects.all():
    changed = False
    
    if is_bad(p.title):
        print(f"Fixing Title for {p.id}: {p.title}")
        p.title = titles[p.id % len(titles)] if p.id else "Restored Product"
        changed = True
        
    if is_bad(p.description):
        print(f"Fixing Description for {p.id}")
        p.description = "A high-quality item available for rent. Perfect for your next event."
        changed = True
        
    if is_bad(p.price_per_day): # unlikely for float/decimal but checking
        p.price_per_day = 500.00
        changed = True

    if changed:
        p.save()

# Fix Bookings
# Assuming some booking fields might be bad? Usually bookings are created dynamically.
# But if status is charfield and has bad data:
for b in Booking.objects.all():
    if is_bad(b.status):
        print(f"Fixing Booking Status {b.id}")
        b.status = 'Pending'
        b.save()

print("Data Fix Complete.")
