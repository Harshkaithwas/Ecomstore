# from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
# from products.models import *
# from products.serializers import *
# from rest_framework import status
# from rest_framework.response import Response
# import random
# from datetime import datetime, timedelta
# from rest_framework.exceptions import NotFound
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework import permissions

# class IsSeller(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.is_authenticated and request.user.role == 'seller'


# class CategoryListView(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAuthenticated, IsSeller]  # Authentication required to create categories.


# class SellerProductListView(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAuthenticated, IsSeller]

#     def get_queryset(self):
#         # Filter products for the authenticated user (assuming the user is the seller).
#         return Product.objects.filter(seller=self.request.user)

#     def perform_create(self, serializer):
#         data = serializer.validated_data
#         required_fields = ['name', 'description', 'price', 'category', 'image', 'manufacturer', 'stock']

#         missing_fields = [field for field in required_fields if field not in data]
#         if missing_fields:
#             return Response(
#                 {'error': f'The following fields are required: {", ".join(missing_fields)}'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Set the seller to the authenticated user.
#         data['seller'] = self.request.user
#         product = Product.objects.create(**data)
#         serializer = ProductSerializer(product)  # Create a serializer for the saved product.

#         return Response({'id': product.id, **serializer.data}, status=status.HTTP_201_CREATED)




# class SellerProductDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductDetailSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read access to anyone, and write access to authenticated users.

#     # Override the perform_update method to handle updates.
#     def perform_update(self, serializer):
#         instance = serializer.save()
#         return instance

#     # Override the perform_destroy method to handle deletion.
#     def perform_destroy(self, instance):
#         instance.delete()

#     def update(self, request, *args, **kwargs):
#         try:
#             partial = kwargs.pop('partial', True)
#             instance = self.get_object()
#             serializer = self.get_serializer(instance, data=request.data, partial=partial)
#             if serializer.is_valid():
#                 self.perform_update(serializer)
#                 return Response({"detail": f"Product '{instance.name}' is updated successfully."})
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except NotFound:
#             return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def destroy(self, request, *args, **kwargs):
#         try:
#             instance = self.get_object()
#             product_name = instance.name
#             self.perform_destroy(instance)
#             return Response({"detail": f"Product is deleted successfully."})
#         except NotFound:
#             return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


# class ProductListView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductListSerializer


#     def get_queryset(self):
#         queryset = Product.objects.all()
#         category_id = self.request.query_params.get('category')
#         if category_id:
#             queryset = queryset.filter(category_id=category_id)
#         return queryset


# class ProductDetailView(generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductDetailSerializer






# class CartView(generics.RetrieveAPIView):
#     serializer_class = CartSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         user = self.request.user
#         try:
#             return Cart.objects.get(user=user)
#         except Cart.DoesNotExist:
#             return None

#     def retrieve(self, request, *args, **kwargs):
#         cart = self.get_object()
#         if cart is None:
#             return Response({'detail': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

#         # Serialize the cart with items
#         serializer = self.get_serializer(cart)
#         return Response(serializer.data)

#     def delete(self, request, *args, **kwargs):
#         cart = self.get_object()
#         if cart is None:
#             return Response({'detail': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

#         # Delete all items in the cart by clearing the products ManyToMany relationship
#         cart.products.clear()

#         return Response({'detail': 'All items in the cart have been deleted'}, status=status.HTTP_204_NO_CONTENT)




# class CartItemDeleteView(generics.DestroyAPIView):
#     serializer_class = CartItemDeleteSerializer
#     permission_classes = [IsAuthenticated]

#     def destroy(self, request, product_id, *args, **kwargs):
#         user = self.request.user
#         cart, _ = Cart.objects.get_or_create(user=user)
        
#         try:
#             # Try to get the specific cart item to delete
#             cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
#             cart_item.delete()
#             return Response({'detail': 'Item removed from the cart'}, status=status.HTTP_204_NO_CONTENT)
#         except CartItem.DoesNotExist:
#             return Response({'detail': 'Item not found in the cart'}, status=status.HTTP_404_NOT_FOUND)





