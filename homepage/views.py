from django.shortcuts import render
from django.db.models import Q
from .models import Product

def home(request):
    search_query = request.GET.get('search', '')
    
    # Base products query
    products = Product.objects.all()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    # Separate into categories
    mobiles = products.filter(category='mobiles')
    fashion = products.filter(category='fashion')
    electronics = products.filter(category='electronics')

    # Unique Feature: Smart Budget Planner
    budget_result = None
    budget_error = None
    target_budget = request.GET.get('budget', '')
    selected_cats = request.GET.getlist('budget_categories')

    if target_budget:
        try:
            budget_limit = float(target_budget)
            if budget_limit <= 0:
                budget_error = "Please enter a budget greater than 0."
            elif not selected_cats:
                budget_error = "Please select at least one category."
            else:
                # Greedy Knapsack to build bundle
                # Fetch products in chosen categories, ordered by rating (descending) and price (ascending)
                candidate_products = Product.objects.filter(category__in=selected_cats).order_by('-rating', 'price')
                
                bundle = []
                total_cost = 0.0
                
                for prod in candidate_products:
                    prod_price = float(prod.price)
                    if total_cost + prod_price <= budget_limit:
                        bundle.append(prod)
                        total_cost += prod_price
                
                if bundle:
                    savings = budget_limit - total_cost
                    budget_result = {
                        'bundle': bundle,
                        'total_cost': total_cost,
                        'savings': savings,
                        'budget_limit': budget_limit
                    }
                else:
                    budget_error = "No product combination fits your specified budget."
        except ValueError:
            budget_error = "Please enter a valid numeric budget."

    context = {
        'mobiles': mobiles,
        'fashion': fashion,
        'electronics': electronics,
        'search_query': search_query,
        'budget_result': budget_result,
        'budget_error': budget_error,
        'target_budget': target_budget,
        'selected_cats': selected_cats,
    }
    return render(request, 'home_page_test.html', context)
