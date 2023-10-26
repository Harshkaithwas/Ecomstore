# Ecomstore : JWT auth and the store has functionality to perform operation for both the sides Consumer as well as Seller

Description: "Ecomstore" is a web application that serves as an e-commerce platform, providing features for both consumers and sellers. The application is built using JWT (JSON Web Tokens) authentication for secure and efficient user management. Let's break down the description in detail:


**JWT Authentication**: JWT, or JSON Web Tokens, is a widely used and secure method of authentication and authorization for web applications. In the context of Ecomstore, JWT is employed to ensure that users (both consumers and sellers) can securely log in, access their accounts, and perform actions within the platform.

**Consumer**: In the context of an e-commerce platform like Ecomstore, a "consumer" typically refers to a customer or end user of the platform. Consumers visit the website or app to browse products, make purchases, and interact with the services offered. They use JWT authentication to create and manage their accounts, track orders.
**Seller**: A "seller" in the context of Ecomstore is an entity or individual who registers as a vendor on the platform to list and manage products for sale. Sellers utilize JWT authentication to create and manage their seller accounts, upload product listings, set prices, and manage their orders and inventory.

**Functionality for Both Sides**: Ecomstore is designed to cater to both consumers and sellers, offering a range of features and functionalities:

**For Consumers**:

1. **User Registration and Authentication**: Consumers can create accounts securely using JWT. They can log in and log out of their accounts and reset their passwords.

2. **Browsing and Searching**: Consumers can search for products, view product details, and browse categories to find items they are interested in.

3. **Adding to Cart and Checkout**: Consumers can add products to their shopping carts, proceed to checkout, and make purchases.

4. **Order Management**: Consumers can track their orders, view order history, and manage their delivery addresses.

**For Sellers**:

1. **Seller Registration and Authentication**: Sellers can register as vendors using JWT authentication, create and manage their seller profiles, and access their seller dashboards.

2. **Product Management**: Sellers can add, edit, and delete product listings. They can set product descriptions, prices, and inventory levels.

3. **Order Fulfillment**: Sellers can view and manage orders, confirm shipments, and update order statuses.

4. **Inventory Management**: Sellers can track their inventory, receive notifications for low stock, and manage product availability.

Ecomstore is a comprehensive e-commerce platform that accommodates both consumers and sellers, providing JWT authentication for secure and efficient user management. It offers a wide range of features and functionalities tailored to the needs of these two user groups, enhancing the shopping and selling experience for all parties involved.


# How to use this project a step by step guide.

1. There are two was to use this project:

a. Online hosted project is availability is on : https://harshestore.pythonanywhere.com/  
        
        Admin login details: email: a@a.com && password: 261121

        
        Step1. Go to the given link and you will see all the routs.
        step2. Use Postman for performing all the actions.
        Step3. Create an account:
                                fields:{
                                        email:
                                        password:
                                        password2:
                                        role: Choose the role between Customer and Seller.
                                }

        step4. verify your account with otp You will get on your email.
        step5. Login 
        Step6. Now you are readt to use this project as the role u previously choosed.


b. For using this project on your machine.
                
        Step1. Download this project to your local machine.
        Step2. Create virtual environment.
        Step3. Goto project directory and find requirements.txt and install all the requirements on your active virtual environment.
        Step4. Setup the databse at your machine and configure it with settings.py file.


now you are ready to go with this project now open your terminal and follow the following steps to use this project.

1st : Run command
        
        python manage.py makemigrations

2nd : Next we need to migrate our project

        python manage.py migrate

3rd : You are all set to go with this project.
        
        python manage.py runserver

Note: Please create a super user to access the admin pannel: by using command 

        python manage.py createsuperuser

and follow the instructions on terminal.



Features for Consumers (Customer Role):

        User registration and authentication
        Browsing, searching, and product discovery
        Shopping cart management and checkout
        Order tracking and history
        User profile customization
        Wish lists and product reviews
        Personalized recommendations

Features for Sellers:

        Seller registration and authentication
        Product management, including adding, editing, and deleting listings
        Order fulfillment, shipment confirmation, and order status updates
        Inventory management with low stock notifications
        Access to data and analytics related to sales and customer behavior
        Communication with customers regarding products, shipping, and order-related inquiries
        Payment processing and seller payouts
        This comprehensive e-commerce platform empowers both consumers and sellers, ensuring a seamless shopping and selling experience. With JWT authentication, robust user management, and a rich set of features, Ecomstore stands ready to serve your e-commerce needs.

URL Routes: Here are the URL routes for user management and product-related functionalities in the project:

User Management:

        /sign_up/: User registration
        
        /otp_verification/: OTP (One-Time Password) verification
        
        /resend_otp/: Resend OTP for verification
        
        /sign_in/: User login
        
        /sign_out/: User logout
        
        /user/<int:pk>/: View user details
        
        /profile/: Access account profile
        
        /submit_kyc/: Submit KYC (Know Your Customer) information
        
        /change_password/: Change user password
        
        /reset_password/: Request a password reset
        
        /reset_password/<str:uidb64>/<str:token>/: Confirm password reset


Product Management:

        /categories/: List and create categories

        /products/: List seller's products
        
        /products/<int:pk>/: Retrieve, update, or delete a specific product
        
        /product/: List all products
        
        /product/<int:pk>/: Retrieve details of a specific product
        
        /cart/: Retrieve the user's cart
        
        /cart/add/: Add items to the cart
        
        /cart/clear/: Clear all items from the cart
        
        /cart/item/delete/<int:product_id>/: Delete a specific cart item
        
        /cart/item/update/<int:product_id>/: Update the quantity of a cart item
        
        /orders/: List user's orders
        
        /orders/<int:pk>/: Retrieve or delete a specific order
        
        /create_orders/: Create a new order
        
        /orders/cancel/<int:order_id>/: Cancel an order
        
        /seller/orders/: List all orders (for sellers)
        
        /seller/orders/<int:pk>/: Retrieve or update a specific order (for sellers)
