from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm, CustomPasswordChangeForm
from .views import (
    UserLoginView,
    CustomerRegistrationView,
    ProfileView,
    AddressView,
)

urlpatterns = [

    # -----------------------
    # AUTHENTICATION
    # -----------------------

    path(
        '',
        UserLoginView.as_view(),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='login'),
        name='logout'
    ),

    path(
        'register/',
        CustomerRegistrationView.as_view(),
        name='register'
    ),

    # -----------------------
    # PASSWORD RESET
    # -----------------------

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='app/password_reset.html'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='app/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='app/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='app/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # -----------------------
    # PASSWORD CHANGE
    # -----------------------

path(
    'password-change/',
    auth_views.PasswordChangeView.as_view(
        template_name='app/password_change.html',
        form_class=CustomPasswordChangeForm,
        success_url='/profile/'
    ),
    name='password_change'
),
    # -----------------------
    # PROTECTED PAGES (LOGIN REQUIRED)
    # -----------------------

    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),


    # app/urls.py
    path('category/<str:val>/', views.CategoryView.as_view(), name='category'),
    path('category-title/<slug:val>/', views.CategoryTitle.as_view(), name='category-title'),
    path(
    'category/<str:val>/<str:sub>/',
    views.SubCategoryView.as_view(),
    name='subcategory'
    ),
    path('product-detail/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('address/', AddressView.as_view(), name='address'),

    #add to cart
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),  # ✅ THIS IS REQUIRED
    path('cart/', views.show_cart, name='show_cart'),

    # AJAX CALLS FOR CART QUANTITY UPDATE
    path('plus-cart/', views.plus_cart, name='plus_cart'),
    path('minus-cart/', views.minus_cart, name='minus_cart'),

    #buy product paths
    path('buy-now/', views.buy_now, name='buy_now'),
    path('checkout/', views.checkout, name='checkout'),
    path('remove-cart-item/', views.remove_cart_item, name='remove_cart_item'),

    #payment proceed step path
    path('payment/', views.payment, name='payment'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('confirm-address/', views.confirm_address, name='confirm_address'),

    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),




]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )