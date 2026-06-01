from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # API endpoints
    path('products/', views.ProductAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductAPIView.as_view(), name='product-detail'),
    
    # Interactive Playground UI
    path('playground/', views.PlaygroundView.as_view(), name='playground'),
]
