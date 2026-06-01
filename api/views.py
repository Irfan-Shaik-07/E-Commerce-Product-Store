import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from homepage.models import Product

def seed_if_empty():
    """Seed sample products if the database is empty so that the playground is immediately useful."""
    if Product.objects.count() == 0:
        Product.objects.create(
            name="iPhone 15 Pro Max",
            price=1199.99,
            description="Titanium design, powerful A17 Pro chip, and the most advanced iPhone camera system.",
            category="mobiles",
            rating=4.9,
            image_url="https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&q=80&w=600"
        )
        Product.objects.create(
            name="Premium Denim Jacket",
            price=89.50,
            description="Classic fit denim jacket built with durable organic cotton for everyday rugged wear.",
            category="fashion",
            rating=4.5,
            image_url="https://images.unsplash.com/photo-1576995853123-5a10305d93c0?auto=format&fit=crop&q=80&w=600"
        )
        Product.objects.create(
            name="Sony Noise-Canceling Headphones",
            price=348.00,
            description="Industry-leading wireless active noise-canceling headphones with premium sound quality.",
            category="electronics",
            rating=4.7,
            image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&q=80&w=600"
        )
        Product.objects.create(
            name="Vintage Leather Boots",
            price=180.00,
            description="Full-grain leather boots designed for extreme comfort, durability, and timeless style.",
            category="fashion",
            rating=4.6,
            image_url="https://images.unsplash.com/photo-1520639888713-7851133b1ed0?auto=format&fit=crop&q=80&w=600"
        )

