from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
)
from django.views.generic.edit import FormView
from rest_framework.response import Response
from .models import Category, MenuItem, Cart, Order, OrderItem, Booking, Menu
from .serializers import (
    BookingSerializer,
    MenuSerializer,
    MenuItemSerializer,
    UserCartSerializer,
)
from .forms import BookingForm


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


class UserCartView(ListCreateAPIView):
    serializer_class = UserCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    # def perform_create(self, serializer):
    #     order = self.request.data.get("order")
    #     print("order", order)
    #     # menuitem = self.request.data.get("menuitem")
    #     # quantity = self.request.data.get("quantity")
    #     # unit_price = MenuItem.objects.get(pk=menuitem).price
    #     # quantity = int(quantity)
    #     # price = quantity * unit_price
    #     # serializer.save(user=self.request.user, price=price)


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
