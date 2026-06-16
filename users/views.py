from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import User
from products.models import Product
from bookings.models import Booking
from payments.models import Payment


# =============================
# REGISTER
# =============================
def register_view(request):
    return render(request, 'users/register.html')


# =============================
# LOGIN
# =============================
def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect('home')

        messages.error(request, "Invalid Credentials")

    return render(request, 'users/login.html')


# =============================
# LOGOUT
# =============================
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


# =============================
# DASHBOARD
# =============================
@login_required
def dashboard_view(request):

    user = request.user

    # ===== OWNER DASHBOARD =====
    if user.role == 'owner':

        products = user.products.all().order_by('-created_at')

        incoming_bookings = Booking.objects.filter(
            product__owner=user
        ).select_related('borrower', 'product').order_by('-start_date')

        context = {
            'user': user,
            'products': products,
            'incoming_bookings': incoming_bookings,
        }

        return render(request, 'users/owner_dashboard.html', context)

    # ===== CUSTOMER DASHBOARD =====
    else:

        metrics = {
            'total_spent': 0,
            'active_rentals': 0
        }

        my_bookings = Booking.objects.filter(
            borrower=user
        ).select_related('product', 'product__owner').order_by('-created_at')

        for b in my_bookings:
            status = (b.status or '').lower()

            if status in ['pending', 'confirmed', 'active']:
                metrics['active_rentals'] += 1

            if status in ['completed', 'confirmed']:
                metrics['total_spent'] += float(b.total_price or 0)

        context = {
            'user': user,
            'my_bookings': my_bookings,
            'metrics': metrics
        }

        return render(request, 'users/customer_dashboard.html', context)


# =============================
# PROFILE VIEW
# =============================
def profile_view(request, username):

    profile_user = get_object_or_404(User, username=username)

    listed_products = Product.objects.filter(
        owner=profile_user
    ).order_by('-created_at')

    owner_bookings = Booking.objects.filter(
        product__owner=profile_user
    )

    payments = Payment.objects.filter(
        user=profile_user
    )

    context = {
        'profile_user': profile_user,
        'listed_products': listed_products,
        'owner_bookings': owner_bookings,
        'payments': payments,
    }

    return render(request, 'users/profile.html', context)
