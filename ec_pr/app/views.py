from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

from .models import (
    Customer,
    Product,
    Cart,
    OrderItem,
    PlaceOrder,
    Wishlist,
    Category,
)

from .forms import (
    LoginForm,
    CustomerProfileForm,
    UserProfileForm,
    CustomerRegistrationForm
)

# --------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------

class UserLoginView(LoginView):
    template_name = 'app/login.html'
    authentication_form = LoginForm


# --------------------------------------------------
# BASIC PAGES (LOGIN REQUIRED)
# --------------------------------------------------

@login_required(login_url='login')
def home(request):
    return render(request, 'app/home.html')


@login_required(login_url='login')
def about(request):
    return render(request, 'app/about.html')


@login_required(login_url='login')
def contact(request):
    return render(request, 'app/contact.html')

@login_required(login_url='login')
def search(request):
    query = request.GET.get('q')

    products = Product.objects.none()

    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(category__icontains=query)
        )

    return render(request, 'app/search_results.html', {
        'query': query,
        'products': products
    })
# --------------------------------------------------
# PRODUCT VIEWS
# --------------------------------------------------

class CategoryView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, val):
        # ✅ correct filter for CharField
        products = Product.objects.filter(category=val)

        # Sidebar subcategories (manual text)
        subcategories = (
            Product.objects
            .filter(category=val)
            .values_list('subcategory', flat=True)
            .distinct()
        )

        context = {
            'product': products,
            'subcategories': subcategories,
            'active_category': val,
        }
        return render(request, 'app/category.html', context)

class SubCategoryView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, val, sub):
        products = Product.objects.filter(
            category__code=val,
            subcategory=sub
        )

        subcategories = (
            Product.objects
            .filter(category__code=val)
            .values_list('subcategory', flat=True)
            .distinct()
        )

        return render(request, 'app/category.html', {
            'product': products,
            'subcategories': subcategories,
            'active_subcategory': sub,
        })

    
class CategoryTitle(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(
            category=product[0].category
        ).values('title')
        return render(request, 'app/category.html', locals())


class ProductDetail(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', locals())


# --------------------------------------------------
# USER REGISTRATION
# --------------------------------------------------

class CustomerRegistrationView(View):

    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Registration successful. Please login.'
            )
            return redirect('login')

        messages.error(request, 'Please correct the errors below.')
        return render(request, 'app/customerregistration.html', {'form': form})


# --------------------------------------------------
# PROFILE VIEW (PROFILE + ADDRESS ON SAME PAGE)
# --------------------------------------------------

class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        # User & Profile
        profile, _ = Customer.objects.get_or_create(user=request.user)

        user_form = UserProfileForm(instance=request.user)
        profile_form = CustomerProfileForm(instance=profile)

        # 🔥 CART DATA
        cart = Cart.objects.filter(user=request.user)
        amount = sum(item.total_cost for item in cart)
        shipping_amount = 40 if cart else 0
        totalamount = amount + shipping_amount

        # 🔥 ORDER DATA (THIS WAS MISSING)
        orders = PlaceOrder.objects.filter(
            user=request.user
        ).prefetch_related('items__product').order_by('-created_at')

        wishlist = Wishlist.objects.filter(user=request.user)



        return render(request, 'app/profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'cart': cart,
            'amount': amount,
            'totalamount': totalamount,
            'orders': orders,
            'wishlist': wishlist,  
        })


    def post(self, request):
        profile, _ = Customer.objects.get_or_create(user=request.user)

        # ADDRESS UPDATE
        if 'submit_address' in request.POST:
            profile_form = CustomerProfileForm(
                request.POST,
                instance=profile
            )
            if profile_form.is_valid():
                profile_form.save()
                messages.success(
                    request,
                    'Address updated successfully.'
                )
                return redirect('profile')

        # PROFILE UPDATE
        elif 'submit_profile' in request.POST:
            user_form = UserProfileForm(
                request.POST,
                instance=request.user
            )
            profile_form = CustomerProfileForm(
                request.POST,
                request.FILES, 
                instance=profile
            )
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(
                    request,
                    'Profile updated successfully.'
                )
                return redirect('profile')

        return redirect('profile')

# --------------------------------------------------
# ADDRESS PAGE (SEPARATE PAGE)
# --------------------------------------------------

class AddressView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        profile, _ = Customer.objects.get_or_create(user=request.user)
        profile_form = CustomerProfileForm(instance=profile)

        return render(request, 'app/address.html', {
            'profile': profile,
            'profile_form': profile_form
        })

    def post(self, request):
        profile, _ = Customer.objects.get_or_create(user=request.user)
        profile_form = CustomerProfileForm(
            request.POST,
            instance=profile
        )

        if profile_form.is_valid():
            profile_form.save()
            messages.success(
                request,
                'Address saved successfully.'
            )
            return redirect('address')

        messages.error(request, 'Please correct the errors below.')
        return render(request, 'app/address.html', {
            'profile': profile,
            'profile_form': profile_form
        })

