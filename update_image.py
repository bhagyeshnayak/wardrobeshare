import os
import django
import shutil
from django.core.files import File

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

# Source image path (Artifact)
source_path = r"C:\Users\NAYAK BHAGYESH\.gemini\antigravity\brain\3de49e3a-201a-4627-b3fb-21aef8b0e88f\media__1770375209524.png"
target_name = "tuxedo_real.png"

try:
    # Find product
    product = Product.objects.get(title__icontains="Tuxedo")
    print(f"Found product: {product.title} (ID: {product.id})")
    
    # Copy file to media root (optional, or just let Django handle it)
    # Django FileField saves it to media/products/ usually
    
    with open(source_path, 'rb') as f:
        product.image.save(target_name, File(f), save=True)
        
    print(f"Successfully updated image for {product.title}")
    
except Product.DoesNotExist:
    # Fallback to "Suit" if Tuxedo not found
    try:
        product = Product.objects.get(title__icontains="Suit")
        print(f"Tuxedo not found, updating closest match: {product.title}")
        with open(source_path, 'rb') as f:
            product.image.save(target_name, File(f), save=True)
        print(f"Successfully updated image for {product.title}")
    except Product.DoesNotExist:
        print("Product not found!")

except Exception as e:
    print(f"Error: {e}")
