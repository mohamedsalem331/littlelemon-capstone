from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import include, path
from .views import (
    home,
    about,
    menu,
    MenuItemView,
    SingleItemView,
    UserCartView,
    BookView,
    BookForm,
)

urlpatterns = [
    path("", home.as_view(), name="home"),
    path("about/", about.as_view(), name="about"),
    path("menu/", menu.as_view(), name="menu"),
    path("menu-items/", MenuItemView.as_view()),
    path("menu_items/<int:pk>/", SingleItemView.as_view(), name="menu_item"),
    path("cart/menu-items/", UserCartView.as_view()),
    path("book/", BookForm.as_view(), name="book"),
    path("bookings/", BookView.as_view(), name="book"),
    path("api-token-auth/", obtain_auth_token),
]
