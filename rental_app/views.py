from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

from .models import User, Admin, Car, Rental
from .serializers import (
    UserSerializer, UserRegistrationSerializer, AdminSerializer, 
    CarSerializer, RentalSerializer, RentalCreateSerializer
)

# User Management Views
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# Admin Management Views
class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

# Car Management Views
class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [] # Allow anyone to view cars
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        make = self.request.query_params.get("make")
        model = self.request.query_params.get("model")
        year = self.request.query_params.get("year")
        availability_status = self.request.query_params.get("availability_status")

        if make: queryset = queryset.filter(make__icontains=make)
        if model: queryset = queryset.filter(model__icontains=model)
        if year: queryset = queryset.filter(year=year)
        if availability_status: queryset = queryset.filter(availability_status__iexact=availability_status)
        return queryset

# Rental Management Views
class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["list", "retrieve"]:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return RentalCreateSerializer
        return RentalSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff: # Admin user
            return queryset
        return queryset.filter(user=self.request.user) # Regular user

    def cancel_rental(self, request, pk=None):
        rental = get_object_or_404(Rental, pk=pk, user=request.user)
        if rental.status == "pending":
            rental.status = "cancelled"
            rental.save()
            return Response({"detail": "Rental cancelled successfully."})
        return Response({"detail": "Rental cannot be cancelled."}, status=status.HTTP_400_BAD_REQUEST)
    def update_status(self, request, pk=None):
        if not request.user.is_staff:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        rental = get_object_or_404(Rental, pk=pk)
        new_status = request.data.get("status")
        if new_status:
            rental.status = new_status
            rental.save()
            return Response(RentalSerializer(rental).data)
        return Response({"detail": "Status not provided."}, status=status.HTTP_400_BAD_REQUEST)



from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import UserForm, CarForm, AdminForm, RentalForm

# Template Views for User
class UserListView(ListView):
    model = User
    template_name = 'rental_app/user_list.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'rental_app/user_form.html'
    success_url = reverse_lazy('user_list')

class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'rental_app/user_form.html'
    success_url = reverse_lazy('user_list')

class UserDeleteView(DeleteView):
    model = User
    template_name = 'rental_app/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

# Template Views for Car
class CarListView(ListView):
    model = Car
    template_name = 'rental_app/car_list.html'
    context_object_name = 'cars'

class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'rental_app/car_form.html'
    success_url = reverse_lazy('car_list')

class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'rental_app/car_form.html'
    success_url = reverse_lazy('car_list')

class CarDeleteView(DeleteView):
    model = Car
    template_name = 'rental_app/car_confirm_delete.html'
    success_url = reverse_lazy('car_list')

# Template Views for Admin
class AdminListView(ListView):
    model = Admin
    template_name = 'rental_app/admin_list.html'
    context_object_name = 'admins'

class AdminCreateView(CreateView):
    model = Admin
    form_class = AdminForm
    template_name = 'rental_app/admin_form.html'
    success_url = reverse_lazy('admin_list')

class AdminUpdateView(UpdateView):
    model = Admin
    form_class = AdminForm
    template_name = 'rental_app/admin_form.html'
    success_url = reverse_lazy('admin_list')

class AdminDeleteView(DeleteView):
    model = Admin
    template_name = 'rental_app/admin_confirm_delete.html'
    success_url = reverse_lazy('admin_list')

# Template Views for Rental
class RentalListView(ListView):
    model = Rental
    template_name = 'rental_app/rental_list.html'
    context_object_name = 'rentals'

class RentalCreateView(CreateView):
    model = Rental
    form_class = RentalForm
    template_name = 'rental_app/rental_form.html'
    success_url = reverse_lazy('rental_list')

class RentalUpdateView(UpdateView):
    model = Rental
    form_class = RentalForm
    template_name = 'rental_app/rental_form.html'
    success_url = reverse_lazy('rental_list')

class RentalDeleteView(DeleteView):
    model = Rental
    template_name = 'rental_app/rental_confirm_delete.html'
    success_url = reverse_lazy('rental_list')


