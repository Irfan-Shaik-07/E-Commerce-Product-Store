from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from orders.models import Order
from .models import Payment
from .forms import PaymentForm
import uuid

def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status != 'pending':
        messages.info(request, "This order has already been processed.")
        return redirect('order_list')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.transaction_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
            payment.status = 'Success'
            payment.save()

            # Update Order Status
            order.status = 'paid'
            order.save()

            # Create Notification
            from notifications.models import Notification
            Notification.objects.create(
                user=order.user,
                session_id=order.session_id,
                title="Payment Successful",
                message=f"Payment of ₹{order.total_amount:.2f} for Order #{order.id} was successful! Transaction ID: {payment.transaction_id}."
            )

            messages.success(request, f"Payment successful! Transaction ID: {payment.transaction_id}")
            return redirect('order_list')
        else:
            messages.error(request, "Invalid payment selection.")

    context = {
        'order': order,
    }
    return render(request, 'payments_test.html', context)

