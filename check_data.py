
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from products.models import Category

print("Users:", [u.username for u in User.objects.all()])
print("Categories:", [c.name for c in Category.objects.all()])
