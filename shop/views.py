from django.shortcuts import render
from .models import Product, Order, Contact, ReturnRequest,Cart
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


def home(request):
    return render(request, 'home.html')
def products(request):

    search = request.GET.get('search')

    if search:
        products = Product.objects.filter(
            name__icontains=search
        )
    else:
        products = Product.objects.all()

    return render(
        request,
        'products.html',
        {'products': products}
    )

@login_required(login_url='/login/')
def cart(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )

@login_required(login_url='/login/')
def remove_cart_item(request, cart_id):

    item = Cart.objects.get(
        id=cart_id,
        user=request.user
    )

    item.delete()

    return redirect('/cart/')
@login_required(login_url='/login/')
def clear_cart(request):

    Cart.objects.filter(
        user=request.user
    ).delete()

    return redirect('/cart/')

@login_required(login_url='/login/')
def checkout(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    if not cart_items.exists():

        return render(
            request,
            'checkout.html',
            {
                'error': 'Your cart is empty.'
            }
        )

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    if request.method == "POST":

        address = request.POST.get("address")
        city = request.POST.get("city")
        phone = request.POST.get("phone")

        Order.objects.create(
            user=request.user,
            name=request.user.username,
            email=request.user.email,
            address=address,
            city=city,
            phone=phone,
            total_amount=total
        )

        cart_items.delete()

        return render(
            request,
            'checkout.html',
            {
                'success': True,
                'total': 0
            }
        )

    return render(
        request,
        'checkout.html',
        {
            'total': total
        }
    )


def login_page(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/')

        return render(
            request,
            'login.html',
            {'error': 'Invalid username or password'}
        )

    return render(request, 'login.html')

def signup(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():

            return render(
                request,
                "signup.html",
                {"error": "Username already exists"}
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("/login/")

    return render(request, "signup.html")

def contact(request):

    if request.method == "POST":

        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            message=request.POST.get("message")
        )

        return render(request, "contact.html", {"success": True})

    return render(request, "contact.html")

@login_required(login_url='/login/')
def profile(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-id')

    return render(
        request,
        'profile.html',
        {'orders': orders}
    )

@login_required(login_url='/login/')
def return_request(request):

    if request.method == "POST":

        ReturnRequest.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            reason=request.POST.get("reason"),
            refund_amount=request.POST.get("refund")
        )

        return render(
            request,
            "return.html",
            {"success": True}
        )

    return render(request, "return.html")

@login_required(login_url='/login/')
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart_item = Cart.objects.filter(
        user=request.user,
        product=product
    ).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(
            user=request.user,
            product=product,
            quantity=1
        )

    return redirect('/products/')

def logout_page(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def increase_quantity(request, cart_id):

    item = Cart.objects.get(
        id=cart_id,
        user=request.user
    )

    item.quantity += 1
    item.save()

    return redirect('/cart/')

@login_required(login_url='/login/')
def decrease_quantity(request, cart_id):

    item = Cart.objects.get(
        id=cart_id,
        user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('/cart/')