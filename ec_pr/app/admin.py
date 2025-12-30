from django.contrib import admin
from .models import (
    Customer,
    Product,
    Cart,
    PlaceOrder,
    OrderItem,
    Wishlist
)

# -----------------------------
# CUSTOMER
# -----------------------------
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'name',
        'city',
        'state',
        'zipcode'
    )
    search_fields = ('user__username', 'name', 'city')
    list_filter = ('state',)


# -----------------------------
# PRODUCT
# -----------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'subcategory',
        'discounted_price'
    )
    list_filter = ('category',)
    search_fields = ('title', 'subcategory')


# -----------------------------
# CART
# -----------------------------
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'product',
        'quantity'
    )
    search_fields = ('user__username', 'product__title')


# -----------------------------
# PLACE ORDER (MAIN ORDER)
# -----------------------------
@admin.register(PlaceOrder)
class PlaceOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'amount',
        'status',
        'paid',
        'created_at',
    )
    list_filter = ('status', 'paid', 'created_at')



# -----------------------------
# ORDER ITEMS
# -----------------------------
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'quantity',
        'price'
    )
    search_fields = ('product__title', 'order__user__username')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'added_at')
