import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def assign_tuxedo_image():
    # Source and Destination paths
    source_name = 'black_suit.jpg'
    dest_name = 'real_tuxedo_suit.jpg'
    
    media_root = os.path.join(os.getcwd(), 'media', 'products')
    source_path = os.path.join(media_root, source_name)
    dest_path = os.path.join(media_root, dest_name)
    
    # Check if source exists
    if not os.path.exists(source_path):
        print(f"Error: Source image {source_name} not found in {media_root}")
        # Try alternative
        source_name = 'classic_black_suit.jpg'
        source_path = os.path.join(media_root, source_name)
        if not os.path.exists(source_path):
            print("Error: No suitable fallback image found.")
            return

    # Copy file
    print(f"Copying {source_name} to {dest_name}...")
    shutil.copy2(source_path, dest_path)
    
    # Update Database
    try:
        product = Product.objects.get(title='Tuxedo')
        product.image = f'products/{dest_name}'
        product.save()
        print(f"✅ Success: Assigned products/{dest_name} to '{product.title}'")
    except Product.DoesNotExist:
        print("Error: Product 'Tuxedo' not found.")

if __name__ == '__main__':
    assign_tuxedo_image()
