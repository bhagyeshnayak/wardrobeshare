from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import Conversation, Message
from products.models import Product


@login_required
def start_chat(request, product_id):
    """
    Start or open an existing chat conversation for a product
    between customer and owner.
    """

    product = get_object_or_404(Product, id=product_id)

    # Owner should not chat with themselves
    if request.user == product.owner:
        return redirect('inbox')

    # Ensure product is available for chat
    if not getattr(product, 'is_available', True):
        return HttpResponseForbidden("This product is not available for chat.")

    # Check if conversation already exists
    conversation = Conversation.objects.filter(
        product=product,
        customer=request.user
    ).first()

    # Create new conversation if not exists
    if not conversation:
        conversation = Conversation.objects.create(
            product=product,
            owner=product.owner,
            customer=request.user
        )

    return redirect('chat_room', conversation_id=conversation.id)


@login_required
def chat_room(request, conversation_id):
    """
    Main chat room view – shows messages and allows sending new messages.
    """

    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Security: only participants can access
    if request.user not in [conversation.owner, conversation.customer]:
        return HttpResponseForbidden("You are not part of this conversation.")

    # Mark unread messages as read
    if request.user == conversation.owner:
        conversation.messages.filter(
            sender=conversation.customer,
            is_read=False
        ).update(is_read=True)
    else:
        conversation.messages.filter(
            sender=conversation.owner,
            is_read=False
        ).update(is_read=True)

    # Handle sending message
    if request.method == 'POST':
        content = request.POST.get('text')

        if content and content.strip():
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content.strip()
            )

            # Update conversation timestamp
            conversation.save()

            return redirect('chat_room', conversation_id=conversation.id)

    # Get all messages ordered by time
    chat_messages = conversation.messages.all().order_by('timestamp')

    context = {
        'conversation': conversation,
        'chat_messages': chat_messages,
    }

    return render(request, 'chat/chat_room.html', context)


@login_required
def inbox(request):
    """
    User inbox – list all chat conversations for current user.
    """

    user = request.user

    # Get conversations where user is either owner or customer
    conversations = Conversation.objects.filter(
        Q(owner=user) | Q(customer=user)
    ).order_by('-updated_at')

    # Calculate unread counts and partner info
    for conv in conversations:
        if user == conv.owner:
            conv.unread_count = conv.messages.filter(
                sender=conv.customer,
                is_read=False
            ).count()
            conv.partner = conv.customer
        else:
            conv.unread_count = conv.messages.filter(
                sender=conv.owner,
                is_read=False
            ).count()
            conv.partner = conv.owner

    context = {
        'conversations': conversations
    }

    return render(request, 'chat/inbox.html', context)
