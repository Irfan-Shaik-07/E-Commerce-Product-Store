from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/<int:product_id>/', views.checkout_view, name='checkout_product'),
]
