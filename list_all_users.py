
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User

print("\n--- Listing All Users ---")
for u in User.objects.all():
    print(f"User: {u.username} (Email: {u.email})")
