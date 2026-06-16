from django.urls import path
from . import views

urlpatterns = [
    path('start/<int:product_id>/', views.start_chat, name='start_chat'),
    path('room/<int:conversation_id>/', views.chat_room, name='chat_room'),
    path('inbox/', views.inbox, name='inbox'),
]
