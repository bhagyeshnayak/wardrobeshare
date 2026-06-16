import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def list_users():
    users = User.objects.all()
    print(f"Total Users: {users.count()}")
    for u in users:
        print(f"ID: {u.id}, Username: '{u.username}', Email: '{u.email}'")

if __name__ == "__main__":
    list_users()
