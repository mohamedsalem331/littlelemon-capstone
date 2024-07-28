from functools import reduce
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    RetrieveDestroyAPIView,
)
from django.views.generic.edit import FormView
from rest_framework.response import Response
from .models import Category, MenuItem, Cart, Order, OrderItem, Booking, Menu
from .serializers import (
    BookingSerializer,
    MenuSerializer,
    MenuItemSerializer,
    UserCartSerializer,
    UserSerializer,
    UserOrdersSerializer,
)
from .forms import BookingForm
from django.contrib.auth.models import User, Group
from rest_framework.exceptions import NotFound


class HomeHTMLView(APIView):
    def get(self, request, *args, **kwargs):
        menu_data = Menu.objects.all()
        return render(request, "index.html", {"menu": menu_data})


class AboutHTMLView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "about.html", {})


class MenuHTMLView(APIView):
    def get(self, request, *args, **kwargs):
        menu_data = Menu.objects.all()
        print(menu_data[0])
        return render(request, "menu.html", {"menu": menu_data})


class SingleMenuView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk:
            menu_items_data = MenuItem.objects.filter(menu_id=pk)

        return render(request, "menu_item.html", {"menu_items": menu_items_data})


class BookForm(FormView):
    template_name = "book.html"
    form_class = BookingForm
    success_url = "/"  # or any URL you want to redirect to after a successful booking

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


"""
apis
"""


class menu(ListAPIView, ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MenuItemView(ListAPIView, ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ["price"]
    search_fields = ["title"]


class SingleItemView(RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class ManagerUsersView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        manager_group = Group.objects.get(name="manager")
        if manager_group:
            return User.objects.filter(groups=manager_group)
        else:
            raise NotFound("Manager group not found")


class DeliveryCrewView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        delivery_group = Group.objects.get(name="delivery crew")
        if delivery_group:
            return User.objects.filter(groups=delivery_group)
        else:
            raise NotFound("DeliveryCrew group not found")


class UserCartView(ListCreateAPIView):
    serializer_class = UserCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    def perform_create(self, serializer):
        order_id = self.request.data.get("order")
        order = Order.objects.get(id=order_id)
        serializer.save(user=self.request.user, order=order)

    def delete(self, request):
        user = self.request.user
        Cart.objects.filter(user=user).delete()
        return Response(status=204)


class Orders_view(ListCreateAPIView):
    serializer_class = UserOrdersSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart_items = Cart.objects.filter(user=self.request.user)
        total = self.calculate_total(cart_items)
        order = serializer.save(user=self.request.user, total=total)

        for cart_item in cart_items:
            OrderItem.objects.create(
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price,
                order=order,
            )
            cart_item.delete()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="manager").exists():
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def calculate_total(self, cart_items):
        return reduce(lambda x, y: x + y, cart_items, 0)


class BookView(ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
