from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from adminapp.models import Medicine
from .models import Order, OrderItem
from adminapp.models import DeliveryLocation
from adminapp.models import ServiceableLocation

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

    # ALWAYS get the latest pending order (cart)
    order = Order.objects.filter(
        user=request.user,
        status="PENDING"
    ).order_by('-created_at').first()

    # If no pending cart exists, create one
    if not order:
        order = Order.objects.create(
            user=request.user,
            status="PENDING"
        )

    # Add or update item
    item, created = OrderItem.objects.get_or_create(
        order=order,
        medicine=medicine
    )

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
        status="PENDING"
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
    # ❌ BLOCK ONLY IF LOCATION NOT SET
    if "delivery_location" not in request.session:
        messages.error(request, "Unable to deliver at your location")
        return redirect("cart")

    order = Order.objects.filter(
        user=request.user,
        status="PENDING"
    ).first()

    if not order:
        messages.error(request, "Your cart is empty")
        return redirect("cart")

    items = OrderItem.objects.filter(order=order)
    total = sum(item.medicine.price * item.quantity for item in items)

    return render(request, "userapp/checkout.html", {
        "order": order,
        "items": items,
        "total": total
    })

   


@login_required
def place_order(request):
    if "delivery_location" not in request.session:
        messages.error(request, "Unable to deliver at your location")
        return redirect("checkout")

    order = Order.objects.filter(
        user=request.user,
        status="PENDING"
    ).first()

    if not order:
        messages.error(request, "No active order found")
        return redirect("cart")

    # ✅ PLACE ORDER
    order.status = "PLACED"
    order.save()

    messages.success(request, "Order placed successfully!")
    return redirect("order_success")



@login_required
def order_success(request):
    return render(request, 'userapp/order_success.html')

@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user,
        # is_completed=True
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


# delivery Location


def set_location(request):
    if request.method == "POST":
        pincode = request.POST.get("pincode")

        try:
            location = DeliveryLocation.objects.get(pincode=pincode)

            # ✅ VALID LOCATION
            request.session["delivery_location"] = {
                "city": location.city,
                "pincode": location.pincode
            }
            request.session.pop("delivery_error", None)

        except DeliveryLocation.DoesNotExist:
            # ❌ INVALID LOCATION
            request.session.pop("delivery_location", None)
            request.session["delivery_error"] = "Unable to deliver at your location"

    return redirect(request.META.get("HTTP_REFERER", "/"))


def role_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")  # user or admin

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password")
            return redirect("login")

        # ✅ ADMIN LOGIN
        if role == "admin":
            if user.is_staff or user.is_superuser:
                login(request, user)
                return redirect("dashboard")   # admin dashboard
            else:
                messages.error(request, "You are not authorized as admin")
                return redirect("login")

        # ✅ USER LOGIN
        if role == "user":
            if not user.is_staff:
                login(request, user)
                return redirect("home")  # user homepage
            else:
                messages.error(request, "Admin cannot login as user")
                return redirect("login")

    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


from adminapp.models import HealthCategory

def home(request):
    health_categories = HealthCategory.objects.filter(is_active=True)

    return render(request, 'userapp/home.html', {
        'health_categories': health_categories
    })