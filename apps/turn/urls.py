from django.urls import path
from .views import TurnAPIView, CloseTurnAPIView, NextTurnAPIView, UserActiveTurnAPIView, UserTurnsAPIView, CancelTurnAPIView
from .views import avg_attendacy_time

urlpatterns = [
    path('user_turns/<int:uid>', UserTurnsAPIView.as_view(), name='user_turns'),
    path('', TurnAPIView.as_view(), name='turn_api'),
    path('close_turn/<int:uid>/<int:tid>',
         CloseTurnAPIView.as_view(), name='close_turn'),
     path('cancel_turn/<int:tid>',
         CancelTurnAPIView.as_view(), name='cancel_turn'),
    path('user_active_turn/<int:uid>',
         UserActiveTurnAPIView.as_view(), name='user_active_turn'),
    path('next_turn/<int:uid>/<int:pid>',
         NextTurnAPIView.as_view(), name='next_turn')
]
