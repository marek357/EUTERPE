from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('list/', views.lista, name='list'),
    path('endpoint/', views.endpoint, name='endpoint'),
]
