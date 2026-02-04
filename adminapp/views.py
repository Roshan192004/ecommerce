from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.text import slugify
from .models import Category,Medicine
from .models import DeliveryLocation
from .forms import MedicineForm
from userapp.models import Order, OrderItem


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

    return render(request, "adminpanel/admin_login.html")


#  ADMIN LOGOUT 

@login_required
def admin_logout(request):
    logout(request)
    return redirect('home')


#  ADMIN DASHBOARD 

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

    return render(request, "adminpanel/dashboard.html", {
        "users_count": users_count,
        "total_orders": total_orders,
        "total_sales": total_sales,
        "orders": orders,
    })


# CATEGORY ADMIN 

@login_required
@user_passes_test(is_admin)
def admin_categories(request):
    categories = Category.objects.all()
    return render(request, "adminpanel/categories.html", {
        "categories": categories
    })


@login_required
@user_passes_test(is_admin)
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        slug = request.POST.get("slug")
        image = request.FILES.get("image")
        is_active = request.POST.get("is_active") == "on"

        # Auto-generate slug if empty
        if not slug and name:
            slug = slugify(name)

        category = Category.objects.create(
            name=name,
            slug=slug,
            image=image,
            is_active=is_active
        )

        # Handle buttons
        if "save_add_another" in request.POST:
            return redirect("add_category")

        if "save_continue" in request.POST:
            return redirect("edit_category", id=category.id)
        return redirect("admin_categories")

    return render(request, "adminpanel/category_form.html")

@login_required
@user_passes_test(is_admin)
def edit_category(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == "POST":
        category.name = request.POST.get("name")
        category.slug = slugify(category.name)

        if "image" in request.FILES:
            category.image = request.FILES["image"]

        category.save()
        return redirect("admin_categories")

    return render(request, "adminpanel/category_form.html", {
        "category": category
    })


@login_required
@user_passes_test(is_admin)
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect("admin_categories")


#  MEDICINE / PRODUCT ADMIN 

@login_required
@user_passes_test(is_admin)
def admin_products(request):
    products = Medicine.objects.all()
    categories = Category.objects.all()

    return render(request, "adminpanel/products.html", {
        "products": products,
        "categories": categories
    })


@login_required
@user_passes_test(is_admin)
def add_product(request):
    categories = Category.objects.all()

    if request.method == "POST":
        Medicine.objects.create(
            name=request.POST.get("name"),
            price=request.POST.get("price"),
            stock=request.POST.get("stock"),
            category_id=request.POST.get("category"),
            image=request.FILES.get("image")
        )
        return redirect("admin_products")

    return render(request, "adminpanel/product_form.html", {
        "categories": categories
    })


@login_required
@user_passes_test(is_admin)
def edit_product(request, id):
    product = get_object_or_404(Medicine, id=id)
    categories = Category.objects.all()

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")
        product.category_id = request.POST.get("category")

        if "image" in request.FILES:
            product.image = request.FILES["image"]

        product.save()
        return redirect("admin_products")

    return render(request, "adminpanel/product_form.html", {
        "product": product,
        "categories": categories
    })


@login_required
@user_passes_test(is_admin)
def delete_product(request, id):
    product = get_object_or_404(Medicine, id=id)
    product.delete()
    return redirect("admin_products")


# ================= DELIVERY LOCATIONS =================

@login_required
@user_passes_test(is_admin)
def admin_locations(request):
    if request.method == "POST":
        DeliveryLocation.objects.create(
            city=request.POST.get("city"),
            pincode=request.POST.get("pincode")
        )

    locations = DeliveryLocation.objects.all()
    return render(request, "adminpanel/locations.html", {
        "locations": locations
    })


# ================= ADMIN ORDERS =================

@login_required
@user_passes_test(is_admin)
def admin_orders(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        new_status = request.POST.get("status")
        Order.objects.filter(id=order_id).update(status=new_status)

    orders = Order.objects.all().order_by("-created_at")

    return render(request, "adminpanel/orders.html", {
        "orders": orders
    })
    

#  admin add_medicine

@login_required
@user_passes_test(is_admin)
def admin_medicines(request):
    medicines = Medicine.objects.all()
    return render(request, 'adminpanel/medicines.html', {
        'medicines': medicines
    })

@login_required
@user_passes_test(is_admin)
def add_medicine(request):
    form = MedicineForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('admin_medicines')

    return render(request, 'adminpanel/medicine_form.html', {
        'form': form
    })
    
@login_required
@user_passes_test(is_admin)
def edit_medicine(request, id):
    medicine = get_object_or_404(Medicine, id=id)
    form = MedicineForm(request.POST or None, request.FILES or None, instance=medicine)

    if form.is_valid():
        form.save()
        return redirect('admin_medicines')

    return render(request, 'adminpanel/medicine_form.html', {
        'form': form,
        'edit': True
    })
    

@login_required
@user_passes_test(is_admin)
def delete_medicine(request, id):
    medicine = get_object_or_404(Medicine, id=id)
    medicine.delete()
    return redirect('admin_medicines')
