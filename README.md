# Prova E-Commerce (2021)

## Overview

This Django project focuses on creating a comprehensive e-commerce platform, incorporating features for user authentication, cart management, order checkout, and product catalog. The project also implements user profile management, including features such as user details, product reviews, and images.

## Features

### User Profile Management

- **User:**
  - First name, last name, email, mobile, address, and other user details.
  - Profile-related metrics: followers, visitors, size_image, height, cup_size, etc.
  - User management functionalities, including superuser creation.

- **Category:**
  - Defines product categories with title, gender specificity, and description.

### Cart Management

- **Cart:**
  - Manages user shopping carts with total, shipping charge, grand total, promo codes, and item counts.
  - Associated with a user profile.

- **CartItem:**
  - Represents items within a shopping cart, including size, color, quantity, title, photo, and price.
  - Linked to the Cart model.

### Order Checkout

- **CheckedCart:**
  - Handles checked-out carts with total, shipping charge, grand total, selling date, and user association.

- **CheckedCartItem:**
  - Represents items within a checked-out cart, similar to CartItem.
  - Linked to CheckedCart and Product models.

### Product Catalog

- **Product:**
  - Describes individual products with title, details, price, discount, brand, and other attributes.
  - Categorized with Category model, associated with vendors and available sizes/colors.
  - Manages product reviews, images, and quantity.

### Additional Models

- **Size:**
  - Represents size options for products.

- **Color:**
  - Represents color options for products.

- **Quantity:**
  - Manages product quantities based on size and color.
  - Includes an alarm for quantity shortage.

- **Review:**
  - Stores product reviews with ratings, content, date, and user association.

- **Image:**
  - Handles product images associated with the Image model.


## Project Structure
The project is organized into the following directory structure:

```sh
└── prova/
    ├── .env.example
    ├── app
    │   ├── app
    │   │   ├── asgi.py
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   └── wsgi.py
    │   ├── e_commerce
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── filter.py
    │   │   ├── management
    │   │   ├── migrations
    │   │   ├── models.py
    │   │   ├── permissions.py
    │   │   ├── serializers.py
    │   │   ├── tests.py
    │   │   ├── urls.py
    │   │   └── views.py
    │   └── manage.py
    ├── docker-compose-deploy.yml
    ├── docker-compose.yml
    ├── Dockerfile
    ├── proxy
    │   ├── default.conf.tpl
    │   ├── Dockerfile
    │   ├── run.sh
    │   └── uwsgi_params
    ├── requirements.txt
    └── scripts
        └── run.sh
```
