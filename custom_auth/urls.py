from django.urls import path, include
from custom_auth import views as custom_auth_views

urlpatterns = [
    path("accounts/register/", custom_auth_views.register, name ="register"),
    path("accounts/", include("django.contrib.auth.urls")),
]
