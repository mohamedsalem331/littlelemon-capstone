from django.contrib import admin
from django.db import router
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("restaurant.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]

"""
-djoser urls
POST /auth/users/ - create a new user
POST /auth/token/login/ - obtain a token
POST /auth/token/logout/ - logout
POST /auth/password/reset/ - reset password
POST /auth/password/reset/confirm/ - confirm password reset
POST /auth/password/change/ - change password
POST /auth/token/refresh/ - refresh token
GET /auth/users/me/ - get user details
PUT /auth/users/me/ - update user details
"""
