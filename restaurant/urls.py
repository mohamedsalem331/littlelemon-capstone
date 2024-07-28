from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import include, path
from .views import (
    HomeHTMLView,
    AboutHTMLView,
    MenuHTMLView,
    SingleMenuView,
    menu,
    MenuItemView,
    SingleItemView,
    UserCartView,
    BookView,
    BookForm,
    ManagerUsersView,
    DeliveryCrewView,
)

urlpatterns = [
    path("", HomeHTMLView.as_view(), name="home"),
    path("about/", AboutHTMLView.as_view(), name="about"),
    path("menu/", MenuHTMLView.as_view(), name="menu"),
    path("menus/", menu.as_view()),
    path("menu-items/<int:pk>/", SingleMenuView.as_view(), name="menu-items"),
    path("menu-items/", MenuItemView.as_view()),
    # path("menu-items/<int:pk>/", SingleItemView.as_view(), name="menu_item"),
    path("cart/menu-items/", UserCartView.as_view()),
    path("groups/manager/users/", ManagerUsersView.as_view()),
    path("groups/delivery-crew/users/", DeliveryCrewView.as_view()),
    path("bookings/", BookForm.as_view(), name="book"),
    path("book/", BookView.as_view(), name="book"),
    path("api-token-auth/", obtain_auth_token),
]
