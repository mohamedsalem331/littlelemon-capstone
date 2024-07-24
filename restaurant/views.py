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
)
from .forms import BookingForm
from django.contrib.auth.models import User, Group
from rest_framework.exceptions import NotFound


class home(APIView):
    def get(self, request, *args, **kwargs):
        menu_data = Menu.objects.all()
        return render(request, "index.html", {"menu": menu_data})


class about(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "about.html", {})


# class single_menu_item(RetrieveUpdateDestroyAPIView):
# def get(self, request, *args, **kwargs):
#     pk = kwargs.get("pk")
#     item = ""
#     if pk:
#         item = get_object_or_404(MenuItem, pk=pk)

#     return render(request, "menu_item.html", {"menu_item": item})


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


class BookForm(FormView):
    template_name = "book.html"
    form_class = BookingForm
    success_url = "/"  # or any URL you want to redirect to after a successful booking

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class BookView(ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
