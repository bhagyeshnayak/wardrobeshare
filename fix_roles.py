import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def check_and_fix_roles():
    print("🔍 Checking User Roles...")
    users = User.objects.all()
    for user in users:
        print(f"User: {user.username}, Role: '{user.role}'")
        
        if user.role == 'lender':
            print(f"  -> Updating {user.username} to 'owner'")
            user.role = 'owner'
            user.save()
        elif user.role == 'borrower':
            print(f"  -> Updating {user.username} to 'customer'")
            user.role = 'customer'
            user.save()
        elif user.role == 'both':
             print(f"  -> Updating {user.username} to 'customer' (defaulting from both)")
             user.role = 'customer'
             user.save()
             
    print("✅ Role update check complete.")

if __name__ == '__main__':
    check_and_fix_roles()
