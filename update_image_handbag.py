import os
import django
import shutil
from django.core.files import File
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def update_image():
    print("🖼️ Updating Product Image...")
    
    # 1. Find Product
    title_query = "Premium Designer Handbag"
    product = Product.objects.filter(title__icontains=title_query).first()
    
    if not product:
        # Fallback search if exact match fails
        product = Product.objects.filter(title__icontains="Handbag").first()

    if not product:
        print(f"❌ Product matching '{title_query}' not found!")
        return

    print(f"✅ Found product: {product.title} (ID: {product.id})")
    
    # 2. Source Image Path
    source_path = r"C:/Users/NAYAK BHAGYESH/.gemini/antigravity/brain/87747053-89a6-44fa-82fe-295fa2180adf/uploaded_media_0_1770020835174.jpg"
    
    if not os.path.exists(source_path):
        print(f"❌ Source image not found at: {source_path}")
        return

    # 3. Update Image
    with open(source_path, 'rb') as f:
        new_filename = 'designer_handbag.jpg'
        product.image.save(new_filename, File(f), save=True)
        
    print(f"🎉 Image updated successfully for '{product.title}'")

if __name__ == '__main__':
    update_image()
