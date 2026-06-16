from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from .models import Booking
from products.models import Product
from users.models import OTP
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.utils import timezone
import random
from users.decorators import customer_required

@login_required
@customer_required
def create_booking_view(request, product_id):
    """Create a new booking and initiate OTP verification"""
    product = get_object_or_404(Product, pk=product_id)
    
    # Role check handled by decorator
    
    if product.owner == request.user:
        messages.error(request, 'You cannot book your own product!')
        return redirect('product_detail', pk=product_id)
    
    if not product.is_available:
        messages.error(request, 'This product is not available!')
        return redirect('product_detail', pk=product_id)
        
    if product.stock_quantity < 1:
        messages.error(request, 'This product is out of stock!')
        return redirect('product_detail', pk=product_id)
    
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        notes = request.POST.get('notes', '')
        
        # Convert to date objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Validation
        if start_date >= end_date:
            messages.error(request, 'End date must be after start date!')
            return render(request, 'bookings/create_booking.html', {'product': product})
        
        # Create booking (pending verification)
        booking = Booking.objects.create(
            product=product,
            borrower=request.user,
            start_date=start_date,
            end_date=end_date,
            notes=notes,
            is_verified=False
        )
        
        # Validate Email
        if not request.user.email:
             messages.error(request, "Your account does not have an email address. Please update your profile.")
             return redirect('profile')

        # Generate OTP
        otp_code = ''.join(random.choices('0123456789', k=6))
        
        # Save OTP first
        OTP.objects.create(user=request.user, otp_code=otp_code)
        
        # Send OTP Email
        try:
            subject = 'Your OTP Verification Code – WardrobeShare'
            message = f"""
            Dear {request.user.username},
            
            Your OTP code for booking verification is: {otp_code}
            
            This code is valid for 5 minutes.
            Do not share this code with anyone.
            """
            
            # Using request.user.email explicitly
            recipient_email = request.user.email
            
            send_mail(
                subject, 
                message, 
                settings.DEFAULT_FROM_EMAIL, 
                [recipient_email], 
                fail_silently=False
            )
            
            print(f"📧 OTP email sent to {recipient_email}")
            messages.success(request, 'Booking initiated! Please verify your email.')
            
        except Exception as e:
            # Log the actual error
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send OTP email to {request.user.email}: {str(e)}")
            
            # DEBUGGING: Check if password is set
            has_password = bool(settings.EMAIL_HOST_PASSWORD)
            print(f"❌ SMTP Error: {e}")
            print(f"🔐 Email Password Set: {'✅ YES' if has_password else '❌ NO (Check Environment Variables!)'}")
            
            messages.error(request, f"Failed to send OTP email. Error: {e}")
        
        return redirect('verify_booking_otp', pk=booking.id)
    
    context = {'product': product}
    return render(request, 'bookings/create_booking.html', context)


@login_required
def verify_booking_otp_view(request, pk):
    """Verify OTP and confirm booking"""
    booking = get_object_or_404(Booking, pk=pk)
    
    # Security check
    if booking.borrower != request.user:
        messages.error(request, "Unauthorized access.")
        return redirect('dashboard')
        
    if booking.is_verified:
        return redirect('make_payment', booking_id=booking.id)
        
    if request.method == 'POST':
        entered_otp = request.POST.get('otp_code')
        
        # Get latest OTP for user
        otp_record = OTP.objects.filter(user=request.user, is_verified=False).order_by('-created_at').first()
        
        if otp_record and otp_record.otp_code == entered_otp and otp_record.is_valid():
            # Success
            otp_record.is_verified = True
            otp_record.save()
            
            booking.is_verified = True
            booking.save()
            
            # Send Booking Confirmation Email (Moved here after verification)
            try:
                subject = 'Booking Confirmed – WardrobeShare'
                message = f"""
                Dear {request.user.username},
                
                You have successfully initiated a booking.
                
                Product: {booking.product.title}
                Dates: {booking.start_date} to {booking.end_date}
                Status: {booking.status}
                
                Please complete your payment to confirm the booking.
                """
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [request.user.email], fail_silently=False)
            except Exception as e:
                print(f"❌ Confirmation Email failed: {e}")
            
            messages.success(request, "Email verified successfully! Please proceed to payment.")
            return redirect('make_payment', booking_id=booking.id)
        else:
            messages.error(request, "Invalid or expired OTP. Please try again.")
            
    return render(request, 'bookings/verify_otp.html', {'booking': booking})


@login_required
def booking_detail_view(request, pk):
    """View booking details"""
    booking = get_object_or_404(Booking, pk=pk)
    
    # Check if user is authorized to view this booking
    if booking.borrower != request.user and booking.product.owner != request.user:
        messages.error(request, 'You are not authorized to view this booking!')
        return redirect('dashboard')
    
    context = {'booking': booking}
    return render(request, 'bookings/booking_detail.html', context)


@login_required
def return_product_view(request, pk):
    """Handle product return and penalty calculation"""
    booking = get_object_or_404(Booking, pk=pk)
    
    if request.method == 'POST':
        # For testing purposes, allow manual date override if provided, else use today
        manual_date = request.POST.get('return_date')
        if manual_date:
            return_date = datetime.strptime(manual_date, '%Y-%m-%d').date()
        else:
            return_date = timezone.now().date()
            
        booking.actual_return_date = return_date
        
        # Calculate Penalty
        booking.late_days = 0
        booking.penalty_amount = 0
        
        if return_date > booking.end_date:
            delta = return_date - booking.end_date
            overdue_days = delta.days
            
            # Penalty Logic
            # Default: Charge for every late day
            # Special Rule: If category is 'Jacket', allowed return = 2 days (grace period)
            
            is_jacket = booking.product.category.name.lower() == 'jacket'
            grace_period = 2 if is_jacket else 0
            
            chargeable_days = max(0, overdue_days - grace_period)
            
            if chargeable_days > 0:
                booking.late_days = overdue_days # total overdue days
                # But penalty is calculated on chargeable days? 
                # "If returned after 2 days: Charge ₹101 per extra day"
                # This could mean: allowed return date = end_date + 2 days.
                # If returned on end_date + 1, no penalty.
                # If returned on end_date + 3, penalty for 1 day? Or 3 days?
                # "Charge ₹101 per extra day" usually means per chargeable day.
                
                booking.penalty_amount = chargeable_days * 101
                messages.warning(request, f"Late Return! Penalty: ₹{booking.penalty_amount} ({chargeable_days} chargeable days)")
            else:
                messages.info(request, "Returned late but within grace period. No penalty.")
        
        # Restore Stock
        product = booking.product
        product.stock_quantity += 1
        product.save()

        booking.status = 'completed'
        booking.save()
        messages.success(request, 'Product returned successfully.')
        return redirect('booking_detail', pk=pk)
    
    return redirect('booking_detail', pk=pk)


@login_required
def cancel_booking_view(request, pk):
    """Cancel booking and restore stock"""
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.borrower != request.user and booking.product.owner != request.user:
        messages.error(request, "Unauthorized action.")
        return redirect('dashboard')
        
    if booking.status in ['cancelled', 'completed']:
        messages.warning(request, "Booking is already cancelled or completed.")
        return redirect('booking_detail', pk=pk)
        
    # Restore stock if it was confirmed (and thus stock reduced)
    if booking.status == 'confirmed':
        product = booking.product
        product.stock_quantity += 1
        product.save()
        
    booking.status = 'cancelled'
    booking.save()
    
    messages.success(request, "Booking cancelled successfully.")
    return redirect('booking_detail', pk=pk)
