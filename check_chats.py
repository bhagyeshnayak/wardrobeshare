import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from chat.models import Message as ChatMessage
from chatbot.models import Message as ChatbotMessage

print("--- Chat App Messages ---")
chat_msgs = ChatMessage.objects.all()
print(f"Count: {chat_msgs.count()}")
for msg in chat_msgs:
    print(f"- {msg.sender}: {msg.text}")

print("\n--- Chatbot App Messages ---")
chatbot_msgs = ChatbotMessage.objects.all()
print(f"Count: {chatbot_msgs.count()}")
for msg in chatbot_msgs:
    print(f"- {msg.sender}: {msg.content}")
