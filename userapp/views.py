from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from adminapp.models import Medicine
from .models import Order, OrderItem


# ----------------------------
# ----------------------------
# REGISTER
# ----------------------------
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'userapp/register.html')
# ----------------------------
# LOGIN
# ----------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # home page
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'userapp/login.html')
# ----------------------------
# LOGOUT
# ----------------------------
def logout_view(request):
    logout(request)
    return redirect('home')

# ADD TO CART
# ----------------------------
@login_required
def add_to_cart(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)

    # Get or create active order (cart)
    order, created = Order.objects.get_or_create(
        user=request.user,
        is_completed=False
    )

    # Get or create order item
    item, created = OrderItem.objects.get_or_create(
        order=order,
        medicine=medicine
    )

    # Increase quantity if already exists
    if not created:
        item.quantity += 1
    item.save()

    return redirect('cart')


# ----------------------------
# CART PAGE
# ----------------------------
@login_required
def cart_view(request):
    order = Order.objects.filter(
        user=request.user,
        is_completed=False
    ).first()

    items = OrderItem.objects.filter(order=order) if order else []

    total = 0
    for item in items:
        total += item.medicine.price * item.quantity

    return render(request, 'userapp/cart.html', {
        'items': items,
        'total': total
    })
    
@login_required
def checkout_view(request):
    order = Order.objects.filter(
        user=request.user,
        is_completed=False
    ).first()

    if not order:
        messages.error(request, "Your cart is empty")
        return redirect('cart')

    items = OrderItem.objects.filter(order=order)

    total = 0
    for item in items:
        total += item.medicine.price * item.quantity

    return render(request, 'userapp/checkout.html', {
        'order': order,
        'items': items,
        'total': total
    })

@login_required
def place_order(request):
    order = Order.objects.filter(
        user=request.user,
        is_completed=False
    ).first()

    if not order:
        messages.error(request, "No active order found")
        return redirect('cart')

    order.is_completed = True
    order.save()

    messages.success(request, "Order placed successfully!")
    return redirect('order_success')

@login_required
def order_success(request):
    return render(request, 'userapp/order_success.html')

@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user,
        is_completed=True
    ).order_by('-created_at')

    return render(request, 'userapp/my_orders.html', {
        'orders': orders
    })

# ----------------------------
# INCREASE QUANTITY
# ----------------------------
@login_required
def increase_qty(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart')


# ----------------------------
# DECREASE QUANTITY
# ----------------------------
@login_required
def decrease_qty(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')


# ----------------------------
# REMOVE ITEM FROM CART
# ----------------------------
@login_required
def remove_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    item.delete()
    return redirect('cart')
