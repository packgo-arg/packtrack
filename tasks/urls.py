from django.urls import path

from . import views

urlpatterns = [
    path('', views.OrderList.as_view()),
    path('<int:pk>/', views.OrderDetail.as_view()),
    path('status/', views.StatusDetail.as_view()),
    path('order_price/', views.PriceDetail.as_view()),
]
