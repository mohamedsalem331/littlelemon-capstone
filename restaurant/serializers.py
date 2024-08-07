from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, MenuItem, Cart, Order, OrderItem, Booking, Menu
from datetime import datetime


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "_all_"


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    # Date_Joined = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(write_only=True, default=datetime.now)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined"]

    def get_date_joined(self, obj):
        return obj.date_joined.strftime("%Y-%m-%d")

    # def get_Date_Joined(self, obj):
    #     return obj.date_joined.strftime("%Y-%m-%d")


class UserCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = "__all__"


# class OrderItemSerializer(serializers.ModelSerializer):
#     unit_price = serializers.DecimalField(
#         max_digits=6, decimal_places=2, source="menuitem.price", read_only=True
#     )
#     name = serializers.CharField(source="menuitem.title", read_only=True)

#     class Meta:
#         model = OrderItem
#         fields = ["name", "quantity"]
#         extra_kwargs = {"menuitem": {"read_only": True}}


class UserOrdersSerializer(serializers.ModelSerializer):
    Date = serializers.SerializerMethodField()
    date = serializers.DateTimeField(write_only=True, default=datetime.now)
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "delivery_crew",
            "status",
            "total",
            "Date",
            "date",
            "order_items",
        ]
        extra_kwargs = {"total": {"read_only": True}}

    def get_Date(self, obj):
        return obj.date.strftime("%Y-%m-%d")

    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        serializer = OrderItemSerializer(
            order_items, many=True, context={"request": self.context["request"]}
        )
        return serializer


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
