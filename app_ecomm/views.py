from django.shortcuts import render, redirect, HttpResponse


def index(request):
    return render(request, 'index.html')


def log_in(request):
    userList = User.objects.filter(email=request.POST['your_email'])
    if userList:
        user = userList[0]
        if bcrypt.checkpw(request.POST['pw'].encode(), user.pw_hash.encode()):
            request.session['user_id'] = user.id
            request.session['name'] = user.first_name
            return redirect('/success')
    messages.error(request, "Incorrect login.")
    return redirect('/')


def log_out(request):
    request.session.clear()
    return redirect('/')


def createOrder(request):
    pass


def createProduct(request):
    if "user_id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/')

    errors = Product.objects.validate_product(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            return redirect('/dashboard/products')

    user_id = request.session['user_id']
    this_user = User.objects.get(id=user_id)
    add_name = request.POST['name']
    add_desc = request.POST['desc']
    add_cat = request.POST['cat']
    add_img = request.POST['img']
    add_count = request.POST['count']
    add_user = this_user

    newProduct = Product.objects.create(
        name=add_name,
        desc=add_desc,
        category=add_cat,
        image=add_img,
        user=add_user,
        inventory_count=count
    )

    newProduct.save()

    return redirect('/dashboard/products')

def product_page(request, product_id):
    print('\n-----------> product HTML show id:', product_id)
    return render(request, 'product.html')

def cart_page(request):
    print('\n-----------> cart HTML page')
    return render(request, 'cart_page.html')