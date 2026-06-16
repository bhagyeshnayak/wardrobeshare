from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Count
from django.contrib import messages
from .models import Product, Category
from reviews.models import Review

def home_view(request):
    """
    Renders the homepage with featured products and categories.
    """
    # Fetch categories
    categories = Category.objects.filter(~Q(name='Shoes')).order_by('name')
    
    # Fetch featured products (limit 6)
    featured_products = Product.objects.select_related('owner', 'category').filter(is_available=True).order_by('-created_at')[:6]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'home.html', context)

def product_list_view(request):
    """
    Renders the product listing page with filters.
    """
    products = Product.objects.select_related('category', 'owner').filter(is_available=True)
    categories = Category.objects.filter(~Q(name='Shoes')).order_by('name')
    
    # Filter Parameters
    category_id = request.GET.get('category')
    search_query = request.GET.get('search', '')
    size = request.GET.get('size')
    sort_by = request.GET.get('sort')
    
    # Apply Filters
    if category_id:
        products = products.filter(category_id=category_id)
        
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
        
    if size:
        products = products.filter(size=size)
        
    # Apply Sorting
    if sort_by == 'price_low':
        products = products.order_by('price_per_day')
    elif sort_by == 'price_high':
        products = products.order_by('-price_per_day')
    else:
        products = products.order_by('-created_at')
        
    context = {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id and category_id.isdigit() else None,
        'search_query': search_query,
        'selected_size': size,
        'sort_by': sort_by,
    }
    return render(request, 'products/product_list.html', context)

from bookings.models import Booking

def product_detail_view(request, pk):
    """
    Renders the product detail page.
    """
    product = get_object_or_404(Product.objects.select_related('owner', 'category'), pk=pk)
    
    # Get reviews
    reviews = Review.objects.filter(product=product).select_related('user').order_by('-created_at')
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Check if user can review
    can_review = False
    
    if request.user.is_authenticated:
        # CORRECT WAY – query Booking model directly
        has_booking = Booking.objects.filter(
            product=product,
            borrower=request.user,
            status='Completed'
        ).exists()
        
        can_review = has_booking
    
    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': round(average_rating, 1),
        'range_5': range(1, 6),
        'can_review': can_review
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def add_product_view(request):
    """
    View to add a new product.
    """
    # Ensure only owners can add
    if hasattr(request.user, 'role') and request.user.role == 'customer':
        messages.error(request, "Only owners can list items.")
        return redirect('home')

    if request.method == 'POST':
        try:
            Product.objects.create(
                owner=request.user,
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                category_id=request.POST.get('category'),
                price_per_day=request.POST.get('price_per_day'),
                size=request.POST.get('size'),
                condition=request.POST.get('condition'),
                image=request.FILES.get('image'),
                stock_quantity=request.POST.get('stock_quantity', 1)
            )
            messages.success(request, "Product listed successfully!")
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f"Error creating product: {e}")
            
    categories = Category.objects.all()
    return render(request, 'products/add_product.html', {'categories': categories})

@login_required
def edit_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if product.owner != request.user:
        messages.error(request, "You are not authorized to edit this product.")
        return redirect('product_detail', pk=pk)
        
    if request.method == 'POST':
        product.title = request.POST.get('title')
        product.description = request.POST.get('description')
        product.price_per_day = request.POST.get('price_per_day')
        product.size = request.POST.get('size')
        product.condition = request.POST.get('condition')
        product.stock_quantity = request.POST.get('stock_quantity')
        
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
            
        product.save()
        messages.success(request, "Product updated successfully!")
        return redirect('product_detail', pk=pk)

    categories = Category.objects.all()
    return render(request, 'products/edit_product.html', {'product': product, 'categories': categories})

@login_required
def add_review_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        Review.objects.create(
            user=request.user,
            product=product,
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment')
        )
        return redirect('product_detail', pk=pk)
    return render(request, 'products/add_review.html', {'product': product})
