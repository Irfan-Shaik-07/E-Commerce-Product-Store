from django.shortcuts import render
from homepage.models import Product
from .models import Coupon

def offers_page(request):
    coupons = Coupon.objects.filter(active=True)
    # Grab a few products and simulate a special discount for them
    deal_products = Product.objects.order_by('-rating')[:6]
    
    context = {
        'coupons': coupons,
        'deal_products': deal_products,
    }
    return render(request, 'offers_test.html', context)
