
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def update_scarf_v2():
    try:
        product = Product.objects.filter(title__icontains='Silk Scarf').first()
        if product:
            print(f"Updating Scarf: {product.title}")
            product.image = 'products/silk_scarf_v2.png'
            product.save()
            print("Successfully updated Silk Scarf image (v2).")
        else:
            print("Product containing 'Silk Scarf' not found.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    update_scarf_v2()