# Exempt the API class from CSRF checks so that clients (and the playground) can easily make POST/PUT/PATCH/DELETE calls.
@method_decorator(csrf_exempt, name='dispatch')
class ProductAPIView(View):
    
    def dispatch(self, request, *args, **kwargs):
        # Auto-seed if the database has zero products
        seed_if_empty()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk=None, *args, **kwargs):
        """
        GET /api/products/ - List all products (supports optional 'search' and 'category' filters)
        GET /api/products/<pk>/ - Retrieve a single product
        """
        if pk is not None:
            try:
                product = Product.objects.get(pk=pk)
                return JsonResponse({
                    'id': product.id,
                    'name': product.name,
                    'price': float(product.price),
                    'description': product.description,
                    'category': product.category,
                    'rating': float(product.rating),
                    'image_url': product.image_url,
                    'created_at': product.created_at.isoformat()
                })
            except Product.DoesNotExist:
                return JsonResponse({'error': f'Product with id {pk} not found.'}, status=404)

        # Listing products
        products = Product.objects.all().order_by('-id')
        
        # Apply optional filters
        category = request.GET.get('category', '')
        if category:
            products = products.filter(category=category)
            
        search = request.GET.get('search', '')
        if search:
            products = products.filter(name__icontains=search) | products.filter(description__icontains=search)
            
        data = []
        for p in products:
            data.append({
                'id': p.id,
                'name': p.name,
                'price': float(p.price),
                'description': p.description,
                'category': p.category,
                'rating': float(p.rating),
                'image_url': p.image_url,
                'created_at': p.created_at.isoformat()
            })
            
        return JsonResponse(data, safe=False)

    def post(self, request, *args, **kwargs):
        """
        POST /api/products/ - Create a new product
        """
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body.'}, status=400)

        # Basic field validation
        name = body.get('name')
        price = body.get('price')
        description = body.get('description', '')
        category = body.get('category')
        rating = body.get('rating', 4.0)
        image_url = body.get('image_url', '')

        if not name or price is None or not category:
            return JsonResponse({'error': "Missing required fields: 'name', 'price', and 'category' are mandatory."}, status=400)

        # Category choices validation
        valid_categories = dict(Product.CATEGORY_CHOICES).keys()
        if category not in valid_categories:
            return JsonResponse({'error': f"Invalid category '{category}'. Must be one of: {', '.join(valid_categories)}."}, status=400)

        # Price validation
        try:
            price_val = float(price)
            if price_val <= 0:
                return JsonResponse({'error': "Price must be a positive number greater than 0."}, status=400)
        except ValueError:
            return JsonResponse({'error': "Price must be a valid number."}, status=400)

        # Rating validation
        try:
            rating_val = float(rating)
            if not (0 <= rating_val <= 5):
                return JsonResponse({'error': "Rating must be between 0.0 and 5.0."}, status=400)
        except ValueError:
            return JsonResponse({'error': "Rating must be a valid number."}, status=400)

        # Save to database
        product = Product.objects.create(
            name=name,
            price=price_val,
            description=description,
            category=category,
            rating=rating_val,
            image_url=image_url
        )

        return JsonResponse({
            'message': 'Product created successfully!',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'description': product.description,
                'category': product.category,
                'rating': float(product.rating),
                'image_url': product.image_url,
                'created_at': product.created_at.isoformat()
            }
        }, status=201)

    def put(self, request, pk=None, *args, **kwargs):
        """
        PUT /api/products/<pk>/ - Complete update (replaces all fields)
        """
        if pk is None:
            return JsonResponse({'error': 'Method PUT requires a product ID.'}, status=405)

        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return JsonResponse({'error': f'Product with id {pk} not found.'}, status=404)

        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body.'}, status=400)

        # For PUT, all main fields are required to completely replace the resource
        name = body.get('name')
        price = body.get('price')
        description = body.get('description')
        category = body.get('category')
        rating = body.get('rating')
        image_url = body.get('image_url')

        if not name or price is None or description is None or not category or rating is None or image_url is None:
            return JsonResponse({
                'error': "Complete resource replacement (PUT) requires all fields: 'name', 'price', 'description', 'category', 'rating', and 'image_url'."
            }, status=400)

        # Category choices validation
        valid_categories = dict(Product.CATEGORY_CHOICES).keys()
        if category not in valid_categories:
            return JsonResponse({'error': f"Invalid category '{category}'. Must be one of: {', '.join(valid_categories)}."}, status=400)

        # Price validation
        try:
            price_val = float(price)
            if price_val <= 0:
                return JsonResponse({'error': "Price must be a positive number."}, status=400)
        except ValueError:
            return JsonResponse({'error': "Price must be a valid number."}, status=400)

        # Rating validation
        try:
            rating_val = float(rating)
            if not (0 <= rating_val <= 5):
                return JsonResponse({'error': "Rating must be between 0.0 and 5.0."}, status=400)
        except ValueError:
            return JsonResponse({'error': "Rating must be a valid number."}, status=400)

        # Update product
        product.name = name
        product.price = price_val
        product.description = description
        product.category = category
        product.rating = rating_val
        product.image_url = image_url
        product.save()

        return JsonResponse({
            'message': 'Product updated completely (PUT) successfully!',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'description': product.description,
                'category': product.category,
                'rating': float(product.rating),
                'image_url': product.image_url,
                'created_at': product.created_at.isoformat()
            }
        })

    def patch(self, request, pk=None, *args, **kwargs):
        """
        PATCH /api/products/<pk>/ - Partial update (updates only the fields provided)
        """
        if pk is None:
            return JsonResponse({'error': 'Method PATCH requires a product ID.'}, status=405)

        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return JsonResponse({'error': f'Product with id {pk} not found.'}, status=404)

        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body.'}, status=400)

        # Track updates
        if 'name' in body:
            if not body['name']:
                return JsonResponse({'error': "Name cannot be empty."}, status=400)
            product.name = body['name']

        if 'category' in body:
            valid_categories = dict(Product.CATEGORY_CHOICES).keys()
            if body['category'] not in valid_categories:
                return JsonResponse({'error': f"Invalid category. Must be one of: {', '.join(valid_categories)}."}, status=400)
            product.category = body['category']

        if 'price' in body:
            try:
                price_val = float(body['price'])
                if price_val <= 0:
                    return JsonResponse({'error': "Price must be a positive number."}, status=400)
                product.price = price_val
            except ValueError:
                return JsonResponse({'error': "Price must be a valid number."}, status=400)

        if 'rating' in body:
            try:
                rating_val = float(body['rating'])
                if not (0 <= rating_val <= 5):
                    return JsonResponse({'error': "Rating must be between 0.0 and 5.0."}, status=400)
                product.rating = rating_val
            except ValueError:
                return JsonResponse({'error': "Rating must be a valid number."}, status=400)

        if 'description' in body:
            product.description = body['description']

        if 'image_url' in body:
            product.image_url = body['image_url']

        product.save()

        return JsonResponse({
            'message': 'Product updated partially (PATCH) successfully!',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'description': product.description,
                'category': product.category,
                'rating': float(product.rating),
                'image_url': product.image_url,
                'created_at': product.created_at.isoformat()
            }
        })

    def delete(self, request, pk=None, *args, **kwargs):
        """
        DELETE /api/products/<pk>/ - Delete a product
        """
        if pk is None:
            return JsonResponse({'error': 'Method DELETE requires a product ID.'}, status=405)

        try:
            product = Product.objects.get(pk=pk)
            product_id = product.id
            product.delete()
            return JsonResponse({
                'message': f'Product with id {product_id} deleted successfully!',
                'deleted_id': product_id
            }, status=200) # 200 OK with message is nice, or we could do 204 No Content. 200 with JSON payload is awesome for playgrounds!
        except Product.DoesNotExist:
            return JsonResponse({'error': f'Product with id {pk} not found.'}, status=404)

    def head(self, request, pk=None, *args, **kwargs):
        """
        HEAD /api/products/<pk>/ - Retrieve response metadata headers only (empty body)
        """
        if pk is not None:
            try:
                product = Product.objects.get(pk=pk)
                response = HttpResponse()
                response['Content-Type'] = 'application/json'
                response['X-Product-Exists'] = 'True'
                response['X-Product-Price'] = str(product.price)
                response['X-Product-Category'] = product.category
                return response
            except Product.DoesNotExist:
                return HttpResponse(status=404)
        
        # HEAD on collection
        count = Product.objects.count()
        response = HttpResponse()
        response['Content-Type'] = 'application/json'
        response['X-Total-Count'] = str(count)
        return response

    def options(self, request, *args, **kwargs):
        """
        OPTIONS /api/products/ - Return details of allowed methods and schema definitions
        """
        response = JsonResponse({
            "name": "ShopNova REST Product API Schema",
            "description": "A fully compliant REST API to manage products using all HTTP methods.",
            "allowed_methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
            "endpoints": {
                "/api/products/": {
                    "GET": {
                        "description": "List all products in reverse chronological order.",
                        "parameters": {
                            "category": "Filter products by category (mobiles, fashion, electronics)",
                            "search": "Sub-string search on product name and description"
                        }
                    },
                    "POST": {
                        "description": "Create a new product record in the system.",
                        "required_fields": {
                            "name": "string (max 200)",
                            "price": "decimal/float (positive value)",
                            "category": "string (mobiles, fashion, electronics)"
                        },
                        "optional_fields": {
                            "description": "string",
                            "rating": "decimal/float (default 4.0, range 0.0 to 5.0)",
                            "image_url": "valid URL string"
                        }
                    }
                },
                "/api/products/<id>/": {
                    "GET": {
                        "description": "Retrieve full details of a specific product by its ID."
                    },
                    "PUT": {
                        "description": "Complete replacement of a product's fields. All fields must be supplied.",
                        "fields_required": ["name", "price", "description", "category", "rating", "image_url"]
                    },
                    "PATCH": {
                        "description": "Partial update of a product. Only supply the fields that you want to update."
                    },
                    "DELETE": {
                        "description": "Remove a product permanently from the database."
                    },
                    "HEAD": {
                        "description": "Get response headers and check product existence without transferring the response body."
                    }
                }
            },
            "fields": {
                "id": "integer (auto-incrementing primary key)",
                "name": "string (max 200 characters)",
                "price": "decimal (max 10 digits, 2 decimal places)",
                "description": "text field",
                "category": "string (choices: 'mobiles', 'fashion', 'electronics')",
                "rating": "decimal (range 0.0 to 5.0)",
                "image_url": "URL (max 500 characters, optional)"
            }
        })
        
        response['Allow'] = 'GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS'
        return response


class PlaygroundView(View):
    """
    Renders the API Interactive Playground web interface.
    """
    def get(self, request, *args, **kwargs):
        # Fetch categories to show in UI filters
        categories = [cat[0] for cat in Product.CATEGORY_CHOICES]
        return render(request, 'api/playground.html', {
            'categories': categories,
            'existing_products': Product.objects.all().order_by('-id')[:10]
        })
