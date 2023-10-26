from django.urls import path
from products.views import *

urlpatterns = [
    # Categories
    path('categories/', CategoryListView.as_view(), name='category-list'),  # List and create categories

    # Seller Products
    path('products/', SellerProductListView.as_view(), name='seller-product-list'),  # List seller's products
    path('products/<int:pk>/', SellerProductDetailView.as_view(), name='product-detail'),  # Retrieve, update, or delete a specific product

    # Products (for all users)
    path('product/', ProductListView.as_view(), name='product-list'),  # List all products
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),  # Retrieve details of a specific product

    # Cart
    path('cart/', CartView.as_view(), name='user-cart'),  # Retrieve the user's cart
    path('cart/add/', CartItemAddView.as_view(), name='cart-item-add'),  # Add items to the cart
    path('cart/clear/', ClearCartView.as_view(), name='clear-cart'),  # Clear all items from the cart
    path('cart/item/delete/<int:product_id>/', CartItemDeleteView.as_view(), name='cart-item-delete'),  # Delete a specific cart item
    path('cart/item/update/<int:product_id>/', CartItemUpdateView.as_view(), name='cart-item-update'),  # Update the quantity of a cart item

    # Orders
    path('orders/', OrderListView.as_view(), name='order-list'),  # List user's orders
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),  # Retrieve or delete a specific order
    path('create_orders/', OrderCreateView.as_view(), name='create-order'),  # Create a new order
    path('orders/cancel/<int:order_id>/', OrderCancellationView.as_view(), name='order-cancellation'),  # Cancel an order

    # Seller Orders
    path('seller/orders/', SellerOrderListView.as_view(), name='seller-orders'),  # List all orders (for sellers)
    path('seller/orders/<int:pk>/', SellerOrderDetailView.as_view(), name='seller-orders'),  # Retrieve or update a specific order (for sellers)
]
