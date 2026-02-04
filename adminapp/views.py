from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from collections import defaultdict
from .models import HealthCategory
from .models import Category, Medicine, DeliveryLocation
from userapp.models import Order, OrderItem
from .forms import HealthCategoryForm

# ADMIN CHECK

def is_admin(user):
    return user.is_staff or user.is_superuser


# ADMIN LOGIN

def admin_login(request):
    if request.user.is_authenticated and is_admin(request.user):
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user and is_admin(user):
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid admin credentials")

    return render(request, "adminapp/admin_login.html")


# ADMIN LOGOUT

@login_required
def admin_logout(request):
    logout(request)
    return redirect('home')


# ADMIN DASHBOARD

@login_required
@user_passes_test(is_admin)
def dashboard(request):
    orders = Order.objects.all()

    total_orders = orders.count()

    total_sales = sum(
        item.medicine.price * item.quantity
        for order in orders
        for item in order.orderitem_set.all()
        if order.status == "PLACED"
    )

    users_count = User.objects.count()

    return render(request, "adminapp/dashboard.html", {
        "users_count": users_count,
        "total_orders": total_orders,
        "total_sales": total_sales,
        "orders": orders,
    })


# ADMIN CATEGORIES

@login_required
@user_passes_test(is_admin)
def admin_categories(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Category.objects.create(name=name)

    categories = Category.objects.all()
    return render(request, "adminapp/categories.html", {
        "categories": categories
    })


# ADMIN MEDICINES

@login_required
@user_passes_test(is_admin)
def admin_medicines(request):
    if request.method == "POST":
        Medicine.objects.create(
            name=request.POST.get("name"),
            price=request.POST.get("price"),
            stock=request.POST.get("stock"),
            category_id=request.POST.get("category")
        )

    medicines = Medicine.objects.all()
    categories = Category.objects.all()

    return render(request, "adminapp/medicines.html", {
        "medicines": medicines,
        "categories": categories
    })


# ADMIN DELIVERY LOCATIONS

@login_required
@user_passes_test(is_admin)
def admin_locations(request):
    if request.method == "POST":
        DeliveryLocation.objects.create(
            city=request.POST.get("city"),
            pincode=request.POST.get("pincode")
        )

    locations = DeliveryLocation.objects.all()
    return render(request, "adminapp/locations.html", {
        "locations": locations
    })

# ADMIN ORDERS

@login_required
@user_passes_test(is_admin)
def admin_orders(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        new_status = request.POST.get("status")
        Order.objects.filter(id=order_id).update(status=new_status)

    orders = Order.objects.all().order_by("-created_at")

    return render(request, "adminapp/orders.html", {
        "orders": orders
    })



# USER SIDE – ALL MEDICINES

def all_medicines(request):
    categories = Category.objects.all().order_by("name")
    grouped_categories = defaultdict(list)

    for category in categories:
        grouped_categories[category.name[0].upper()].append(category)

    return render(request, "medicines/all_medicines.html", {
        "grouped_categories": dict(grouped_categories)
    })


# USER SIDE – CATEGORY MEDICINES

def acne_medicines(request):
    category_name = request.GET.get("category")
    category = Category.objects.get(name=category_name)
    medicines = Medicine.objects.filter(category=category)

    return render(request, "medicines/acne_medicines.html", {
        "medicines": medicines,
        "category": category
    })

def admin_health_categories(request):
    categories = HealthCategory.objects.all()
    return render(request, 'adminapp/health_categories.html', {
        'categories': categories
    })

def add_health_category(request):
    form = HealthCategoryForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('admin_health_categories')
    return render(request, 'adminapp/health_category_form.html', {'form': form})

def edit_health_category(request, id):
    category = get_object_or_404(HealthCategory, id=id)
    form = HealthCategoryForm(request.POST or None, request.FILES or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('admin_health_categories')
    return render(request, 'adminapp/health_category_form.html', {'form': form})


def admin_categories(request):
    categories = Category.objects.all()
    return render(request, 'adminapp/categories.html', {'categories': categories})


def add_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('admin_categories')
    return render(request, 'adminapp/category_form.html', {'form': form})


def edit_category(request, id):
    category = get_object_or_404(Category, id=id)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('admin_categories')
    return render(request, 'adminapp/category_form.html', {'form': form})