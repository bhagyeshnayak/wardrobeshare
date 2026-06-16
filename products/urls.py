from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list_view, name='product_list'),
    path('<int:pk>/', views.product_detail_view, name='product_detail'),
    path('<int:pk>/review/', views.add_review_view, name='add_review'),
    path('<int:pk>/edit/', views.edit_product_view, name='edit_product'),
    path('add/', views.add_product_view, name='add_product'),
]
