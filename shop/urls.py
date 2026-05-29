from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup, name='signup'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('return/', views.return_request, name='return'),
    path('logout/', views.logout_page, name='logout'),
    path(
    'add-to-cart/<int:product_id>/',
    views.add_to_cart,
    name='add_to_cart'
),path(
    'remove-cart/<int:cart_id>/',
    views.remove_cart_item,
    name='remove_cart_item'
),path(
    'clear-cart/',
    views.clear_cart,
    name='clear_cart'
),
path(
    'increase/<int:cart_id>/',
    views.increase_quantity,
    name='increase_quantity'
),

path(
    'decrease/<int:cart_id>/',
    views.decrease_quantity,
    name='decrease_quantity'
),
]