from django.db import models
from PIL.Image import core as _imaging

class User (models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # products


class ProductManager(models.Manager):
    def validate_product(request, post_data):
        errors = {}

        return errors


class Product(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(max_length=255)
    category = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products')
    inventory_count = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    user = models.ForeignKey(
        User, related_name="created_products", on_delete=models.CASCADE)
    objects = ProductManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # orders_with_product


class OrderManager(models.Manager):
    def validate_order(request, post_data):
        errors = {}

        return errors


class Order(models.Model):
    customer = models.CharField(max_length=255)
    billing_address = models.TextField(max_length=255)
    shipping_address = models.TextField(max_length=255)
    products = models.ManyToManyField(
        Product, related_name='orders_with_product')
    # total = models.DecimalField(max_digits=9, decimal_places=2)
    objects = OrderManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
