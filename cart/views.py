from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from homepage.models import Product
from .models import Cart, CartItem

def get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        # If guest cart exists, merge it
        guest_cart = Cart.objects.filter(session_id=session_id).first()
        if guest_cart:
            for item in guest_cart.items.all():
                existing_item = CartItem.objects.filter(cart=cart, product=item.product).first()
                if existing_item:
                    existing_item.quantity += item.quantity
                    existing_item.save()
                else:
                    item.cart = cart
                    item.save()
            guest_cart.delete()
    else:
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart

def cart_view(request):
    cart = get_or_create_cart(request)
    items = cart.items.all().select_related('product')
    total = sum(item.product.price * item.quantity for item in items)
    
    context = {
        'cart': cart,
        'items': items,
        'total': total,
    }
    return render(request, 'cart_test.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    
    # Track product view in analytics
    from analytics.models import ProductView
    ProductView.track_view(product)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Increased quantity of {product.name} in cart.")
    else:
        messages.success(request, f"Added {product.name} to cart.")
        
    return redirect(request.META.get('HTTP_REFERER', 'cart_view'))

def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f"Updated quantity of {cart_item.product.name}.")
        else:
            cart_item.delete()
            messages.success(request, f"Removed {cart_item.product.name} from cart.")
    return redirect('cart_view')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f"Removed {product_name} from cart.")
    return redirect('cart_view')

def add_bundle(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('product_ids')
        if not product_ids:
            messages.error(request, "No products in the bundle to add.")
            return redirect('home')
            
        cart = get_or_create_cart(request)
        added_count = 0
        
        for pid in product_ids:
            try:
                product = Product.objects.get(id=pid)
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                if not created:
                    cart_item.quantity += 1
                    cart_item.save()
                added_count += 1
            except Product.DoesNotExist:
                pass
                
        if added_count > 0:
            messages.success(request, f"Successfully added {added_count} products from bundle to your cart!")
        else:
            messages.error(request, "Could not add bundle items.")
            
    return redirect('cart_view')
