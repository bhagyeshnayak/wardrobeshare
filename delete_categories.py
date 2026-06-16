import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Category

def delete_test_categories():
    print("🗑️ Deleting Test Categories...")
    
    categories_to_delete = [
        "Flex Cat",
        "Test Category",
        "Review Cat"
    ]
    
    for cat_name in categories_to_delete:
        try:
            category = Category.objects.get(name__iexact=cat_name)
            category.delete()
            print(f"✅ Successfully deleted category: '{category.name}'")
        except Category.DoesNotExist:
            print(f"⚠️ Category '{cat_name}' not found.")
        except Exception as e:
            print(f"❌ Error deleting '{cat_name}': {str(e)}")

    print("\n🎉 Cleanup complete.")

if __name__ == '__main__':
    delete_test_categories()
