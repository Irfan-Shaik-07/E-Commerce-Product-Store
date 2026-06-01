from django.core.management.base import BaseCommand
from homepage.models import Product
from offers.models import Coupon

class Command(BaseCommand):
    help = 'Seeds the database with initial products'

    def handle(self, *args, **kwargs):
        # Clear existing products
        Product.objects.all().delete()
        Coupon.objects.all().delete()

        products = [
            # --- MOBILES (10 products) ---
            {
                'name': 'iPhone 15 Pro Max',
                'price': 159999.00,
                'description': 'Titanium design, A17 Pro chip, 48MP main camera, and USB-C. The ultimate iPhone experience.',
                'category': 'mobiles',
                'rating': 4.9,
                'image_url': 'https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'price': 129999.00,
                'description': 'Galaxy AI is here. 200MP camera, built-in S Pen, and Snapdragon 8 Gen 3 processor.',
                'category': 'mobiles',
                'rating': 4.8,
                'image_url': 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Google Pixel 8 Pro',
                'price': 99999.00,
                'description': 'The all-pro phone engineered by Google. Advanced camera features and AI photo editing.',
                'category': 'mobiles',
                'rating': 4.7,
                'image_url': 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'OnePlus 12',
                'price': 69999.00,
                'description': 'Smooth Beyond Belief. 4th Gen Hasselblad Camera, 100W SUPERVOOC charging, and 2K display.',
                'category': 'mobiles',
                'rating': 4.6,
                'image_url': 'https://images.unsplash.com/photo-1565630916779-e303be97b6f5?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Xiaomi 14 Ultra',
                'price': 119999.00,
                'description': 'Leica Summilux optical lens, 1-inch sensor, and Snapdragon 8 Gen 3 for professional photography.',
                'category': 'mobiles',
                'rating': 4.7,
                'image_url': 'https://images.unsplash.com/photo-1580910051074-3eb694886505?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Nothing Phone (2)',
                'price': 39999.00,
                'description': 'A new way to interact. Glyphs interface, Nothing OS 2.0, and a sleek transparent design.',
                'category': 'mobiles',
                'rating': 4.5,
                'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Asus ROG Phone 8',
                'price': 94999.00,
                'description': 'The ultimate gaming phone. 165Hz AMOLED display, AirTrigger system, and active cooling accessories.',
                'category': 'mobiles',
                'rating': 4.8,
                'image_url': 'https://images.unsplash.com/photo-1546054454-aa26e2b734c7?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Motorola Edge 50 Ultra',
                'price': 54999.00,
                'description': 'Artistry meets performance. Pantone validated display, wooden finish back, and 125W turbo power.',
                'category': 'mobiles',
                'rating': 4.4,
                'image_url': 'https://images.unsplash.com/photo-1573148195900-7845dcb9b127?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Vivo X100 Pro',
                'price': 89999.00,
                'description': 'ZEISS APO Telephoto camera, Dimensity 9300 processor, and professional portrait presets.',
                'category': 'mobiles',
                'rating': 4.6,
                'image_url': 'https://images.unsplash.com/photo-1523206489230-c012c64b2b48?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Realme GT 6',
                'price': 40999.00,
                'description': 'Flagship killer performance. 6000 nits ultra-bright display and 120W charging support.',
                'category': 'mobiles',
                'rating': 4.3,
                'image_url': 'https://images.unsplash.com/photo-1551645121-d1034da75057?w=500&auto=format&fit=crop&q=60'
            },

            # --- FASHION (10 products) ---
            {
                'name': 'Classic Leather Jacket',
                'price': 4999.00,
                'description': '100% genuine vintage leather jacket. Durable, stylish, and perfect for all seasons.',
                'category': 'fashion',
                'rating': 4.6,
                'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Premium Slim-Fit Suit',
                'price': 12999.00,
                'description': 'Tailored slim-fit 3-piece suit in navy blue. Includes blazer, vest, and trousers.',
                'category': 'fashion',
                'rating': 4.8,
                'image_url': 'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Vintage Denim Jacket',
                'price': 2499.00,
                'description': 'Light wash classic denim jacket. Made with heavy-duty organic cotton.',
                'category': 'fashion',
                'rating': 4.4,
                'image_url': 'https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Minimalist Canvas Sneakers',
                'price': 1999.00,
                'description': 'Clean, breathable canvas sneakers. Ortholite insoles for all-day comfort.',
                'category': 'fashion',
                'rating': 4.2,
                'image_url': 'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Elegant Silk Evening Gown',
                'price': 7999.00,
                'description': 'Stunning emerald green silk gown. Drape neck design and elegant side slit.',
                'category': 'fashion',
                'rating': 4.9,
                'image_url': 'https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Activewear Running Shoes',
                'price': 3499.00,
                'description': 'Ergonomic athletic running shoes with shock absorption and breathable mesh panels.',
                'category': 'fashion',
                'rating': 4.5,
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Urban Streetwear Hoodie',
                'price': 1899.00,
                'description': 'Oversized fleece hoodie in charcoal black. Featuring high-density chest print details.',
                'category': 'fashion',
                'rating': 4.3,
                'image_url': 'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Smart Casual Blazer',
                'price': 4500.00,
                'description': 'Structured knit blazer in light grey. Versatile for both office wear and dinners.',
                'category': 'fashion',
                'rating': 4.5,
                'image_url': 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Designer Aviator Sunglasses',
                'price': 1200.00,
                'description': 'UV400 polarized aviator sunglasses with gold frames and dark green tint lenses.',
                'category': 'fashion',
                'rating': 4.1,
                'image_url': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Leather Chelsea Boots',
                'price': 5999.00,
                'description': 'Premium water-resistant leather Chelsea boots with elasticated side panels and pull tabs.',
                'category': 'fashion',
                'rating': 4.7,
                'image_url': 'https://images.unsplash.com/photo-1638247025967-b4e38f787b76?w=500&auto=format&fit=crop&q=60'
            },

            # --- ELECTRONICS (10 products) ---
            {
                'name': 'Sony WH-1000XM5 Headphones',
                'price': 29999.00,
                'description': 'Industry-leading noise cancelling wireless over-ear headphones with auto-NC optimizer.',
                'category': 'electronics',
                'rating': 4.8,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'MacBook Pro 14" M3',
                'price': 169999.00,
                'description': 'Next-generation M3 chip, 8GB unified memory, 512GB SSD, Liquid Retina XDR screen.',
                'category': 'electronics',
                'rating': 4.9,
                'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Dell XPS 13 Laptop',
                'price': 119999.00,
                'description': 'Ultra-thin Windows laptop. Intel Core Ultra 7 processor, InfinityEdge FHD+ display.',
                'category': 'electronics',
                'rating': 4.6,
                'image_url': 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'iPad Air 10.9"',
                'price': 59999.00,
                'description': 'Versatile tablet powered by M2 chip. Liquid Retina display, Center Stage camera, Apple Pencil support.',
                'category': 'electronics',
                'rating': 4.7,
                'image_url': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Nintendo Switch OLED',
                'price': 32999.00,
                'description': '7-inch vibrant OLED screen, adjustable stand, wired LAN port dock, and 64GB storage.',
                'category': 'electronics',
                'rating': 4.8,
                'image_url': 'https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Bose QuietComfort Ultra',
                'price': 35999.00,
                'description': 'Premium spatial audio wireless earbuds with breakthrough noise cancellation and CustomTune tech.',
                'category': 'electronics',
                'rating': 4.5,
                'image_url': 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Sony PlayStation 5',
                'price': 54999.00,
                'description': 'Slim Digital Edition console. Ultra-fast SSD, haptic feedback, 4K gaming, 120fps support.',
                'category': 'electronics',
                'rating': 4.9,
                'image_url': 'https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Kindle Paperwhite',
                'price': 14999.00,
                'description': '6.8-inch display, adjustable warm light, waterproof, and up to 10 weeks of battery life.',
                'category': 'electronics',
                'rating': 4.7,
                'image_url': 'https://images.unsplash.com/photo-1592496001020-d31bd830651f?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'Canon EOS R50 Camera',
                'price': 74999.00,
                'description': 'Mirrorless camera kit with RF-S 18-45mm lens. 24.2 Megapixel APS-C sensor, 4K vlogging.',
                'category': 'electronics',
                'rating': 4.6,
                'image_url': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=500&auto=format&fit=crop&q=60'
            },
            {
                'name': 'LG 27" 4K IPS Monitor',
                'price': 26999.00,
                'description': 'UltraFine display with HDR10 support, USB Type-C connectivity, and height-adjustable stand.',
                'category': 'electronics',
                'rating': 4.4,
                'image_url': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500&auto=format&fit=crop&q=60'
            },
        ]

        # Import Review model
        from reviews.models import Review
        Review.objects.all().delete()

        reviewers = [
            ("Rahul", "Amazing product quality, highly recommend!"),
            ("Sneha", "Worth the money. Extremely satisfied!"),
            ("Amit", "Decent build quality. Delivery was quick."),
            ("Priya", "Super fast shipping, works exactly as described."),
            ("Vikram", "Excellent customer service and premium packaging."),
            ("Anjali", "Very stylish and fits perfectly. Love it!"),
            ("Rohan", "Great performance and specs at this price point."),
            ("Kiran", "The color looks beautiful, and it feels high-end."),
            ("Divya", "Absolutely amazing. Exceeded all my expectations!"),
            ("Siddharth", "Very reliable and well built. 5 stars.")
        ]

        db_products = []
        for p_data in products:
            prod = Product.objects.create(**p_data)
            db_products.append(prod)
        
        # Seed Reviews for each product
        for idx, prod in enumerate(db_products):
            rev1_name, rev1_comment = reviewers[idx % len(reviewers)]
            rev2_name, rev2_comment = reviewers[(idx + 3) % len(reviewers)]
            
            rating1 = 5 if idx % 2 == 0 else 4
            rating2 = 4 if idx % 3 == 0 else 5
            
            Review.objects.create(
                user_name=rev1_name,
                product=prod,
                rating=rating1,
                comment=rev1_comment
            )
            Review.objects.create(
                user_name=rev2_name,
                product=prod,
                rating=rating2,
                comment=rev2_comment
            )
            
            # Recalculate average rating of product
            prod.rating = (rating1 + rating2) / 2.0
            prod.save()
        
        # Seed Coupons
        Coupon.objects.create(code='SUMMER30', discount_percentage=30, active=True)
        Coupon.objects.create(code='SHOPNOVA10', discount_percentage=10, active=True)

        self.stdout.write(self.style.SUCCESS('Successfully seeded 30 products, coupons, and customer reviews!'))

