import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def rename_otp_owner():
    try:
        user = User.objects.get(username='otp_owner')
        print(f"Found user: {user.username}")
        
        # Check if 'Jack' is free
        if User.objects.filter(username='Jack').exists():
            print("Username 'Jack' is already taken!")
            return
            
        user.username = 'Jack'
        user.save()
        print("Successfully renamed user 'otp_owner' to 'Jack'.")
        
    except User.DoesNotExist:
        print("User 'otp_owner' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    rename_otp_owner()
