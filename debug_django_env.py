import os
import django
from django.conf import settings
from django.template import Template, Context

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

print(f"DB Path: {settings.DATABASES['default']['NAME']}")

try:
    p = Product.objects.get(id=19)
    print(f"Product Loaded: {p}")
    print(f"Product Title Raw: '{p.title}'")
    
    t = Template("Rendered: {{ p.title }} | Price: {{ p.price_per_day }}")
    c = Context({"p": p})
    print(t.render(c))
    
except Exception as e:
    print(f"Error: {e}")