# class ClearCartView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = self.request.user
#         cart, _ = Cart.objects.get_or_create(user=user)

#         # Clear all items from the cart
#         cart.cartitem_set.all().delete()  # Use the correct related name

#         return Response({'detail': 'Cart cleared successfully'}, status=status.HTTP_200_OK)


# class CartItemUpdateView(generics.UpdateAPIView):
#     serializer_class = CartItemUpdateSerializer
#     permission_classes = [IsAuthenticated]

#     def update(self, request, product_id, *args, **kwargs):
#         user = self.request.user
#         # cart, _ = Cart.objects.get_or create(user=user)
#         cart, _ = Cart.objects.get_or_create(user=user)

#         cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

#         if not cart_item:
#             return Response({'detail': 'Item not found in the cart'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = self.get_serializer(cart_item, data=request.data, context={'cart_item': cart_item})
#         serializer.is_valid(raise_exception=True)
#         cart_item.quantity = serializer.validated_data['quantity']
#         cart_item.save()

#         # Update corresponding order items for this cart item
#         self.update_order_items(cart_item)

#         return Response({'detail': 'Item quantity updated'}, status=status.HTTP_200_OK)

#     def update_order_items(self, cart_item):
#         # Find and update the corresponding order items
#         order_items = cart_item.product.orderitem_set.all()
#         for order_item in order_items:
#             order_item.quantity = cart_item.quantity
#             order_item.save()


            
# class CartItemAddView(generics.CreateAPIView):
#     serializer_class = CartItemAddSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         product_id = serializer.validated_data['product_id']
#         quantity = serializer.validated_data['quantity']

#         try:
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return Response({'detail': 'Product not found'}, status=status.HTTP_NOT_FOUND)

#         user = self.request.user
#         cart, created = Cart.objects.get_or_create(user=user)
#         cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

#         # If the cart item already exists, add to the quantity instead of replacing it.
#         if not created:
#             cart_item.quantity += quantity
#             cart_item.save()
#         else:
#             cart_item.quantity = quantity
#             cart_item.save()

#         return Response({'detail': 'Item added to the cart'}, status=status.HTTP_201_CREATED)





# class OrderListView(generics.ListAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderListSerializer  # Use the new serializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return Order.objects.filter(user=user)

#     def list(self, request, *args, **kwargs):
#         try:
#             queryset = self.get_queryset()
#             serializer = self.get_serializer(queryset, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response(
#                 {"error": f"An error occurred: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#     def get(self, request, *args, **kwargs):
#         try:
#             return self.list(request, *args, **kwargs)
#         except Exception as e:
#             return Response(
#                 {"error": f"An error occurred: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )



# # views.py

# class OrderDetailView(generics.RetrieveDestroyAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderDetailSerializer
#     permission_classes = [IsAuthenticated]

#     def retrieve(self, request, *args, **kwargs):
#         try:
#             order = self.get_object()
#             if order.user != request.user:
#                 return Response(
#                     {"error": "You don't have permission to access this order."},
#                     status=status.HTTP_403_FORBIDDEN
#                 )
#             serializer = self.get_serializer(order)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Http404:
#             return Response(
#                 {"error": "Order not found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#     def destroy(self, request, *args, **kwargs):
#         try:
#             order = self.get_object()
#             if order.user != request.user:
#                 return Response(
#                     {"error": "You don't have permission to delete this order."},
#                     status=status.HTTP_403_FORBIDDEN
#                 )
#             order.delete()
#             return Response(
#                 {"message": "Order deleted successfully."},
#                 status=status.HTTP_204_NO_CONTENT
#             )
#         except Http404:
#             return Response(
#                 {"error": "Order not found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )



# class OrderCancellationView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, order_id):
#         try:
#             order = Order.objects.get(id=order_id)
            
#             # Check if the user is allowed to cancel the order (e.g., order owner)
#             if order.user == self.request.user:
#                 # Update the order status to "Canceled" (you may need to define this status)
#                 order.order_status = "Canceled by User"
#                 order.save()
                
