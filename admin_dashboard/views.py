from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import Order
from homepage.models import Product
from support.models import SupportTicket
from reviews.models import Review
from .models import AdminActivityLog
from .forms import ProductForm

@staff_member_required(login_url='login')
def dashboard_home(request):
    # Fetch lists to display
    orders = Order.objects.all().order_by('-created_at')[:10]
    products = Product.objects.all()
    tickets = SupportTicket.objects.all().order_by('-created_at')[:10]
    reviews = Review.objects.all().order_by('-created_at')[:10]
    logs_count = AdminActivityLog.objects.count()
    
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
        'logs_count': logs_count,
    }
    return render(request, 'admin_dashboard_test.html', context)

@staff_member_required(login_url='login')
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    context = {'products': products}
    return render(request, 'admin_product_list.html', context)

@staff_member_required(login_url='login')
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            AdminActivityLog.objects.create(
                action_type='CREATE',
                action_details=f"Created product: {product.name} (Price: ₹{product.price}, Category: {product.get_category_display()})",
                user=request.user
            )
            messages.success(request, f"Product '{product.name}' was successfully created!")
            return redirect('admin_product_list')
        else:
            messages.error(request, "Error creating product. Please check form inputs.")
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Add New Product',
        'btn_text': 'Create Product'
    }
    return render(request, 'admin_product_form.html', context)

@staff_member_required(login_url='login')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            AdminActivityLog.objects.create(
                action_type='UPDATE',
                action_details=f"Updated product ID {product.id}: {product.name} (Price: ₹{product.price}, Category: {product.get_category_display()})",
                user=request.user
            )
            messages.success(request, f"Product '{product.name}' was successfully updated!")
            return redirect('admin_product_list')
        else:
            messages.error(request, "Error updating product. Please check form inputs.")
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'title': f'Edit Product: {product.name}',
        'btn_text': 'Save Changes',
        'product': product
    }
    return render(request, 'admin_product_form.html', context)

@staff_member_required(login_url='login')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        AdminActivityLog.objects.create(
            action_type='DELETE',
            action_details=f"Deleted product ID {pk}: {name}",
            user=request.user
        )
        product.delete()
        messages.success(request, f"Product '{name}' was successfully deleted!")
        return redirect('admin_product_list')
    
    context = {'product': product}
    return render(request, 'admin_product_confirm_delete.html', context)

@staff_member_required(login_url='login')
def activity_logs(request):
    logs = AdminActivityLog.objects.all().order_by('-timestamp')
    context = {'logs': logs}
    return render(request, 'admin_activity_logs.html', context)
