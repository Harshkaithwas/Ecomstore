from django.db import models
from django.conf import settings  # Assuming User is imported from Django auth.

class Category(models.Model):
    """
    Model representing product categories.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    """
    Model representing products available for sale.
    """
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)  # Field for product stock.
    manufacturer = models.CharField(max_length=100, null=True, blank=True)  # Field for manufacturer.
    # Add more fields as needed, such as manufacturer, SKU, and so on.

    def __str__(self):
        return self.name

class Cart(models.Model):
    """
    Model representing a user's shopping cart.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

class CartItem(models.Model):
    """
    Model representing items in a user's shopping cart.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    """
    Model representing customer orders.
    """
    ORDER_STATUS_CHOICES = (
        ('Pending', 'Waiting for Confirmation from Seller'),
        ('Rejected', 'Rejected'),
        ('Confirmed', 'Order Confirmed'),
        ('Ready to Ship', 'Ready to Ship'),
        ('Dispatch', 'Dispatched'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Successfully Delivered'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20, unique=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    payment_method = models.CharField(max_length=100)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')
    order_date = models.DateTimeField(auto_now_add=True)
    order_notes = models.TextField(blank=True, null=True)
    delivery_date = models.DateField(null=True, blank=True)

class OrderItem(models.Model):
    """
    Model representing items within an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
