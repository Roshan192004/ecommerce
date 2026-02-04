from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.landing, name='home'), 
    path('medicines/', views.all_medicines, name='all_medicines'),
    # path('medicines/acne/', views.acne_medicines, name='acne_medicines'),
    path('categories:', views.category_page, name='category_page'),
    path('categories/<slug:slug>/', views.category_detail, name='category_detail'),
]
