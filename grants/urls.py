from django.urls import path
from . import views

urlpatterns = [
    path('request-code/', views.request_code, name='request_code'),
    path('verify-code/<str:email>/', views.verify_code, name='verify_code'),
]