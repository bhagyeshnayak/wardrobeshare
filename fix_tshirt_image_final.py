import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product
from django.conf import settings

def finalize_tshirt_image():
    product_id = 13
    # The file we successfully assigned previously
    source_file = os.path.join(settings.MEDIA_ROOT, 'products', 'tshirt_13.png') 
    # The target standard file
    target_file = os.path.join(settings.MEDIA_ROOT, 'products', 'tshirt.png')
    
    if os.path.exists(source_file):
        print(f"Moving {source_file} -> {target_file}")
        # Move/Rename (overwrite if exists)
        shutil.move(source_file, target_file)
    else:
        # Fallback if source missing (maybe we already moved it?)
        print(f"Source {source_file} not found. Checking target...")
        if not os.path.exists(target_file):
             print(f"Error: Neither {source_file} nor {target_file} found!")
             return

    try:
        product = Product.objects.get(pk=product_id)
        product.image = 'products/tshirt.png'
        product.save()
        print(f"Product {product.title} updated to use image: {product.image}")
        print("Final Verification: Image field is set.")
    except Product.DoesNotExist:
        print("Product 13 not found.")

if __name__ == "__main__":
    finalize_tshirt_image()
