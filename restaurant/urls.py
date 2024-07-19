from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("menu/", views.menu, name="menu"),
    path("menu_item/<int:pk>/", views.single_menu_item, name="menu_item"),
    path("book/", views.book, name="book"),
    path("api-token-auth/", obtain_auth_token),
]
