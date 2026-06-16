import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

def delete_products():
    print("🗑️ Deleting Test Products...")
    
    # Titles seen in screenshot
    titles_to_delete = [
        'Review Product',
        'Test Jacket', 
        'Both Item', 
        'Lender Item'
    ]
    
    for title in titles_to_delete:
        products = Product.objects.filter(title__icontains=title)
        count = products.count()
        if count > 0:
            products.delete()
            print(f"✅ Deleted {count} product(s) with title containing '{title}'")
        else:
            print(f"ℹ️ No products found with title containing '{title}'")

    # Clean up test users if needed
    test_users = ['lender1', 'test_owner', 'flex_both', 'flex_lender', 'review_owner', 'review_customer', 'flex_borrower']
    print("\n👤 Checking Test Users (Optional cleanup)...")
    for username in test_users:
        users = User.objects.filter(username=username)
        if users.exists():
            # users.delete() # User didn't explicitly ask to delete users, only products. 
            # I will keep the users for now to avoid breaking other things, or delete them if I'm sure.
            # "delete thses product" -> strictly products.
            print(f"ℹ️ Found test user '{username}' (Keeping user, only deleted products)")
            
    print("\n🎉 Cleanup Complete.")

if __name__ == '__main__':
    delete_products()
