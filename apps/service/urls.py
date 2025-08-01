from django.urls import path
from .views import ServiceListAPIView, ServiceDetailAPIView


urlpatterns = [
    path('', ServiceListAPIView.as_view(), name='service_api'),
    path('<int:sid>', ServiceDetailAPIView.as_view(), name='service_detail'),
]