@login_required(login_url='login')
def add_to_cart(request):
    product_id = request.GET.get('prod_id')

    product = get_object_or_404(Product, id=product_id)

    # 🔥 FIX: use filter().first() OR get_or_create
    cart_item = Cart.objects.filter(
        user=request.user,
        product=product
    ).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(
            user=request.user,
            product=product,
            quantity=1
        )

    return redirect('show_cart')


# -------------------------
# SHOW CART
# -------------------------
@login_required(login_url='login')
def show_cart(request):
    cart = Cart.objects.filter(user=request.user)

    amount = 0
    for item in cart:
        amount += item.total_cost

    shipping_amount = 40
    totalamount = amount + shipping_amount

    return render(request, 'app/addtocart.html', {
        'cart': cart,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'totalamount': totalamount,
    })



@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = Cart.objects.get(
            product_id=prod_id,
            user=request.user
        )
        cart_item.quantity += 1
        cart_item.save()

        return JsonResponse({
            'quantity': cart_item.quantity,
            'total_cost': cart_item.total_cost
        })


@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = Cart.objects.get(
            product_id=prod_id,
            user=request.user
        )

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        return JsonResponse({
            'quantity': cart_item.quantity,
            'total_cost': cart_item.total_cost
        })

@login_required(login_url='login')
def buy_now(request):
    prod_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=prod_id)

    # 🔥 SAFE: respect UNIQUE constraint
    cart_item = Cart.objects.filter(
        user=request.user,
        product=product
    ).first()

    if cart_item:
        # Optional: force quantity to 1 for Buy Now
        cart_item.quantity = 1
        cart_item.save()
    else:
        Cart.objects.create(
            user=request.user,
            product=product,
            quantity=1
        )

    # 🚀 Go directly to checkout flow
    return redirect('checkout')



@login_required(login_url='login')
def checkout(request):
    cart = Cart.objects.filter(user=request.user)

    amount = sum(item.total_cost for item in cart)
    shipping_amount = 40 if cart else 0
    totalamount = amount + shipping_amount

    return render(request, 'app/checkout.html', {
        'cart': cart,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'totalamount': totalamount,
    })

@login_required(login_url='login')
def remove_cart_item(request):
    prod_id = request.GET.get('prod_id')

    if prod_id:
        cart_item = Cart.objects.filter(
            user=request.user,
            product_id=prod_id
        ).first()   # 🔥 ONLY ONE ITEM

        if cart_item:
            cart_item.delete()

    return redirect('checkout')



@login_required(login_url='login')
def payment(request):
    cart = Cart.objects.filter(user=request.user)

    if not cart.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('home')

    amount = sum(item.total_cost for item in cart)
    shipping_amount = 40
    totalamount = amount + shipping_amount

    return render(request, 'app/payment.html', {
        'cart': cart,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'totalamount': totalamount
    })


@login_required(login_url='login')
def place_order(request):
    if request.method != 'POST':
        return redirect('payment')

    cart = Cart.objects.filter(user=request.user)
    if not cart.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('home')

    address_id = request.session.get('address_id')
    if not address_id:
        messages.error(request, 'Please select delivery address.')
        return redirect('confirm_address')

    address = get_object_or_404(Customer, id=address_id)

    amount = sum(item.total_cost for item in cart) + 40

    # ✅ CREATE NEW ORDER EVERY TIME
    order = PlaceOrder.objects.create(
        user=request.user,
        address=address,
        amount=amount,
        paid=True
    )

    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.discounted_price
        )

    # ✅ CLEAR CART
    cart.delete()
    request.session.pop('address_id', None)

    # ✅ SEND EMAIL
    send_mail(
        subject='Order Confirmed - SellDesk',
        message=(
            f'Hello {request.user.username},\n\n'
            f'Your order #{order.id} has been placed successfully.\n'
            f'Total Paid: ₹{amount}\n\n'
            'Thank you for shopping with SellDesk!'
        ),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
        fail_silently=False,
    )

    return redirect('order_success')


@login_required(login_url='login')
def order_success(request):
    return render(request, 'app/order_success.html')

@login_required(login_url='login')
def confirm_address(request):
    cart = Cart.objects.filter(user=request.user)

    if not cart.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('home')

    addresses = Customer.objects.filter(user=request.user)

    if request.method == 'POST':
        address_id = request.POST.get('address')

        if not address_id:
            messages.error(request, 'Please select an address.')
            return redirect('confirm_address')

        request.session['address_id'] = address_id
        return redirect('payment')

    return render(request, 'app/confirm_address.html', {
        'addresses': addresses
    })

@login_required(login_url='login')
def add_to_wishlist(request):
    prod_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=prod_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    messages.success(request, 'Added to wishlist ❤️')
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required(login_url='login')
def remove_from_wishlist(request):
    prod_id = request.GET.get('prod_id')

    Wishlist.objects.filter(
        user=request.user,
        product_id=prod_id
    ).delete()

    messages.success(request, 'Removed from wishlist')
    return redirect('profile')
