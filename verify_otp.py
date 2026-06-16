
import os
import django
from django.conf import settings
from django.test import RequestFactory
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User, OTP
from products.models import Product
from bookings.models import Booking
from bookings.views import create_booking_view, verify_booking_otp_view
import datetime

def setup_test_data():
    print("Setting up test data...")
    owner, _ = User.objects.get_or_create(username='otp_owner', email='owner@example.com', password='password')
    borrower, _ = User.objects.get_or_create(username='otp_borrower', email='borrower@example.com', password='password')
    
    product, _ = Product.objects.get_or_create(
        title='OTP Test Product',
        owner=owner,
        price_per_day=50.00,
        is_available=True,
        description="OTP Testing"
    )
    return borrower, product

def test_otp_flow(borrower, product):
    print("\n--- Testing OTP Flow ---")
    factory = RequestFactory()
    
    # 1. Create Booking (Initiate OTP)
    print("1. Initiating Booking...")
    start_date = datetime.date.today() + datetime.timedelta(days=10)
    end_date = start_date + datetime.timedelta(days=2)
    
    data = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'notes': 'OTP Flow Test'
    }
    
    request = factory.post(f'/bookings/create/{product.id}/', data)
    request.user = borrower
    
    # Middleware
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    messages = MessageMiddleware(lambda x: None)
    messages.process_request(request)

    response = create_booking_view(request, product.id)
    print(f"   Response status: {response.status_code}")
    
    # Check if booking exists (unverified)
    booking = Booking.objects.filter(borrower=borrower, product=product).order_by('-created_at').first()
    if not booking:
        print("❌ Failed to create booking")
        return
    print(f"   Booking created (ID {booking.id}). Verified: {booking.is_verified}")

    # 2. Get OTP from DB
    otp_record = OTP.objects.filter(user=borrower, is_verified=False).order_by('-created_at').first()
    if not otp_record:
        print("❌ No OTP generated!")
        return
    print(f"   OTP Generated: {otp_record.otp_code}")

    # 3. Verify OTP
    print("2. Verifying OTP...")
    verify_data = {'otp_code': otp_record.otp_code}
    verify_request = factory.post(f'/bookings/verify/{booking.id}/', verify_data)
    verify_request.user = borrower
    
    # Middleware
    middleware.process_request(verify_request)
    verify_request.session.save()
    messages.process_request(verify_request)
    
    verify_response = verify_booking_otp_view(verify_request, booking.id)
    print(f"   Verify Response status: {verify_response.status_code}")
    
    # Check if booking is now verified
    booking.refresh_from_db()
    otp_record.refresh_from_db()
    
    print(f"   Booking Verified: {booking.is_verified}")
    print(f"   OTP Used: {otp_record.is_verified}")
    
    if booking.is_verified and otp_record.is_verified:
        print("✅ OTP Flow SUCCESS!")
    else:
        print("❌ OTP Flow FAILED!")

if __name__ == "__main__":
    try:
        borrower, product = setup_test_data()
        test_otp_flow(borrower, product)
    except Exception as e:
        print(f"Error: {e}")
