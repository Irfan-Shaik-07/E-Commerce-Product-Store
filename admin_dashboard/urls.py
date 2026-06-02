from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('products/', views.product_list, name='admin_product_list'),
    path('products/add/', views.product_add, name='admin_product_add'),
    path('products/edit/<int:pk>/', views.product_edit, name='admin_product_edit'),
    path('products/delete/<int:pk>/', views.product_delete, name='admin_product_delete'),
    path('logs/', views.activity_logs, name='admin_activity_logs'),
]
