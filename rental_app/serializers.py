from rest_framework import serializers
from .models import User, Admin, Car, Rental

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 
            'phone_number', 'address'
        )
        read_only_fields = ('id',)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'first_name', 'last_name', 
            'phone_number', 'address'
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            address=validated_data.get('address', '')
        )
        return user

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Admin
        fields = ('user', 'permissions')

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            'id', 'make', 'model', 'year', 'color', 'license_plate', 
            'daily_rate', 'availability_status'
        )
        read_only_fields = ('id',)

class RentalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    car = CarSerializer(read_only=True)

    class Meta:
        model = Rental
        fields = (
            'id', 'user', 'car', 'start_date', 'end_date', 
            'total_cost', 'status'
        )
        read_only_fields = ('id', 'total_cost')

class RentalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ('car', 'start_date', 'end_date')



