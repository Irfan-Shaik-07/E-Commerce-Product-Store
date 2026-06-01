from django.shortcuts import render, redirect
from orders.models import Order
from homepage.models import Product
from support.models import SupportTicket
from reviews.models import Review

def dashboard_home(request):
    # Fetch lists to display
    orders = Order.objects.all().order_by('-created_at')[:10]
    products = Product.objects.all()
    tickets = SupportTicket.objects.all().order_by('-created_at')[:10]
    reviews = Review.objects.all().order_by('-created_at')[:10]
    
    # Calculate stats
    total_sales = sum(o.total_amount for o in Order.objects.filter(status='paid'))
    orders_count = Order.objects.count()
    products_count = Product.objects.count()
    tickets_count = SupportTicket.objects.filter(status='Open').count()

    context = {
        'orders': orders,
        'products': products,
        'tickets': tickets,
        'reviews': reviews,
        'total_sales': total_sales,
        'orders_count': orders_count,
        'products_count': products_count,
        'tickets_count': tickets_count,
    }
    return render(request, 'admin_dashboard_test.html', context)
