from django.urls import path
from . import views


urlpatterns = [
    # CUSTOMER ROUTES
    path('', views.index),
    path('products/show/<int:product_id>', views.displayProduct),
    path('products/show/<int:product_id>/add/<int:quantity>', views.addToCart),
    path('cart', views.orderInfoForm),
    path('checkout', views.createOrder),

    # LOGIN ROUTES
    path('admin/login', views.displayAdminLogin),
    path('admin/login/success', views.log_in),
    path('admin/logout', views.log_out),

    # ADMIN ROUTES
    path('dashboard/orders', views.displayOrders),
    path('dashboard/products', views.displayInventory),
    path('dashboard/products/create', views.createProduct),
    path('dashboard/products/edit/<int:product_id>', views.editProduct),
    path('dashboard/products/preview', views.displayPreview),
    path('dashboard/orders/show/<int:order_id>', views.displayOrder)
]
