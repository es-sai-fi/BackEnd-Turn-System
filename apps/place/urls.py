from django.urls import path
from .views import PlaceListAPIView, PlaceDetailAPIView, UserPlacesDetailAPIView, AddUserToPlaceAPIView, \
    PlaceCreateAPIView

urlpatterns = [
    path('', PlaceListAPIView.as_view(), name='place_api'),
    path('create_place', PlaceCreateAPIView.as_view(), name='place_Create_api'),
    path('<int:pid>', PlaceDetailAPIView.as_view(), name='place_detail'),
    path('user_places/<int:uid>', UserPlacesDetailAPIView.as_view(), name='user_places'),
    path('add_user_to_place/<int:uid>/<int:pid>', AddUserToPlaceAPIView.as_view(), name='add_user_to_place')
]
