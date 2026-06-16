import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category
from django.db.models import Q

def debug_filters():
    print("--- Debugging Filters ---")
    
    # 1. Check Categories
    categories = Category.objects.all()
    print(f"Categories Count: {categories.count()}")
    for cat in categories:
        print(f"  - [{cat.id}] {cat.name}")

    # 2. Check Products
    all_products = Product.objects.all()
    print(f"Total Products: {all_products.count()}")
    
    # 3. Test filtering
    print("\n--- Testing Filter Logic ---")
    
    # Simulate View Logic
    category_param = "1" # Assuming 1 exists
    size_param = "M"     # Assuming M exists
    
    print(f"Filtering with Category={category_param} AND Size={size_param}")
    
    qs = Product.objects.filter(is_available=True)
    initial_count = qs.count()
    print(f"Available Products: {initial_count}")
    
    # Filter Category
    if category_param.isdigit():
        qs = qs.filter(category_id=int(category_param))
        print(f"After Category Filter ({category_param}): {qs.count()}")
        
    # Filter Size
    qs = qs.filter(size=size_param)
    print(f"After Size Filter ({size_param}): {qs.count()}")
    
    if qs.exists():
        print("Found products:")
        for p in qs:
            print(f"  - {p.title} (Cat: {p.category.id}, Size: {p.size})")
    else:
        print("No products found with this combination.")
        
    # Check if any products exist with this combo regardless of is_available
    raw_check = Product.objects.filter(category_id=int(category_param), size=size_param)
    print(f"\nRaw DB Check (Ignoring is_available): {raw_check.count()}")

if __name__ == "__main__":
    debug_filters()
