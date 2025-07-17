from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.schedule_list, name='list'),
    path('session/<slug:slug>/', views.session_detail, name='session_detail'),
]