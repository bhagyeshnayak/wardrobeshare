from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:product_id>/', views.create_booking_view, name='create_booking'),
    path('<int:pk>/', views.booking_detail_view, name='booking_detail'),
    path('<int:pk>/verify/', views.verify_booking_otp_view, name='verify_booking_otp'),
    path('<int:pk>/return/', views.return_product_view, name='return_product'),
    path('<int:pk>/cancel/', views.cancel_booking_view, name='cancel_booking'),
]
