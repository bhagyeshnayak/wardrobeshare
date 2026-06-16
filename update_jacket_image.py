import os
import django
from django.core.files import File

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

# Source image path (Artifact)
source_path = r"C:\Users\NAYAK BHAGYESH\.gemini\antigravity\brain\3de49e3a-201a-4627-b3fb-21aef8b0e88f\media__1770376218963.png"
target_name = "vintage_denim_jacket_real.png"

try:
    # Find product by partial title
    product = Product.objects.filter(title__icontains="Vintage Denim Jacket").first()
    
    if not product:
         product = Product.objects.filter(title__icontains="Denim Jacket").first()
         
    if product:
        print(f"Found product: {product.title} (ID: {product.id})")
        with open(source_path, 'rb') as f:
            product.image.save(target_name, File(f), save=True)
        print(f"Successfully updated image for {product.title}")
    else:
        print("Product 'Vintage Denim Jacket' not found!")

except Exception as e:
    print(f"Error: {e}")
