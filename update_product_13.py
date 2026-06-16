import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def update_product():
    try:
        product = Product.objects.get(pk=13)
        print(f"Current Product: {product.title} - {product.description}")
        
        product.title = "T-Shirt"
        product.description = "Cotton T-Shirt for daily wear"
        # price_per_day is already 50.00, but ensuring it stays that way (or just not touching it)
        # product.price_per_day = Decimal('50.00') 
        
        product.save()
        
        updated_product = Product.objects.get(pk=13)
        print(f"Updated Product: {updated_product.title} - {updated_product.description}")
        print("Update Successful.")
        
    except Product.DoesNotExist:
        print("Product with ID 13 does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    update_product()
