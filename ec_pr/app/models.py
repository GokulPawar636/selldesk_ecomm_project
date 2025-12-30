from django.db import models
from django.contrib.auth.models import User

# ==============================
# STATE CHOICES
# ==============================
STATE_CHOICES = [
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
]

CATEGORY_CHOICES = (
    ('ML', 'Milk'),
    ('CZ', 'Cheese'),
    ('CR', 'Curd'),
    ('IC', 'Ice Cream'),
    ('MS', 'Milk Shake'),
    ('PN', 'Paneer'),
    ('GH', 'Ghee'),
    ('LS', 'Lassi'),
    ('OT', 'Others'),
)

# ==============================
# CATEGORY
# ==============================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ==============================
# PRODUCT
# ==============================
class Product(models.Model):
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES
    )

    # Manual subcategory (optional text)
    subcategory = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Example: Cow Milk, Buffalo Milk"
    )

    title = models.CharField(max_length=200)

    selling_price = models.FloatField()
    discounted_price = models.FloatField()

    product_image = models.ImageField(
        upload_to='product'
    )

    # ✅ NEW FIELDS
    description = models.TextField(
        blank=True,
        help_text="Detailed product description"
    )

    composition = models.CharField(
        max_length=255,
        blank=True,
        help_text="Example: 100% Cow Milk"
    )

    prodapp = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Product Application",
        help_text="Example: Tea, Coffee, Daily Consumption"
    )

    def __str__(self):
        return self.title


# ==============================
# CUSTOMER
# ==============================
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    locality = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(
        max_length=50,
        choices=STATE_CHOICES,
        blank=True
    )
    zipcode = models.IntegerField(blank=True, null=True)

    profile_image = models.ImageField(
        upload_to='profile_images/',
        default='profile_images/default.png',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.username


# ==============================
# CART
# ==============================
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_user_product_cart'
            )
        ]

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"


# ==============================
# PLACE ORDER
# ==============================
class PlaceOrder(models.Model):
    STATUS_CHOICES = (
        ('PLACED', 'Placed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.FloatField()
    paid = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PLACED'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


# ==============================
# ORDER ITEMS
# ==============================
class OrderItem(models.Model):
    order = models.ForeignKey(
        PlaceOrder,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.product.title} × {self.quantity}"


# ==============================
# WISHLIST
# ==============================
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"
