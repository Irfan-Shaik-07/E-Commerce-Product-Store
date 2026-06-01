from django.urls import path
from . import views

urlpatterns = [
    path('', views.reviews_page, name='reviews_page'),
    path('product/<int:product_id>/', views.reviews_page, name='reviews_product'),
]
