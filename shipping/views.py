from django.shortcuts import render, get_object_or_404
from orders.models import Order
from .models import ShippingInfo

def track_shipment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    shipping_info = get_object_or_404(ShippingInfo, order=order)
    
    # Calculate status stages for visualization
    status = order.status
    stages = {
        'ordered': True,
        'paid': status in ['paid', 'shipped', 'delivered'],
        'shipped': status in ['shipped', 'delivered'],
        'delivered': status == 'delivered'
    }

    context = {
        'order': order,
        'shipping': shipping_info,
        'stages': stages,
    }
    return render(request, 'shipping_test.html', context)
