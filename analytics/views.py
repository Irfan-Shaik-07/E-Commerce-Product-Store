from django.shortcuts import render
from .models import ProductView
from homepage.models import Product
from orders.models import Order, OrderItem
from reviews.models import Review
from django.db.models import Sum, Avg

def analytics_report(request):
    # 1. Product views ranking
    top_viewed = ProductView.objects.select_related('product').order_by('-view_count')[:10]
    
    # 2. General metrics
    total_sales = Order.objects.filter(status__in=['paid', 'shipped', 'delivered']).aggregate(Sum('total_amount'))['total_amount__sum'] or 0.0
    total_orders = Order.objects.count()
    total_views = ProductView.objects.aggregate(Sum('view_count'))['view_count__sum'] or 0
    total_reviews = Review.objects.count()
    
    # 3. Category performance analysis
    categories = ['mobiles', 'fashion', 'electronics']
    category_data = []
    
    for cat in categories:
        # views count
        cat_views = ProductView.objects.filter(product__category=cat).aggregate(Sum('view_count'))['view_count__sum'] or 0
        
        # sales count
        items = OrderItem.objects.filter(
            product__category=cat,
            order__status__in=['paid', 'shipped', 'delivered']
        ).select_related('product')
        cat_sales = sum(float(item.price) * item.quantity for item in items)
        
        # average rating
        cat_rating = Product.objects.filter(category=cat).aggregate(Avg('rating'))['rating__avg'] or 4.0
        
        category_data.append({
            'name': cat.capitalize(),
            'views': cat_views,
            'sales': float(cat_sales),
            'rating': round(float(cat_rating), 1)
        })
        
    # Scaling helpers for pure CSS charts
    max_views = max(c['views'] for c in category_data) or 1
    max_sales = max(c['sales'] for c in category_data) or 1.0
    max_prod_views = max(pv.view_count for pv in top_viewed) if top_viewed else 1

    for c in category_data:
        c['views_pct'] = (c['views'] / max_views) * 100
        c['sales_pct'] = (c['sales'] / max_sales) * 100
        c['rating_pct'] = (c['rating'] / 5.0) * 100

    top_viewed_list = []
    for rank, pv in enumerate(top_viewed, 1):
        top_viewed_list.append({
            'rank': rank,
            'product': pv.product,
            'view_count': pv.view_count,
            'pct': (pv.view_count / max_prod_views) * 100
        })
        
    context = {
        'top_viewed': top_viewed_list,
        'total_sales': float(total_sales),
        'total_orders': total_orders,
        'total_views': total_views,
        'total_reviews': total_reviews,
        'category_data': category_data,
    }
    return render(request, 'analytics_test.html', context)
