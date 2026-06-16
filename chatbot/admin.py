from django.contrib import admin
from .models import ChatRoom, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('timestamp',)

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'owner', 'customer', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('product__title', 'owner__username', 'customer__username')
    inlines = [MessageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'sender', 'timestamp', 'is_read')
    list_filter = ('timestamp', 'is_read')
    search_fields = ('content', 'sender__username')
