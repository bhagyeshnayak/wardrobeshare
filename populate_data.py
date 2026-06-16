"""
Script to populate the database with sample data for testing
"""
import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.files import File
from users.models import User
from products.models import Category, Product
from bookings.models import Booking
from reviews.models import Review
from datetime import date, timedelta

# Create categories
categories_data = [
    {'name': 'Dresses', 'description': 'Elegant dresses for all occasions'},
    {'name': 'Suits', 'description': 'Formal and casual suits'},
    {'name': 'Accessories', 'description': 'Bags, jewelry, and more'},
    {'name': 'Shoes', 'description': 'Footwear for every style'},
    {'name': 'Jackets', 'description': 'Coats and jackets'},
]

print("Creating categories...")
for cat_data in categories_data:
    Category.objects.get_or_create(name=cat_data['name'], defaults=cat_data)

# Create sample users
print("Creating sample users...")
lender1, _ = User.objects.get_or_create(
    username='lender1',
    defaults={
        'email': 'lender1@example.com',
        'role': 'lender',
        'phone': '9876543210'
    }
)
lender1.set_password('password123')
lender1.save()

borrower1, _ = User.objects.get_or_create(
    username='borrower1',
    defaults={
        'email': 'borrower1@example.com',
        'role': 'borrower',
        'phone': '9876543211'
    }
)
borrower1.set_password('password123')
borrower1.save()

both_user, _ = User.objects.get_or_create(
    username='fashionista',
    defaults={
        'email': 'fashionista@example.com',
        'role': 'both',
        'phone': '9876543212'
    }
)
both_user.set_password('password123')
both_user.save()

# Create sample products
print("Creating sample products...")
products_data = [
    {
        'title': 'Elegant Red Evening Dress',
        'description': 'Beautiful red evening dress perfect for parties and special occasions. Designer brand, excellent condition.',
        'category': 'Dresses',
        'size': 'M',
        'condition': 'like_new',
        'brand': 'Zara',
        'color': 'Red',
        'price_per_day': 500,
        'owner': lender1,
        'image_file': 'red_evening_dress.jpg'
    },
    {
        'title': 'Classic Black Suit',
        'description': 'Professional black suit ideal for business meetings and formal events.',
        'category': 'Suits',
        'size': 'L',
        'condition': 'good',
        'brand': 'Raymond',
        'color': 'Black',
        'price_per_day': 800,
        'owner': lender1,
        'image_file': 'black_suit.jpg'
    },
    {
        'title': 'Designer Leather Jacket',
        'description': 'Stylish leather jacket for a cool, edgy look. Perfect for winter.',
        'category': 'Jackets',
        'size': 'M',
        'condition': 'new',
        'brand': 'Levi\'s',
        'color': 'Brown',
        'price_per_day': 600,
        'owner': both_user,
        'image_file': 'leather_jacket.jpg'
    },
    {
        'title': 'Floral Summer Dress',
        'description': 'Light and breezy floral dress perfect for summer outings.',
        'category': 'Dresses',
        'size': 'S',
        'condition': 'good',
        'brand': 'H&M',
        'color': 'Multicolor',
        'price_per_day': 300,
        'owner': both_user,
        'image_file': 'floral_summer_dress.jpg'
    },
    {
        'title': 'Premium Designer Handbag',
        'description': 'Luxury handbag from a premium brand. Perfect for special occasions.',
        'category': 'Accessories',
        'size': 'M',
        'condition': 'like_new',
        'brand': 'Michael Kors',
        'color': 'Beige',
        'price_per_day': 400,
        'owner': lender1,
        'image_file': 'designer_handbag.jpg'
    },
]


# Get base directory and media path
BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR / 'media' / 'products'

for prod_data in products_data:
    category = Category.objects.get(name=prod_data.pop('category'))
    image_filename = prod_data.pop('image_file', None)
    
    # Check if product already exists
    product, created = Product.objects.get_or_create(
        title=prod_data['title'],
        defaults={**prod_data, 'category': category}
    )
    
    # Assign image if product was just created and image file exists
    if created and image_filename:
        image_path = MEDIA_DIR / image_filename
        if image_path.exists():
            with open(image_path, 'rb') as img_file:
                product.image.save(image_filename, File(img_file), save=True)
            print(f"  ✅ {prod_data['title']} - Image assigned")
        else:
            print(f"  ⚠️  {prod_data['title']} - Image not found: {image_filename}")
    elif not created:
        print(f"  ℹ️  {prod_data['title']} - Already exists")


print("\n✅ Sample data created successfully!")
print("\n📊 Database Summary:")
print(f"   Users: {User.objects.count()}")
print(f"   Categories: {Category.objects.count()}")
print(f"   Products: {Product.objects.count()}")
print("\n👤 Test Accounts:")
print("   Admin: username='admin', password='admin123'")
print("   Lender: username='lender1', password='password123'")
print("   Borrower: username='borrower1', password='password123'")
print("   Both: username='fashionista', password='password123'")
print("\n🌐 Access the application at: http://127.0.0.1:8000/")
print("🔧 Admin panel at: http://127.0.0.1:8000/admin/")
