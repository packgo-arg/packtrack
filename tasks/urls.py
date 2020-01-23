from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListTask),
    path('<int:pk>/', views.DetailTask),
]
