from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularJSONAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SwaggerUIView  # Adjust this import based on where you put the SwaggerUIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/json/', SpectacularJSONAPIView.as_view(), name='schema-json'),
    path('api/docs/', SwaggerUIView.as_view(), name='swagger-ui'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]