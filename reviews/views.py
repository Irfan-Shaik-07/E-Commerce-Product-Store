from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from homepage.models import Product
from .models import Review
from .forms import ReviewForm

def reviews_page(request, product_id=None):
    selected_product = None
    if product_id:
        selected_product = get_object_or_404(Product, id=product_id)
        reviews = Review.objects.filter(product=selected_product).order_by('-created_at')
    else:
        reviews = Review.objects.all().order_by('-created_at')[:20]

    if request.method == 'POST':
        # Map 'product_id' to 'product' for ModelForm validation
        data = request.POST.copy()
        if 'product_id' in data and 'product' not in data:
            data['product'] = data['product_id']

        form = ReviewForm(data)
        if form.is_valid():
            review = form.save()
            prod = review.product

            # Track product view in analytics
            from analytics.models import ProductView
            ProductView.track_view(prod)

            # Update Product overall rating slightly
            prod_reviews = Review.objects.filter(product=prod)
            avg_rating = sum(r.rating for r in prod_reviews) / prod_reviews.count()
            prod.rating = round(avg_rating, 1)
            prod.save()

            messages.success(request, f"Review submitted for {prod.name}!")
            return redirect('reviews_page')
        else:
            messages.error(request, "Invalid review form submission. Please check your inputs.")

    products = Product.objects.all()
    context = {
        'products': products,
        'selected_product': selected_product,
        'reviews': reviews,
    }
    return render(request, 'reviews_test.html', context)

