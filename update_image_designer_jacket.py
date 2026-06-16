import os
import django
from django.core.files import File

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def update_image():
    print("🖼️ Updating Product Image...")
    
    # 1. Find Product
    title_query = "Designer Leather Jacket"
    product = Product.objects.filter(title__icontains=title_query).first()
    
    if not product:
        # Fallback
        product = Product.objects.filter(title__icontains="Leather Jacket").first()

    if not product:
        print(f"❌ Product matching '{title_query}' not found!")
        return

    print(f"✅ Found product: {product.title} (ID: {product.id})")
    
    # 2. Source Image Path
    source_path = r"C:/Users/NAYAK BHAGYESH/.gemini/antigravity/brain/87747053-89a6-44fa-82fe-295fa2180adf/uploaded_media_0_1770021258775.jpg"
    
    if not os.path.exists(source_path):
        print(f"❌ Source image not found at: {source_path}")
        return

    # 3. Update Image
    with open(source_path, 'rb') as f:
        new_filename = 'designer_leather_jacket_v2.jpg'
        product.image.save(new_filename, File(f), save=True)
        
    print(f"🎉 Image updated successfully for '{product.title}'")

if __name__ == '__main__':
    update_image()
