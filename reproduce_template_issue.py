import os
import django
from django.template.loader import render_to_string
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_render():
    from products.models import Product
    
    # Create a mock product context
    # We'll just define a class to mimic the product if we don't want to hit DB, 
    # but hitting DB is fine since we are in dev environment.
    try:
        product = Product.objects.get(pk=13)
    except:
        print("Product 13 not found, using first available.")
        product = Product.objects.first()
        
    if not product:
        print("No products found to test.")
        return

    ctx = {
        'product': product,
        'user': product.owner, # Mock user
        'range_5': range(1, 6),
        'reviews': [],
        'average_rating': 4.5,
        'review_count': 10,
        'can_review': True,
    }
    
    print(f"Testing render for Product: {product.title}")
    
    try:
        rendered = render_to_string('products/product_detail.html', ctx)
        
        if '{{' in rendered and '}}' in rendered:
            print("FAILURE: Found literal '{{' and '}}' in rendered output!")
            idx = rendered.find('{{')
            snippet = rendered[max(0, idx-50):min(len(rendered), idx+50)]
            print(f"Snippet: ...{snippet}...")
        else:
            print("SUCCESS: No literal variable tags found.")
            
            # Check specifically for stock badge content
            if f"Low Stock: Only {product.stock_quantity} left!" in rendered:
                 print("Stock Badge Content: Verified (Low Stock)")
            elif "In Stock" in rendered:
                 print("Stock Badge Content: Verified (In Stock)")
            elif "Out of Stock" in rendered:
                 print("Stock Badge Content: Verified (Out of Stock)")
            else:
                 print("Stock Badge Content: NOT FOUND or Unexpected Format")
                
    except Exception as e:
        print(f"Template Rendering Error: {e}")

if __name__ == "__main__":
    test_render()
