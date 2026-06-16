
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User

def rename_users():
    print("Renaming test users...")
    
    # Rename otp_owner
    try:
        u = User.objects.get(username='otp_owner')
        u.username = 'SarahStyles'
        u.first_name = 'Sarah'
        u.last_name = 'Styles'
        u.save()
        print("✅ Renamed 'otp_owner' to 'SarahStyles'")
    except User.DoesNotExist:
        print("ℹ️ 'otp_owner' not found")

    # Rename otp_borrower
    try:
        u = User.objects.get(username='otp_borrower')
        u.username = 'MikeRenter'
        u.first_name = 'Mike'
        u.last_name = 'Renter'
        u.save()
        print("✅ Renamed 'otp_borrower' to 'MikeRenter'")
    except User.DoesNotExist:
        print("ℹ️ 'otp_borrower' not found")

if __name__ == "__main__":
    rename_users()
