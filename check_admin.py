import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib import admin
from chatbot.models import ChatRoom, Message

print("Checking admin registration...")

is_chatroom_registered = admin.site.is_registered(ChatRoom)
is_message_registered = admin.site.is_registered(Message)

print(f"ChatRoom registered: {is_chatroom_registered}")
print(f"Message registered: {is_message_registered}")

if is_chatroom_registered and is_message_registered:
    print("SUCCESS: Both models are registered in admin.")
else:
    print("FAILURE: One or both models are NOT registered.")
