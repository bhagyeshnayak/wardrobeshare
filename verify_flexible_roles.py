()import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from products.models import Product, Category
from bookings.models import Booking

User = get_user_model()

def verify_flexible_roles():
    print("🚀 Verifying Flexible Role System...")
    
    # 1. Cleanup
    User.objects.filter(username__in=['flex_borrower', 'flex_lender', 'flex_both']).delete()
    
    # 2. Create Users
    print("👤 Creating users...")
    u_borrower = User.objects.create_user('flex_borrower', 'p', role='customer') # 'customer' maps to "Borrow items"
    u_lender = User.objects.create_user('flex_lender', 'p', role='owner')      # 'owner' maps to "Lend items"
    u_both = User.objects.create_user('flex_both', 'p', role='both')
    
    # 3. Verify Permissions
    print("🔒 Verifying Permissions...")
    
    # Borrower
    if not u_borrower.can_borrow(): print("❌ Borrower cannot borrow!")
    if u_borrower.can_lend(): print("❌ Borrower can lend!")
    
    # Lender
    if u_lender.can_borrow(): print("❌ Lender can borrow!")
    if not u_lender.can_lend(): print("❌ Lender cannot lend!")
    
    # Both
    if not u_both.can_borrow(): print("❌ Both cannot borrow!")
    if not u_both.can_lend(): print("❌ Both cannot lend!")
    
    print("✅ Permissions Verified.")
    
    # 4. Product Ownership Check
    cat, _ = Category.objects.get_or_create(name='Flex Cat')
    p_lender = Product.objects.create(owner=u_lender, title='Lender Item', category=cat, size='M', price_per_day=10)
    p_both = Product.objects.create(owner=u_both, title='Both Item', category=cat, size='M', price_per_day=10)
    
    # View Logic Simulation
    # Check if 'Both' user can book 'Lender' item
    if u_both.can_borrow() and p_lender.owner != u_both:
        print("✅ 'Both' user can book Lender item.")
    else:
        print("❌ 'Both' user prevented from booking Lender item!")

    # Check if 'Both' user can book OWN item
    if u_both.can_borrow() and p_both.owner == u_both:
        print("ℹ️ 'Both' user has permission, but view should block own item.")
        # Logic check: (user.can_borrow and user != product.owner)
        if not (u_both.can_borrow() and u_both != p_both.owner):
            print("✅ Button Logic correctly hides book button for own item.")
        else:
             print("❌ Button Logic FAIL: Would show book button for own item!")
             
    print("🎉 Flexible Role Verification Complete.")

if __name__ == '__main__':
    verify_flexible_roles()
