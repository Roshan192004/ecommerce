from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Category, Medicine


@login_required
def dashboard(request):
    users_count = User.objects.count()

    # TEMP: order system not active yet
    orders = []
    total_sales = 0

    return render(request, 'adminapp/dashboard.html', {
        'users_count': users_count,
        'orders': orders,
        'total_sales': total_sales
    })

def all_medicines(request):
    categories = Category.objects.all()
    return render(request, "medicines/all_medicines.html", {
        "categories": categories
    })


def acne_medicines(request):
    medicines = Medicine.objects.filter(category__name="Acne")
    return render(request, "medicines/acne_medicines.html", {
        "medicines": medicines
    })


# def acne_medicines(request):
#     medicines = [
#         {
#             "name": "Acne Control Gel",
#             "price": 249,
#             "image": "products/med_1.jpg"
#         },
#         {
#             "name": "Pimple Clear Cream",
#             "price": 199,
#             "image": "products/med_2.jpg"
#         },
#         {
#             "name": "Acne Care Capsules",
#             "price": 349,
#             "image": "products/med_3.jpg"
#         },
#     ]

#     return render(request, "medicines/acne_medicines.html", {
#         "medicines": medicines
#     })
