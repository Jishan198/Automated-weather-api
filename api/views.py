from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .throttles import TieredRateThrottle
from .models import DailyWeatherStats
from .serializers import DailyWeatherStatsSerializer
import stripe
from django.core.cache import cache
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import DailyWeatherStats 
from drf_spectacular.utils import extend_schema # Use your actual model name
from .tasks import process_successful_payment
from django.shortcuts import render
import json

def dashboard_view(request):
    return render(request, 'dashboard.html')

class WeatherListView(APIView):
    def get(self, request):
        cache_key = 'all_weather_stats_cache'
        cached_data = cache.get(cache_key)

        if cached_data:
            print("--- SPEED BOOST: DATA RETRIEVED FROM REDIS ---")
            return Response(cached_data)

        print("--- CACHE MISS: FETCHING FROM MYSQL DATABASE ---")
        
        queryset = DailyWeatherStats.objects.all().order_by('-record_date')
        
        # CHANGE THIS LINE: Use the correct serializer name
        serializer = DailyWeatherStatsSerializer(queryset, many=True) 
        
        data = serializer.data
        cache.set(cache_key, data, 900)

        return Response(data)
    

class DailyWeatherStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows weather stats to be viewed.
    Secured with JWT Authentication and Tiered Rate Limiting.
    Now supercharged with Redis Caching.
    """
    queryset = DailyWeatherStats.objects.all().order_by('-record_date')
    serializer_class = DailyWeatherStatsSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [TieredRateThrottle] 

    def list(self, request, *args, **kwargs):
        cache_key = 'all_weather_stats_cache'
        
        # 1. Try to get data from Redis
        cached_data = cache.get(cache_key)

        if cached_data:
            print("--- SPEED BOOST: DATA RETRIEVED FROM REDIS ---")
            return Response(cached_data)

        # 2. If not in Redis, let the ViewSet fetch from MySQL normally
        print("--- CACHE MISS: FETCHING FROM MYSQL DATABASE ---")
        response = super().list(request, *args, **kwargs)
        
        # 3. Store the result in Redis for 15 minutes
        cache.set(cache_key, response.data, 900)
        
        return response

class CreateStripeCheckoutSessionView(APIView):
    """
    Creates a Stripe Checkout Session for users to purchase Premium Access.
    """
    permission_classes = [IsAuthenticated]
    @extend_schema(responses=None)
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
    If a payment succeeds, hands off the user upgrade to a Celery background task.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    # In a real production environment, you must verify the signature using a webhook secret.
    # For this portfolio demonstration, we will read the payload directly.
    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        return HttpResponse(status=400)

    # Check if the event is a successful payment
    if event.type == 'checkout.session.completed':
        session = event.data.object
        
        # Retrieve the user ID we passed in Step 1
        user_id = session.get('client_reference_id')
        
        if user_id:
            print(f"WEBHOOK: Payment received for User ID {user_id}! Handing off to Celery...")
            
            # THE MAGIC LINE: Sends the heavy lifting to the background worker
            process_successful_payment.delay(user_id)

    # Always return a 200 OK instantly to Stripe so they know we received the message
    return HttpResponse(status=200)