from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from homepage.models import Product
from .models import Wishlist

def get_session_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def wishlist_view(request):
    session_id = get_session_id(request)
    if request.user.is_authenticated:
        # Merge guest wishlist items if any
        guest_items = Wishlist.objects.filter(session_id=session_id)
        for item in guest_items:
            if not Wishlist.objects.filter(user=request.user, product=item.product).exists():
                item.user = request.user
                item.save()
            else:
                item.delete()
        items = Wishlist.objects.filter(user=request.user).select_related('product')
    else:
        items = Wishlist.objects.filter(session_id=session_id).select_related('product')
        
    context = {
        'items': items,
    }
    return render(request, 'wishlist_test.html', context)

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_id = get_session_id(request)
    
    # Track product view in analytics
    from analytics.models import ProductView
    ProductView.track_view(product)
    
    if request.user.is_authenticated:
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    else:
        wishlist_item, created = Wishlist.objects.get_or_create(session_id=session_id, product=product)
        
    if created:
        messages.success(request, f"Added {product.name} to wishlist.")
    else:
        messages.info(request, f"{product.name} is already in your wishlist.")
        
    return redirect(request.META.get('HTTP_REFERER', 'wishlist_view'))

def remove_from_wishlist(request, item_id):
    item = get_object_or_404(Wishlist, id=item_id)
    product_name = item.product.name
    item.delete()
    messages.success(request, f"Removed {product_name} from wishlist.")
    return redirect('wishlist_view')
