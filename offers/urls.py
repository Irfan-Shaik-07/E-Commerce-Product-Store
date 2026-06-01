from django.urls import path
from . import views

urlpatterns = [
    path('', views.offers_page, name='offers_page'),
]
