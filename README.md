## 1. Project Overview

This document provides a comprehensive technical overview of the Django Car Rental Project, a robust and scalable application designed to manage car rentals. The project is built with a focus on a clean separation of concerns, leveraging a RESTful API for backend logic and a set of traditional Django template views for direct user interaction. This dual-interface approach ensures that the application is both developer-friendly for API integrations and user-friendly for direct management.

### 1.1. Core Functionalities

-   **User and Admin Management**: Secure registration, authentication, and profile management for both regular users and administrators with distinct permission levels.
-   **Car Inventory Management**: Comprehensive CRUD (Create, Retrieve, Update, Delete) operations for car listings, including details such as make, model, year, and availability.
-   **Rental Transaction Management**: End-to-end rental process management, from booking and status tracking to cancellation and completion.

### 1.2. Architectural Design

The project follows a **Model-View-Controller (MVC)**-like architecture, which is standard for Django applications. However, with the inclusion of Django REST Framework (DRF), the architecture can be more accurately described as **Model-View-ViewModel (MVVM)** or **Model-View-Serializer (MVS)** for the API part.

-   **Models**: The data layer is defined in `rental_app/models.py`, where each model corresponds to a database table. This layer is the single source of truth for the application's data structure.
-   **Views (API)**: The API views, located in `rental_app/views.py`, handle the business logic for processing API requests. They leverage DRF's `ModelViewSet` and generic views to provide a standardized and efficient way to handle CRUD operations.
-   **Serializers**: The serializers in `rental_app/serializers.py` are responsible for converting complex data types, such as Django model instances, into native Python datatypes that can then be easily rendered into JSON for API responses. They also handle data validation for incoming API requests.
-   **Views (Templates)**: The template-based views, also in `rental_app/views.py`, use Django's generic class-based views (`ListView`, `CreateView`, `UpdateView`, `DeleteView`) to render HTML templates and handle form submissions for direct user interaction.
-   **Templates**: The HTML templates in `rental_app/templates/` define the user interface for the template-based views.
-   **URLs**: The URL configuration in `car_rental_project/urls.py` and `rental_app/urls.py` maps URLs to their corresponding views, directing traffic to the appropriate API or template view.

This architecture ensures that the API and template views are decoupled, allowing for independent development and maintenance. The business logic is primarily encapsulated within the views and models, promoting code reusability and a clear separation of concerns.


## 3. Setup and Running the Project

To get the Car Rental Django project running on your local machine, follow these steps:

### 3.1. Prerequisites

Ensure you have the following installed on your system:

-   **Python 3.8+**: Download from the official Python website.
-   **pip**: Python's package installer, usually included with Python installations.

### 3.2. Installation
1.  **Install Dependencies:**
    With your virtual environment active, install the necessary Python packages:

    ```bash
    pip install django djangorestframework
    ```

2.  **Apply Database Migrations:**
    The project uses SQLite by default. Apply the migrations to create the database schema:

    ```bash
    python manage.py makemigrations rental_app
    python manage.py migrate
    ```

3.  **Create a Superuser:**
    Create an administrative user to access the Django admin panel. Follow the prompts to set a username, email, and password.

    ```bash
    python manage.py createsuperuser
    ```

### 3.3. Running the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The server will typically be accessible at `http://127.0.0.1:8000/`.

## 4. Usage

### 4.1. Accessing the Django Admin Panel

Navigate to `http://127.0.0.1:8000/admin/` in your web browser. Log in with the superuser credentials you created. From here, you can manage all the data related to Users, Admins, Cars, and Rentals.

### 4.2. Using the API Endpoints

The RESTful API endpoints are available under the `/api/` path. You can interact with these endpoints using tools like Postman, Insomnia, or `curl`.

-   **Example: Retrieve all cars**
    `GET http://127.0.0.1:8000/api/cars/`

### 4.3. Using the Template-based CRUD Views

The project also provides traditional web pages for CRUD operations. You can access them directly from the root URL:

-   **Users Management**: `http://127.0.0.1:8000/users/`
-   **Cars Management**: `http://127.0.0.1:8000/cars/`
-   **Admins Management**: `http://127.0.0.1:8000/admins/`
-   **Rentals Management**: `http://127.0.0.1:8000/rentals/`

These pages allow you to create, view, edit, and delete records through a user-friendly web interface.

## 5. Project Structure

```
car_rental_project/
├── car_rental_project/       # Main Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── rental_app/               # Django application for car rental logic
│   ├── migrations/           # Database migrations
│   ├── __init__.py
│   ├── admin.py              # Admin panel configuration
│   ├── apps.py               # App configuration
│   ├── models.py             # Database models (User, Admin, Car, Rental)
│   ├── serializers.py        # DRF serializers for API
│   ├── views.py              # DRF API views and Django template views
│   ├── urls.py               # URL routing for API and template views
│   ├── forms.py              # Django forms for template views
│   └── templates/            # HTML templates for CRUD views
│       └── rental_app/
│           ├── base.html
│           ├── user_list.html
│           ├── user_form.html
│           ├── user_confirm_delete.html
│           ├── car_list.html
│           ├── car_form.html
│           ├── car_confirm_delete.html
│           ├── admin_list.html
│           ├── admin_form.html
│           ├── admin_confirm_delete.html
│           ├── rental_list.html
│           ├── rental_form.html
│           └── rental_confirm_delete.html
├── manage.py                 # Django's command-line utility
└── db.sqlite3                # Default SQLite database file
```



