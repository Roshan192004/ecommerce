from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('medicines/', views.all_medicines, name='all_medicines'),
    # path('update-order/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('medicines/acne/', views.acne_medicines, name='acne_medicines'),
]

