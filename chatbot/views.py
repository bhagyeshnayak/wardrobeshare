from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

@csrf_exempt
@require_POST
def chat_response(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').lower()
        
        # Simple keyword-based logic (can be replaced with AI later)
        response_text = "I'm not sure about that. Try asking 'how to rent' or 'contact support'."
        
        if 'rent' in user_message or 'book' in user_message:
            response_text = "To rent a product, browse our catalog, select an item, and click 'Book Now'. You'll need to be logged in."
        elif 'list' in user_message or 'sold' in user_message or 'sell' in user_message or 'owner' in user_message:
            response_text = "To list your clothes, go to your Dashboard and click 'Add Product'. You need to be registered as an Owner or Both."
        elif 'pay' in user_message or 'price' in user_message or 'cost' in user_message:
            response_text = "We assist with secure payments via Stripe. Prices are listed per day."
        elif 'contact' in user_message or 'support' in user_message or 'help' in user_message:
            response_text = "You can contact support at support@wardrobeshare.com or call +91-9876543210."
        elif 'hello' in user_message or 'hi' in user_message:
            response_text = "Hello! How can I help you today?"
            
        # Store in session (optional, for continuity)
        if 'chat_history' not in request.session:
            request.session['chat_history'] = []
        request.session['chat_history'].append({'user': user_message, 'bot': response_text})
        request.session.modified = True
        
        return JsonResponse({'response': response_text})
        
    except Exception as e:
        return JsonResponse({'response': 'Error processing your request.'}, status=500)
