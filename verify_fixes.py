import os
import django
from django.conf import settings
from django.urls import reverse, resolve
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def verify_template_fix():
    print("--- Verifying Product List Template ---")
    try:
        # Mock context consistent with view
        from products.models import Category
        context = {
            'categories': [{'id': 1, 'name': 'Test'}, {'id': 2, 'name': 'Test2'}],
            'products': [],
            'selected_category': 1,
            'selected_size': 'M',
            'search_query': ''
        }
        rendered = render_to_string('products/product_list.html', context)
        print("✅ product_list.html rendered successfully.")
    except Exception as e:
        print(f"❌ Template Error: {e}")

def verify_url_fix():
    print("\n--- Verifying URL and View Fixes ---")
    try:
        # Check Reverse
        url = reverse('verify_booking_otp', kwargs={'pk': 123})
        print(f"✅ URL Reversed successfully: {url}")
        
        # Check Resolve
        match = resolve(url)
        print(f"✅ URL Resolved to: {match.func.__name__}")
        
        # Check View Signature
        from bookings.views import verify_booking_otp_view
        import inspect
        sig = inspect.signature(verify_booking_otp_view)
        print(f"✅ View Signature: {sig}")
        
        if 'pk' in sig.parameters:
            print("✅ View accepts 'pk'.")
        else:
             print("❌ View MISSING 'pk' argument.")

    except Exception as e:
        print(f"❌ URL/View Error: {e}")

if __name__ == "__main__":
    verify_template_fix()
    verify_url_fix()
