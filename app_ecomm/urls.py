from django.urls import path
from . import views


urlpatterns = [
    # CUSTOMER ROUTES
    path('', views.index),
    path('products/show/<int:product_id>', views.displayProduct),
    path('products/show/<int:product_id>/add', views.addToCart),
    path('cart', views.createOrder),

    # LOGIN ROUTES
    path('admin/login', views.displayAdminLogin)
    path('dashboard/orders', views.log_in),
    path('admin/logout', views.log_out),

    # # ADMIN ROUTES
    # path('', views.displayOrders),
    # path('', views.displayInventory),
    # path('', views.createProduct),
    # path('', views.editProduct),
    # path('', views.displayPreview)
]
