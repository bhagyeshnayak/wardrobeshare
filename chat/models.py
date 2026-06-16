from django.db import models
from django.conf import settings
from products.models import Product

class Conversation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='conversations')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner_conversations')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensure one conversation per product+customer pair
        unique_together = ('product', 'customer')
        ordering = ['-updated_at']

    def __str__(self):
        return f"Chat: {self.product.title} - {self.customer.username}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message by {self.sender.username} at {self.timestamp}"

