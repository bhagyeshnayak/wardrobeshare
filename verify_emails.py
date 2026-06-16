
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from users.models import User
from products.models import Product
from bookings.models import Booking
from bookings.views import create_booking_view
from payments.views import process_payment_view
import datetime

def setup_test_data():
    print("Setting up test data...")
    # Create or get users
    owner, _ = User.objects.get_or_create(username='owner', email='owner@example.com', password='password')
    borrower, _ = User.objects.get_or_create(username='borrower', email='borrower@example.com', password='password')
    
    # Create product
    product, _ = Product.objects.get_or_create(
        title='Test Jacket',
        owner=owner,
        price_per_day=100.00,
        is_available=True,
        description="A nice jacket"
    )
    return borrower, product

def test_booking_email(borrower, product):
    print("\n--- Testing Booking Email ---")
    factory = RequestFactory()
    
    # Simulate POST request to create booking
    start_date = datetime.date.today() + datetime.timedelta(days=1)
    end_date = start_date + datetime.timedelta(days=2)
    
    data = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'notes': 'Test booking'
    }
    
    request = factory.post(f'/bookings/create/{product.id}/', data)
    request.user = borrower
    
    # Add middleware support for messages
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    messages = MessageMiddleware(lambda x: None)
    messages.process_request(request)

    response = create_booking_view(request, product.id)
    print(f"Response status: {response.status_code}")
    
    # Check if booking was created
    booking = Booking.objects.filter(borrower=borrower, product=product).first()
    if booking:
        print(f"Booking created: ID {booking.id}")
        return booking
    else:
        print("Failed to create booking")
        return None

def test_payment_email(borrower, booking):
    print("\n--- Testing Payment Email ---")
    if not booking:
        print("No booking to pay for.")
        return

    factory = RequestFactory()
    request = factory.post(f'/payments/process/{booking.id}/')
    request.user = borrower
    
    # Add middleware support for messages
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    messages = MessageMiddleware(lambda x: None)
    messages.process_request(request)

    response = process_payment_view(request, booking.id)
    print(f"Response status: {response.status_code}")

if __name__ == "__main__":
    try:
        borrower, product = setup_test_data()
        booking = test_booking_email(borrower, product)
        test_payment_email(borrower, booking)
    except Exception as e:
        print(f"Error: {e}")