#                 return Response({'detail': 'Order successfully canceled'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'detail': 'You are not authorized to cancel this order'}, status=status.HTTP_403_FORBIDDEN)
#         except Order.DoesNotExist:
#             return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)






# from datetime import datetime, timedelta
# import random
# from rest_framework import generics, status
# from rest_framework.response import Response
# from .models import Cart, Order, OrderItem, Product
# from .serializers import OrderCreateSerializer

# class OrderCreateView(generics.CreateAPIView):
#     serializer_class = OrderCreateSerializer

#     def create(self, request, *args, **kwargs):
#         try:
#             user = request.user
#             cart = Cart.objects.get(user=user)

#             # Check if the cart is empty
#             if not cart.cartitem_set.exists():
#                 return Response({'error': 'Cart is empty. Add some items to the cart before creating an order.'}, status=status.HTTP_400_BAD_REQUEST)

#             # Extract cart items
#             cart_items = cart.cartitem_set.all()
#             total_price = sum(item.product.price * item.quantity for item in cart_items)

#             # Generate a random 12-digit order ID and a random delivery date
#             order_id = f'OID{random.randint(10**11, 10**12 - 1)}'
#             current_date = datetime.now()
#             delivery_date = current_date + timedelta(days=random.randint(5, 15))

#             # Create the order
#             order = Order.objects.create(
#                 user=user,
#                 order_id=order_id,
#                 delivery_date=delivery_date,
#                 total_price=total_price,
#                 shipping_address=request.data.get('shipping_address'),
#                 payment_method=request.data.get('payment_method'),
#                 order_notes=request.data.get('order_notes')
#             )

#             # Create order items and update product stock
#             for cart_item in cart_items:
#                 product = cart_item.product
#                 quantity = cart_item.quantity
#                 OrderItem.objects.create(order=order, product=product, quantity=quantity)

#                 # Subtract the ordered quantity from the product's stock
#                 product.stock -= quantity
#                 product.save()

#             # Clear the user's cart after creating the order
#             cart_items.delete()

#             return Response(
#                 {
#                     "order_id": order_id,
#                     "message": "Order created successfully",
#                 },
#                 status=status.HTTP_201_CREATED
#             )
#         except Exception as e:
#             return Response(
#                 {"error": f"An error occurred: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )






# class SellerOrderListView(generics.ListAPIView, generics.UpdateAPIView):
#     serializer_class = SellerOrderSerializer
#     permission_classes = [IsAuthenticated, IsSeller]

#     def get_queryset(self):
#     # If the authenticated user is a seller, return all orders
#         if self.request.user.role == 'seller':
#             queryset = Order.objects.all()
#         else:
#             # For non-seller users, return only their own orders
#             queryset = Order.objects.filter(user=self.request.user)
#         return queryset




# class SellerOrderDetailView(generics.RetrieveUpdateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = SellerOrderDetailSerializer
#     permission_classes = [IsAuthenticated, IsSeller]

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def update(self, request, *args, **kwargs):
#         # Update order status as before
#         order = self.get_object()
#         order_status = request.data.get('order_status')

#         if order_status not in ['Pending', 'Rejected', 'Confirmed', 'Ready to Ship', 'Dispatch', 'Shipped', 'Out for Delivery', 'Delivered']:
#             return Response(
#                 {"error": "Invalid order_status provided"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         order.order_status = order_status
#         order.save()

#         # Create a new serializer instance to include item details
#         serializer = SellerOrderDetailSerializer(order)
        
#         return Response(serializer.data, status=status.HTTP_200_OK)







from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView,
    CreateAPIView, UpdateAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, DestroyAPIView
)
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from products.models import (
    Category, Product, Cart, CartItem, Order, OrderItem
)
from products.serializers import (
    CategorySerializer, ProductSerializer, ProductDetailSerializer, ProductListSerializer,
    CartSerializer, CartItemDeleteSerializer, CartItemUpdateSerializer,
    CartItemAddSerializer, OrderCreateSerializer, OrderListSerializer, OrderDetailSerializer,
    SellerOrderSerializer, SellerOrderDetailSerializer,
)
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework import permissions
from django.http import Http404
from datetime import datetime, timedelta
import random

