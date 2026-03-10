from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .throttles import TieredRateThrottle
from .models import DailyWeatherStats
from .serializers import DailyWeatherStatsSerializer
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

class DailyWeatherStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows weather stats to be viewed.
    Secured with JWT Authentication and Tiered Rate Limiting.
    """
    queryset = DailyWeatherStats.objects.all().order_by('-record_date')
    serializer_class = DailyWeatherStatsSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [TieredRateThrottle] # <-- Your custom Paywall

class CreateStripeCheckoutSessionView(APIView):
    """
    Creates a Stripe Checkout Session for users to purchase Premium Access.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=str(request.user.id),
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': 999,  # This means $9.99
                            'product_data': {
                                'name': 'Premium Weather API Access',
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                # In a real app, these go to frontend pages. 
                # For now, we redirect them back to your documentation.
                success_url='http://127.0.0.1:8000/api/docs/?success=true',
                cancel_url='http://127.0.0.1:8000/api/docs/?canceled=true',
            )
            # We return the URL so the frontend can redirect the user to the payment page
            return Response({'checkout_url': checkout_session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        

@csrf_exempt
def stripe_webhook(request):
    """
    Listens for background events from Stripe.
    If a payment succeeds, upgrades the user to Premium (is_staff=True).
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    # In a real production environment, you must verify the signature using a webhook secret.
    # For this portfolio demonstration, we will read the payload directly.
    try:
        event = stripe.Event.construct_from(
            stripe.json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        return HttpResponse(status=400)

    # Check if the event is a successful payment
    if event.type == 'checkout.session.completed':
        session = event.data.object
        
        # Retrieve the user ID we passed in Step 1
        user_id = session.get('client_reference_id')
        
        if user_id:
            try:
                # Find the user in the database and upgrade them to Premium
                user = User.objects.get(id=user_id)
                user.is_staff = True
                user.save()
                print(f"SUCCESS: User {user.username} upgraded to Premium!")
            except User.DoesNotExist:
                print("Error: User not found.")

    # Always return a 200 OK to Stripe so they know we received the message
    return HttpResponse(status=200)