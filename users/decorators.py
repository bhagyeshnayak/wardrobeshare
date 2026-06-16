from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages

def owner_required(view_func):
    """
    Decorator to ensure the user is an Owner.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.can_lend():
            messages.error(request, 'Access denied. Users with "Owner" privileges only.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def customer_required(view_func):
    """
    Decorator to ensure the user is a Customer.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.can_borrow():
            messages.error(request, 'Access denied. Users with "Customer" privileges only.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
