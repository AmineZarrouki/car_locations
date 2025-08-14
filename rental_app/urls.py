from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView, UserLoginView, UserProfileView, 
    AdminUserViewSet, CarViewSet, RentalViewSet
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


