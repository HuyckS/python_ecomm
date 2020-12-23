from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('product/<int:product_id>', views.product_page),
    path('cart', views.cart_page),
]
