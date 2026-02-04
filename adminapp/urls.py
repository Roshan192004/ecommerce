from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('medicines/', views.all_medicines, name='all_medicines'),
    path('medicines/acne/', views.acne_medicines, name='acne_medicines'),
    path('admin/categories/', views.admin_categories, name='admin_categories'),
    path('admin/medicines/', views.admin_medicines, name='admin_medicines'),
    path('admin/locations/', views.admin_locations, name='admin_locations'),
    path('dashboard/orders/', views.admin_orders, name='admin_orders'),
    path('dashboard/health-categories/', views.admin_health_categories
, name='health_category_list'),
    # path('dashboard/health-categories/add/', views.health_category_add, name='health_category_add'),
    path('categories/', views.admin_categories, name='admin_categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:id>/', views.edit_category, name='edit_category'),
    path('health-categories/', views.admin_health_categories, name='admin_health_categories'),
    path('health-categories/add/', views.add_health_category, name='add_health_category'),
    path('health-categories/edit/<int:id>/', views.edit_health_category, name='edit_health_category'),

]


