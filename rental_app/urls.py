from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView, UserLoginView, UserProfileView, 
    AdminUserViewSet, CarViewSet, RentalViewSet,
    UserListView, UserCreateView, UserUpdateView, UserDeleteView,
    CarListView, CarCreateView, CarUpdateView, CarDeleteView,
    AdminListView, AdminCreateView, AdminUpdateView, AdminDeleteView,
    RentalListView, RentalCreateView, RentalUpdateView, RentalDeleteView
)
router = DefaultRouter()
router.register(r"admin/users", AdminUserViewSet)
router.register(r"cars", CarViewSet)
router.register(r"rentals", RentalViewSet)

urlpatterns = [
    path("users/register/", UserRegistrationView.as_view(), name="user-register"),
    path("users/login/", UserLoginView.as_view(), name="user-login"),
    path("users/profile/", UserProfileView.as_view(), name="user-profile"),
    path("rentals/<int:pk>/cancel/", RentalViewSet.as_view({"put": "cancel_rental"}), name="rental-cancel"),
    path("admin/rentals/<int:pk>/status/", RentalViewSet.as_view({"put": "update_status"}), name="admin-rental-status-update"),
    path("", include(router.urls)),
]




# Template View URLs
urlpatterns += [
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/add/", UserCreateView.as_view(), name="user_create"),
    path("users/<int:pk>/edit/", UserUpdateView.as_view(), name="user_update"),
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),

    path("cars/", CarListView.as_view(), name="car_list"),
    path("cars/add/", CarCreateView.as_view(), name="car_create"),
    path("cars/<int:pk>/edit/", CarUpdateView.as_view(), name="car_update"),
    path("cars/<int:pk>/delete/", CarDeleteView.as_view(), name="car_delete"),

    path("admins/", AdminListView.as_view(), name="admin_list"),
    path("admins/add/", AdminCreateView.as_view(), name="admin_create"),
    path("admins/<int:pk>/edit/", AdminUpdateView.as_view(), name="admin_update"),
    path("admins/<int:pk>/delete/", AdminDeleteView.as_view(), name="admin_delete"),

    path("rentals/", RentalListView.as_view(), name="rental_list"),
    path("rentals/add/", RentalCreateView.as_view(), name="rental_create"),
    path("rentals/<int:pk>/edit/", RentalUpdateView.as_view(), name="rental_update"),
    path("rentals/<int:pk>/delete/", RentalDeleteView.as_view(), name="rental_delete"),
]