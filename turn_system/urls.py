from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import StatsAPIView

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Documentación de la API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('place/', include('apps.place.urls')),
    path('turn/', include('apps.turn.urls')),
    path('service/', include('apps.service.urls')),
    path('user/', include('apps.custom_user.urls')),
    path('stats/', StatsAPIView.as_view()),
]
