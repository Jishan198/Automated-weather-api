from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DailyWeatherStatsViewSet, CreateStripeCheckoutSessionView
from .views import DailyWeatherStatsViewSet, CreateStripeCheckoutSessionView, stripe_webhook

router = DefaultRouter()
router.register(r'weather', DailyWeatherStatsViewSet, basename='weather')

urlpatterns = [
    path('', include(router.urls)),
    path('checkout/', CreateStripeCheckoutSessionView.as_view(), name='stripe-checkout'),
    path('webhook/', stripe_webhook, name='stripe-webhook'), 
]