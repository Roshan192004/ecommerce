from django.shortcuts import render, get_object_or_404
from adminapp.models import Category, Medicine


#  HOME PAGE 

def home(request):
    location = request.session.get('delivery_location')

    # Fetch categories added from admin
    categories = Category.objects.filter(is_active=True)

    return render(request, 'main/home.html', {
        'location': location,
        'categories': categories
    })


#  LANDING PAGE 

def landing(request):
    return render(request, 'main/landing.html')


# ALL CATEGORIES (A–Z)

def all_medicines(request):
    categories = Category.objects.filter(is_active=True).order_by("name")

    return render(request, "main/product_list.html", {
        "categories": categories
    })


# ================= CATEGORY → MEDICINES =================
# This replaces acne_medicines (DYNAMIC)

def category_medicines(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    medicines = Medicine.objects.filter(category=category)

    return render(request, "main/medicine_list.html", {
        "category": category,
        "medicines": medicines
    })


# category page
def category_page(request):
    categories = Category.objects.filter(is_active=True)[:]

    return render(request, 'main/category_page.html', {
        'categories': categories
        
    })
    
def categories_focus(request):
    categories = Category.objects.filter(is_active=True)
    # products = Product.objects.filter(category=category)
    return render(request, 'main/categories_focus.html', {
        'categories': categories,
        # 'products'  : products
    })
    
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Medicine.objects.filter(category=category)

    return render(request, 'main/category_detail.html', {
        'category': category,
        'products': products
    })
    
