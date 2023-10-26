from rest_framework import serializers
from products.models import *

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    """
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category', 'image', 'stock', 'manufacturer')

class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed Product information.
    """
    class Meta:
        model = Product
        fields = '__all__'

class ProductListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing Product information.
    """
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'image')

class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for CartItem model, including product details.
    """
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ('product', 'quantity')

class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for Cart model, including related CartItem information and total value.
    """
    items = CartItemSerializer(source='cartitem_set', many=True)
    total_value = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items', 'total_value')

    def get_total_value(self, obj):
        # Calculate the total value of the cart by summing the prices of all items
        total_value = sum(item.product.price * item.quantity for item in obj.cartitem_set.all())
        return total_value

class CartItemAddSerializer(serializers.Serializer):
    """
    Serializer for adding items to the cart.
    """
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class CartItemDeleteSerializer(serializers.Serializer):
    """
    Serializer for deleting items from the cart.
    """
    pass

class CartItemUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating the quantity of items in the cart, including validation.
    """
    quantity = serializers.IntegerField(min_value=1)

    def validate_quantity(self, value):
        # Get the cart item's product
        product = self.context['cart_item'].product

        # Check if the requested quantity exceeds the product's stock
        if value > product.stock:
            raise serializers.ValidationError("The requested quantity exceeds the available stock.")

        return value

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model, including product details.
    """
    product = ProductDetailSerializer()

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')

class OrderListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing Order information.
    """
    class Meta:
        model = Order
        fields = [
            "id",
            "order_id",
            "total_price",
            "shipping_address",
            "payment_method",
            "order_status",
            "order_date",
            "order_notes",
            "delivery_date",
            "user",
        ]

class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed Order information, including order items.
    """
    orderitem_set = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_orderitem_set(self, obj):
        order_items = obj.orderitem_set.all()
        product_details = []

        for order_item in order_items:
            product_detail = {
                "product": ProductDetailSerializer(order_item.product).data,
                "quantity": order_item.quantity
            }
            product_details.append(product_detail)

        return product_details

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model, including order items.
    """
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_orderitem_set(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        return OrderItemSerializer(order_items, many=True).data

class OrderCreateSerializer(serializers.Serializer):
    """
    Serializer for creating a new order, including order items.
    """
    shipping_address = serializers.CharField()
    payment_method = serializers.CharField()
    order_notes = serializers.CharField(allow_blank=True, required=False)
    items = OrderItemSerializer(many=True)

class SellerOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for listing Seller Orders.
    """
    class Meta:
        model = Order
        fields = ['id', 'order_id', 'order_status']

class SellerOrderDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed Seller Order information, including order items.
    """
    items = OrderItemSerializer(many=True, source='orderitem_set')

    class Meta:
        model = Order
        fields = '__all__'

class CartOrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an order from a user's cart.
    """
    class Meta:
        model = Order
        fields = ['shipping_address', 'payment_method', 'order_notes']
