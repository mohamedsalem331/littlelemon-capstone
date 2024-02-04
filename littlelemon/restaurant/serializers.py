from rest_framework import serializers
from django.contrib.auth.models import User, Group

from .models import Menu, Booking

class MenuSerializer(serializers.ModelSerializer):
    class Meta():
        model = Menu
        fields =  '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta():
        model = Booking
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'