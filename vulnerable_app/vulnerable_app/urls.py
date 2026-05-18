from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from blog.api_views import TokenObtainThrottle

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('blog.urls')),
    path('api/token/', TokenObtainPairView.as_view(throttle_classes=[TokenObtainThrottle])),
    path('api/token/refresh/', TokenObtainPairView.as_view(throttle_classes=[TokenObtainThrottle])),
    path('', include('blog.urls')),
]