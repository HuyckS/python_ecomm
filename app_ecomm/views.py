from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

# ----------- CUSTOMER FUNCTIONS-------------------------


def index(request):
    if 'products' not in request.session:  # May not need this if no add to cart on main page
        request.session['products'] = {}
        request.session['item_count'] = 0
        num = 0
    else:
        num = request.session['item_count']
        products = request.session['products']

    context = {
        'count': num,
        'items': products
    }
    return render(request, 'index.html', context)


def displayProduct(request, product_id):
    if 'products' not in request.session:  # May not need this if no add to cart on main page
        request.session['products'] = {}
        request.session['item_count'] = 0
        num = 0
    else:
        num = request.session['item_count']
        products = request.session['products']

    # maybe add if inventory = 0 -- return out of stock page
    product = Product.objects.get(id=product_id)
    products = request.session['products']
    category = product.category
    cart_amount = len(products)
    context = {
        'count': num,
        'items': products,
        'this_product': product,
        'similar_items':  category,
        'cart': cart_amount
    }
    return render(request, 'product.html', context)


def addToCart(request, product_id, quantity):
    print("In addToCart **********")
    if 'products' not in request.session:  # May not need this if no add to cart on main page
        request.session['products'] = {}
        products = request.session['products']
        request.session['item_count'] = 0
        num = 0
    else:
        num = request.session['item_count']
        products = request.session['products']
    if product_name not in products.keys():
        products['product_id'] = quantity
        num += quantity
    else:
        products['product_id'] += quantity
        num += quantity
    messages.add_message(  # Add this to html
        request,
        message.INFO,
        f'{quantity} items added to your cart.'
    )
    context = {
        'count': num,
        'items': products
    }
    return redirect(f'/products/show/{product_id}')


def orderInfoForm(request):  # create own database of helper functions
    if 'products' not in request.session:
        messages.add_message(request, message.INFO,
                             'Add items to your cart to checkout.')
        return redirect('/')

    cart = request.session['products']

    item_ids = cart.keys()
    cart_total = 0.00
    namesObj = {}
    priceObj = {}
    total_priceObj = {}

    for key, value in cart.items():
        product = Product.objects.get(id=key)
        if key not in namesObj:
            namesObj[key] = product.name
            priceObj[key] = product.price
            total_priceObj[key] = product.price
        else:
            total_priceObj[key] += product.price

    for value in total_priceObj.values():
        cart_total += value

    context = {
        'ids_total_prices': total_priceObj,
        'ids_names': namesObj,
        'ids_prices': priceObj,
        'total': cart_total,
        'cart': item_ids
    }
    return render(request, 'cart_page.html', context)


def createOrder(request):
    errors = Product.objects.validate_order(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            return redirect('')
    if 'address_2' in request.POST:
        full_address = request.POST['address_1'], request.POST['address_2']
    else:
        full_address = request.POST['address_1']

    new_customer = request.POST['first_name'], request.POST['last_name']
    new_recipient = request.POST['recipient_first_name'], request.POST['recipient_last_name']

    newOrder = Order.objects.create(
        customer=new_customer,
        billing_address=full_address,
        billing_city=request.POST['city'],
        billing_state=request.POST['state'],
        billing_zip=request.POST['zip'],
        recipient=new_recipient,
        shipping_address=request.POST['shipping_address'],
        shipping_city=request.POST['shipping_city'],
        shipping_state=request.POST['shipping_state'],
        shipping_zip=request.POST['shipping_zip'],
        products=request.session['products']
    )
    newOrder.save()
    # Receipt page / your order details will be emailed to you -- thanks for shopping
    return redirect('')

# ---------------------ADMIN LOGIN FUNCTIONS-------------------


def displayAdminLogin(request):
    return render(request, 'login.html')


def log_in(request):
    userList = User.objects.filter(email=request.POST['your_email'])
    if userList:
        user = userList[0]
        if bcrypt.checkpw(request.POST['pw'].encode(), user.pw_hash.encode()):
            request.session['user_id'] = user.id
            request.session['name'] = user.first_name
            # messages.add_message(request, message.INFO, 'Login successful!')
            return redirect('/dashboard/orders')
    messages.error(request, "Incorrect login.")
    return redirect('/dashboard/orders')


def log_out(request):
    request.session.clear()
    return redirect('/admin/login')


# ------------ADMIN FUNCTIONS----------------------------


def displayOrders(request):
    if "user_id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/admin/login')
    all_orders = Order.objects.all()
    context = {
        'orders': all_orders,
    }
    return render(request, 'status.html', context)


def displayInventory(request):
    if "user_id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/admin/login')
    inventory = Product.objects.all()
    context = {
        'products': inventory
    }
    return render(request, 'inventory.html', context)


def productForm(request):
    if "user_id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/admin/login')
    return render(request, 'addProduct.html')


def editForm(request):
    if "user_id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/admin/login')
    return render(request, 'editProduct.html')


def createProduct(request):
    if "user_id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/admin/login')

    errors = Product.objects.validate_product(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            return redirect('/dashboard/products')

    user_id = request.session['user_id']
    this_user = User.objects.get(id=user_id)

    newProduct = Product.objects.create(
        name=request.POST['name'],
        desc=request.POST['desc'],
        category=request.POST['cat'],
        image=request.POST['img'],
        inventory_count=request.POST['count'],
        price=request.POST['price'],   # add to the html!!!!
        user=this_user
    )

    newProduct.save()

    return redirect('/dashboard/products')

# def product_page(request, product_id):
#     print('\n-----------> product HTML show id:', product_id)
#     return render(request, 'product.html')

# def cart_page(request):
#     print('\n-----------> cart HTML page')
#     return render(request, 'cart_page.html')


def editProduct(request, product_id):
    if "user_id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/admin/login')

    errors = Product.objects.validate_product(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            return redirect('/dashboard/products')

    user_id = request.session['user_id']
    this_user = User.objects.get(id=user_id)
    this_product = Product.objects.get(id=product_id)

    post_keys = request.POST.keys()

    if key in post_keys:
        # make sure names in html match model field names
        this_product.key = request.session['key']
    this_product.save()

    return redirect('/dashboard/products')


def displayPreview(request, product_id):
    if "user_id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/admin/login')
    context = {
        'preview_name': request.POST['name'],
        'preview_desc': request.POST['desc'],
        'preview_category': request.POST['cat'],
        'preview_image': request.POST['img'],
        'preview_price': request.POST['price']
    }
    return render(request, 'previewProduct.html', context)


def displayOrder(request):
    pass
