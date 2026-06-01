from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from homepage.models import Product
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from .forms import CheckoutForm
from shipping.models import ShippingInfo
import random

def get_session_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

@login_required(login_url='login')
def checkout_view(request, product_id=None):
    session_id = get_session_id(request)
    product = None
    cart_items = []
    total_amount = 0.0

    # Single product checkout (Buy Now)
    if product_id:
        product = get_object_or_404(Product, id=product_id)
        total_amount = float(product.price)
        
        # Track product view in analytics
        from analytics.models import ProductView
        ProductView.track_view(product)
    # Cart checkout
    else:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            cart = Cart.objects.filter(session_id=session_id).first()
            
        if not cart or not cart.items.exists():
            messages.error(request, "Your cart is empty. Cannot checkout.")
            return redirect('cart_view')
            
        cart_items = cart.items.all()
        total_amount = float(sum(item.product.price * item.quantity for item in cart_items))

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create Order without saving to DB yet to populate computed fields
            order = form.save(commit=False)
            order.user = request.user if request.user.is_authenticated else None
            order.session_id = session_id
            order.total_amount = total_amount
            order.status = 'pending'
            order.save()

            # Create Order Items
            if product:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=1
                )
            else:
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        price=item.product.price,
                        quantity=item.quantity
                    )
                # Clear cart
                cart.items.all().delete()

            # Create simulated shipping information
            tracking_num = f"SN-{random.randint(100000, 999999)}"
            ShippingInfo.objects.create(
                order=order,
                tracking_number=tracking_num,
                status='In Transit'
            )

            # Create Notification
            from notifications.models import Notification
            Notification.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_id=session_id,
                title="Order Placed",
                message=f"Order #{order.id} for ₹{order.total_amount:.2f} has been created. Please complete the payment."
            )

            messages.success(request, f"Order #{order.id} placed! Please complete the payment.")
            return redirect('payment_page', order_id=order.id)
        else:
            messages.error(request, "Invalid checkout information. Please verify the shipping details.")


    context = {
        'product': product,
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'checkout_test.html', context)

@login_required(login_url='login')
def order_list(request):
    session_id = get_session_id(request)
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    else:
        orders = Order.objects.filter(session_id=session_id).order_by('-created_at')
        
    context = {
        'orders': orders,
    }
    return render(request, 'orders_test.html', context)
