from django.contrib import admin
from .models import *

# Register the Category model in the admin site.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Register the Product model in the admin site.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'manufacturer')
    list_filter = ('category',)
    search_fields = ('name',)

# Register the Cart model in the admin site.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)

# Register the CartItem model in the admin site.
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')

# Register the Order model in the admin site.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'order_status', 'order_date', 'delivery_date')
    list_filter = ('order_status',)
    search_fields = ('user__username', 'order_id')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    list_filter = ('order', 'product')
    search_fields = ('order__order_id', 'product__name')  # Example search fields

# Register the OrderItem model with its admin class
admin.site.register(OrderItem, OrderItemAdmin)