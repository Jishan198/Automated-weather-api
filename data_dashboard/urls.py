from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from api.views import dashboard_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # JWT Authentication Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # OpenAPI Schema (The raw JSON structure)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI (The visual interface)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', dashboard_view, name='dashboard')
]