from django.urls import path
from . import views

urlpatterns = [
    path('make-payment/<int:booking_id>/', views.make_payment_view, name='make_payment'),
    path('make-payment/<int:booking_id>/', views.make_payment_view, name='make_payment'),
    path('checkout/<int:booking_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success_view, name='payment_success'),
    path('cancel/', views.payment_cancel_view, name='payment_cancel'),
]