# Custom Permission Class for Sellers
class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'seller'


class CategoryListView(ListCreateAPIView):
    """
    List and create categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsSeller]


class SellerProductListView(ListCreateAPIView):
    """
    List and create products for the authenticated user (assumed to be a seller).
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def get_queryset(self):
        # Filter products for the authenticated user (assuming the user is the seller).
        return Product.objects.filter(seller=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new product, ensuring required fields are provided.
        """
        data = serializer.validated_data
        required_fields = ['name', 'description', 'price', 'category', 'image', 'manufacturer', 'stock']

        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return Response(
                {'error': f'The following fields are required: {", ".join(missing_fields)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Set the seller to the authenticated user.
        data['seller'] = self.request.user
        product = Product.objects.create(**data)
        serializer = ProductSerializer(product)  # Create a serializer for the saved product.

        return Response({'id': product.id, **serializer.data}, status=status.HTTP_201_CREATED)


class SellerProductDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        """
        Handle updates for a product.
        """
        instance = serializer.save()
        return instance

    def perform_destroy(self, instance):
        """
        Handle deletion of a product.
        """
        instance.delete()

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', True)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response({"detail": f"Product '{instance.name}' is updated successfully."})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except NotFound:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            product_name = instance.name
            self.perform_destroy(instance)
            return Response({"detail": f"Product is deleted successfully."})
        except NotFound:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductListView(ListAPIView):
    """
    List products with optional filtering by category.
    """
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class ProductDetailView(RetrieveAPIView):
    """
    Retrieve details of a product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class CartView(RetrieveAPIView):
    """
    Retrieve the user's cart with items.
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            return Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        cart = self.get_object()
        if cart is None:
            return Response({'detail': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the cart with items
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        cart = self.get_object()
        if cart is None:
            return Response({'detail': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        # Delete all items in the cart by clearing the products ManyToMany relationship
        cart.products.clear()

        return Response({'detail': 'All items in the cart have been deleted'}, status=status.HTTP_204_NO_CONTENT)


class CartItemDeleteView(DestroyAPIView):
    """
    Delete a specific item from the cart.
    """
    serializer_class = CartItemDeleteSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, product_id, *args, **kwargs):
        user = self.request.user
        cart, _ = Cart.objects.get_or_create(user=user)

        try:
            # Try to get the specific cart item to delete
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            return Response({'detail': 'Item removed from the cart'}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'detail': 'Item not found in the cart'}, status=status.HTTP_404_NOT_FOUND)


class ClearCartView(APIView):
    """
    Clear all items from the user's cart.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        cart, _ = Cart.objects.get_or_create(user=user)

        # Clear all items from the cart
        cart.cartitem_set.all().delete()  # Use the correct related name

        return Response({'detail': 'Cart cleared successfully'}, status=status.HTTP_200_OK)


class CartItemUpdateView(UpdateAPIView):
    """
    Update the quantity of a specific item in the cart.
    """
    serializer_class = CartItemUpdateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, product_id, *args, **kwargs):
        user = self.request.user
        cart, _ = Cart.objects.get_or_create(user=user)

        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

        if not cart_item:
            return Response({'detail': 'Item not found in the cart'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(cart_item, data=request.data, context={'cart_item': cart_item})
        serializer.is_valid(raise_exception=True)
        cart_item.quantity = serializer.validated_data['quantity']
        cart_item.save()

        # Update corresponding order items for this cart item
        self.update_order_items(cart_item)

        return Response({'detail': 'Item quantity updated'}, status=status.HTTP_200_OK)

    def update_order_items(self, cart_item):
        # Find and update the corresponding order items
        order_items = cart_item.product.orderitem_set.all()
        for order_item in order_items:
            order_item.quantity = cart_item.quantity
            order_item.save()


class CartItemAddView(CreateAPIView):
    """
    Add an item to the cart or update its quantity.
    """
    serializer_class = CartItemAddSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_NOT_FOUND)

        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        # If the cart item already exists, add to the quantity instead of replacing it.
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        return Response({'detail': 'Item added to the cart'}, status=status.HTTP_201_CREATED)


class OrderCreateView(CreateAPIView):
    """
    Create an order and update product stock.
    """
    serializer_class = OrderCreateSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            cart = Cart.objects.get(user=user)

            # Check if the cart is empty
            if not cart.cartitem_set.exists():
                return Response({'error': 'Cart is empty. Add some items to the cart before creating an order.'}, status=status.HTTP_400_BAD_REQUEST)

            # Extract cart items
            cart_items = cart.cartitem_set.all()
            total_price = sum(item.product.price * item.quantity for item in cart_items)

            # Generate a random 12-digit order ID and a random delivery date
            order_id = f'OID{random.randint(10**11, 10**12 - 1)}'
            current_date = datetime.now()
            delivery_date = current_date + timedelta(days=random.randint(5, 15))

            # Create the order
            order = Order.objects.create(
                user=user,
                order_id=order_id,
                delivery_date=delivery_date,
                total_price=total_price,
                shipping_address=request.data.get('shipping_address'),
                payment_method=request.data.get('payment_method'),
                order_notes=request.data.get('order_notes')
            )

            # Create order items and update product stock
            for cart_item in cart_items:
                product = cart_item.product
                quantity = cart_item.quantity
                OrderItem.objects.create(order=order, product=product, quantity=quantity)

                # Subtract the ordered quantity from the product's stock
                product.stock -= quantity
                product.save()

            # Clear the user's cart after creating the order
            cart_items.delete()

            return Response(
                {
                    "order_id": order_id,
                    "message": "Order created successfully",
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SellerOrderListView(ListAPIView, UpdateAPIView):
    """
    List and update orders for sellers.
    """
    serializer_class = SellerOrderSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def get_queryset(self):
        # If the authenticated user is a seller, return all orders
        if self.request.user.role == 'seller':
            queryset = Order.objects.all()
        else:
            # For non-seller users, return only their own orders
            queryset = Order.objects.filter(user=self.request.user)
        return queryset


class SellerOrderDetailView(RetrieveUpdateAPIView):
    """
    Retrieve and update order details for sellers.
    """
    queryset = Order.objects.all()
    serializer_class = SellerOrderDetailSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Update order status as before
        order = self.get_object()
        order_status = request.data.get('order_status')

        if order_status not in ['Pending', 'Rejected', 'Confirmed', 'Ready to Ship', 'Dispatch', 'Shipped', 'Out for Delivery', 'Delivered']:
            return Response(
                {"error": "Invalid order_status provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.order_status = order_status
        order.save()

        # Create a new serializer instance to include item details
        serializer = SellerOrderDetailSerializer(order)

        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderListView(ListAPIView):
    """
    List orders for the authenticated user.
    """
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderDetailView(RetrieveDestroyAPIView):
    """
    Retrieve and delete an order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            order = self.get_object()
            if order.user != request.user:
                return Response(
                    {"error": "You don't have permission to access this order."},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response(
                {"error": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, *args, **kwargs):
        try:
            order = self.get_object()
            if order.user != request.user:
                return Response(
                    {"error": "You don't have permission to delete this order."},
                    status=status.HTTP_403_FORBIDDEN
                )
            order.delete()
            return Response(
                {"message": "Order deleted successfully."},
                status=status.HTTP_204_NO_CONTENT
            )
        except Http404:
            return Response(
                {"error": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )


class OrderCancellationView(APIView):
    """
    Cancel an order.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)

            # Check if the user is allowed to cancel the order (e.g., order owner)
            if order.user == self.request.user:
                # Update the order status to "Canceled" (you may need to define this status)
                order.order_status = "Canceled by User"
                order.save()

                return Response({'detail': 'Order successfully canceled'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'You are not authorized to cancel this order'}, status=status.HTTP_403_FORBIDDEN)
        except Order.DoesNotExist:
            return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
