from django.urls import path
from . import views

urlpatterns = [
    #  AUTH 
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),

    # DASHBOARD 
    path('dashboard/', views.dashboard, name='dashboard'),

    # CATEGORY MANAGEMENT 
    path('dashboard/categories/', views.admin_categories, name='admin_categories'),
    path('dashboard/categories/add/', views.add_category, name='add_category'),
    path('dashboard/categories/edit/<int:id>/', views.edit_category, name='edit_category'),
    path('dashboard/categories/delete/<int:id>/', views.delete_category, name='delete_category'),

    # MEDICINE / PRODUCT MANAGEMENT
    path('dashboard/medicines/', views.admin_medicines, name='admin_medicines'),
    path('dashboard/medicines/add/', views.add_medicine, name='add_medicine'),
    path('dashboard/medicines/edit/<int:id>/', views.edit_medicine, name='edit_medicine'),
    path('dashboard/medicines/delete/<int:id>/', views.delete_medicine, name='delete_medicine'),

    # DELIVERY LOCATIONS 
    path('dashboard/locations/', views.admin_locations, name='admin_locations'),

    # ORDERS 
    path('dashboard/orders/', views.admin_orders, name='admin_orders'),
]
