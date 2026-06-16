import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def find_specific_users():
    jack = User.objects.filter(username__icontains='Jack').first()
    otp_owner = User.objects.filter(username='otp_owner').first()
    
    if jack:
        print(f"User 'Jack' found: ID {jack.id}, Username: '{jack.username}'")
    else:
        print("User 'Jack' NOT found.")
        
    if otp_owner:
        print(f"User 'otp_owner' found: ID {otp_owner.id}, Username: '{otp_owner.username}'")
    else:
        print("User 'otp_owner' NOT found.")

if __name__ == "__main__":
    find_specific_users()
