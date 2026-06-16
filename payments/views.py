from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Payment
from bookings.models import Booking

@login_required
def make_payment_view(request, booking_id):
    """View to show payment form"""
    booking = get_object_or_404(Booking, pk=booking_id)
    
    # Security check: only borrower can pay
    if request.user != booking.borrower:
        messages.error(request, "You are not authorized to pay for this booking.")
        return redirect('dashboard')
        
    # Check if already paid
    if hasattr(booking, 'payment') and booking.payment.status == 'completed':
        messages.info(request, "This booking is already paid.")
        return redirect('booking_detail', pk=booking.id)
        
    context = {
        'booking': booking,
        'amount': booking.total_price
    }
    return render(request, 'payments/make_payment.html', context)

import stripe
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_checkout_session(request, booking_id):
    """Create Stripe Checkout Session"""
    booking = get_object_or_404(Booking, pk=booking_id)
    
    if request.method == 'POST':
        try:
            # Create a Checkout Session
            domain_url = request.build_absolute_uri('/')[:-1] # Get base URL
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': f"Booking: {booking.product.title}",
                        },
                        'unit_amount': int(booking.total_price * 100), # Amount in paise
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=domain_url + reverse('payment_success') + f'?booking_id={booking.id}&session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=domain_url + reverse('payment_cancel') + f'?booking_id={booking.id}',
                customer_email=request.user.email,
            )
            return redirect(checkout_session.url)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('make_payment', booking_id=booking.id)
            
    return redirect('make_payment', booking_id=booking.id)

@login_required
def payment_success_view(request):
    """Handle successful payment from Stripe"""
    booking_id = request.GET.get('booking_id')
    session_id = request.GET.get('session_id')
    
    booking = get_object_or_404(Booking, pk=booking_id)
    
    # Optional: Verify session with Stripe
    # session = stripe.checkout.Session.retrieve(session_id)
    # if session.payment_status != 'paid': ...
    
    # Check if already processed
    if hasattr(booking, 'payment') and booking.payment.status == 'completed':
        messages.info(request, "Payment already recorded.")
        return redirect('booking_detail', pk=booking.id)

    # Process Payment Record
    Payment.objects.create(
        booking=booking,
        user=request.user,
        amount=booking.total_price,
        payment_method='stripe',
        status='completed',
        transaction_id=session_id,
        notes="Stripe Payment Successful"
    )
    
    # Update Booking & Stock
    booking.status = 'confirmed'
    booking.save()
    
    product = booking.product
    product.stock_quantity -= 1
    product.save()

    # Send Email
    try:
        subject = 'Payment Successful – WardrobeShare'
        message = f"""
        Dear {booking.borrower.username},
        
        Your payment for Booking ID #{booking.id} was successful!
        Amount: ₹{booking.total_price}
        Transaction ID: {session_id}
        
        Thank you for your booking!
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.borrower.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

    messages.success(request, "Payment successful! Booking confirmed.")
    return redirect('booking_detail', pk=booking.id)

@login_required
def payment_cancel_view(request):
    """Handle payment cancellation"""
    booking_id = request.GET.get('booking_id')
    messages.warning(request, "Payment cancelled. You can try again.")
    return redirect('make_payment', booking_id=booking_id)
