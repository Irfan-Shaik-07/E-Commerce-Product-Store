from cart.models import Cart
from wishlist.models import Wishlist

def cart_wishlist_counts(request):
    cart_count = 0
    wishlist_count = 0
    
    if not request.session.session_key:
        try:
            request.session.create()
        except Exception:
            pass
            
    session_id = request.session.session_key
    
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            cart = Cart.objects.filter(session_id=session_id).first()
            
        if cart:
            cart_count = sum(item.quantity for item in cart.items.all())
    except Exception:
        pass
        
    try:
        if request.user.is_authenticated:
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
        else:
            wishlist_count = Wishlist.objects.filter(session_id=session_id).count()
    except Exception:
        pass
        
    return {
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    }
