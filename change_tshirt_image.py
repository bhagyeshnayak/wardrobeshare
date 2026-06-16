import os
import shutil
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product
from django.conf import settings

def change_image():
    # Configuration
    product_id = 13
    source_image_path = r'C:/Users/NAYAK BHAGYESH/.gemini/antigravity/brain/5e30ee8c-ce08-4ba7-811e-7eff2b244f40/uploaded_media_1769674090165.png'
    
    # We use a new filename to avoid browser caching issues with the old name
    new_filename = 'tshirt_new.png'
    
    # Ensure media/products directory exists
    products_media_dir = os.path.join(settings.MEDIA_ROOT, 'products')
    os.makedirs(products_media_dir, exist_ok=True)
    
    destination_path = os.path.join(products_media_dir, new_filename)
    
    try:
        product = Product.objects.get(pk=product_id)
        print(f"Product Found: {product.title}")
        print(f"Old Image: {product.image}")
        
        # Copy the file
        print(f"Copying new image from '{source_image_path}' to '{destination_path}'...")
        shutil.copy2(source_image_path, destination_path)
        print("Image copied successfully.")
        
        # Update the product record
        relative_path = f'products/{new_filename}'
        product.image = relative_path
        product.save()
        
        # Verify
        updated_product = Product.objects.get(pk=product_id)
        print(f"New Image set to: {updated_product.image}")
        print("Update Successful!")
        
    except Product.DoesNotExist:
        print(f"Product with ID {product_id} does not exist!")
    except FileNotFoundError:
        print(f"Source file not found at: {source_image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    change_image()
