
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def remove_test_names():
    print("Cleaning up product names...")
    
    products = Product.objects.filter(title__icontains='Test')
    
    for p in products:
        print(f"Found: {p.title}")
        if 'jacket' in p.title.lower():
            p.title = 'Leather Jacket'
            p.description = "Premium quality leather jacket, perfect for any casual or semi-formal occasion."
            p.save()
            print(f"✅ Renamed to 'Leather Jacket'")
        elif 'otp' in p.title.lower():
            # This should have been renamed already, but just in case
            p.title = 'Red Evening Dress'
            p.save()
            print(f"✅ Renamed to 'Red Evening Dress'")
        else:
            # Fallback for generic "Test" items
            new_title = p.title.replace('Test', '').replace('test', '').strip()
            if not new_title: new_title = "Product item"
            p.title = new_title
            p.save()
            print(f"✅ Renamed to '{new_title}'")

if __name__ == "__main__":
    remove_test_names()
