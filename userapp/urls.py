from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:medicine_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:item_id>/', views.increase_qty, name='increase_qty'),
    path('cart/decrease/<int:item_id>/', views.decrease_qty, name='decrease_qty'),
    path('cart/remove/<int:item_id>/', views.remove_item, name='remove_item'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('set-location/', views.set_location, name='set_location'),
    path('set-location/', views.set_location, name='set_location'),
    path('login/', views.role_login, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
