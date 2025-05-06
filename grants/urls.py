from django.urls import path
from . import views

urlpatterns = [
    path('request_code/', views.request_code, name='request_code'),
    path('verify_code/<str:email>/', views.verify_code, name='verify_code'),
]