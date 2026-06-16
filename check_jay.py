import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def check_jay():
    print("🔍 Checking User 'jay'...")
    try:
        user = User.objects.get(username='jay')
        print(f"User: {user.username}")
        print(f"Role: '{user.role}'")
        print(f"Is Customer? {user.is_customer()}")
        print(f"Is Owner? {user.is_owner()}")
        
        if user.role != 'customer':
            print("⚠️ Role is not 'customer'. Fixing...")
            user.role = 'customer'
            user.save()
            print("✅ Role updated to 'customer'.")
        else:
            print("✅ Role is already 'customer'.")
            
    except User.DoesNotExist:
        print("❌ User 'jay' not found!")

if __name__ == '__main__':
    check_jay()
