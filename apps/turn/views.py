import math

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from ..custom_user.models import CustomUser
from .models import Turn
from ..place.models import Place
from ..custom_user.authentication_mixin import IsUserRole, IsWorkerRole
from .serializers import TurnSerializer, CreateTurnSerializer


def avg_attendacy_time(turns):
    total_minutes = sum(t.turn_attended_time for t in turns)
    expected_minutes = total_minutes / turns.count()

    return expected_minutes


class UserTurnsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_user(self, uid):
        return CustomUser.objects.filter(id=uid).first()

    def get(self, request, uid):
        owner = self.get_user(uid)

        if not owner:
            return Response({'message': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        turns = Turn.objects.filter(owner=owner)
        serializer = TurnSerializer(turns, many=True)

        if turns.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'No se encontraron turnos.'}, status=status.HTTP_200_OK)


class UserActiveTurnAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get_user(self, uid):
        return CustomUser.objects.filter(id=uid).first()

    def get(self, request, uid):
        user = self.get_user(uid)

        if not user:
            return Response({'message': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        turn = Turn.objects.filter(owner=user, active=True).first()

        if not turn:
            return Response({'message': 'No tiene turno activo.'}, status=status.HTTP_200_OK)

        time_eight_hours_ago = timezone.now() - timedelta(hours=8)

        past_turns = Turn.objects.filter(
            active=False,
            place_id=turn.place_id,
            date_created__gte=time_eight_hours_ago,
        )

        if past_turns.exists():
            expected_minutes = math.ceil(avg_attendacy_time(past_turns))
        else:
            expected_minutes = 5.0

        serializer = TurnSerializer(turn)
        
        next_turn = Turn.objects.filter(
            place_id=turn.place_id,
            turn_priority=turn.turn_priority,
            active=True
        ).order_by('date_created').first()

        is_next = (next_turn and next_turn.turn_id == turn.turn_id)

        serializer = TurnSerializer(turn)
        
        return Response({**serializer.data, 'expected_attendacy_time': expected_minutes, 'is_next': is_next}, status=status.HTTP_200_OK)


class CloseTurnAPIView(APIView):
    permission_classes = [IsAuthenticated, IsWorkerRole]
    
    def get_turn(self, tid):
        return Turn.objects.filter(turn_id=tid).first()

    def get_user(self, uid):
        return CustomUser.objects.filter(id=uid).first()

    def get(self, request, uid, tid):
        turn = self.get_turn(tid)
        attended_by = self.get_user(uid)

        if not turn:
            return Response({'message': 'Turno no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if not attended_by:
            return Response({'message': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        turn.active = False
        turn.attended_by = attended_by
        turn.date_closed = timezone.now()
        turn.save()

        return Response({'message': 'Turno cerrado.'}, status=status.HTTP_200_OK)


class CancelTurnAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get_turn(self, tid):
        return Turn.objects.filter(turn_id=tid).first()

    def get(self, request, tid):
        turn = self.get_turn(tid)

        if not turn:
            return Response({'message': 'Turno no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if not request.user == turn.owner:
            return Response({'message': 'No tiene permiso.'}, status=status.HTTP_403_FORBIDDEN)

        turn.active = False
        turn.canceled = True
        turn.date_closed = timezone.now()
        turn.save()

        return Response({'message': 'Turno cancelado.'}, status=status.HTTP_200_OK)


class TurnDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get_turn(self, tid):
        return Turn.objects.filter(turn_id=tid).first()

    def get(self, request, tid):
        turn = self.get_turn(tid)

        if not turn:
            return Response({'message': 'Turno no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TurnSerializer(turn)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TurnAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        turns = Turn.objects.all()
        serializer = TurnSerializer(turns, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateTurnSerializer(data=request.data)

        if serializer.is_valid():
            owner = serializer.validated_data.get('owner')
            place = serializer.validated_data.get('place_id')

            owner_turns = Turn.objects.filter(owner=owner, active=True)

            if owner_turns.count() != 0:
                return Response({'message': 'Ya tiene un turno activo.'}, status=status.HTTP_404_NOT_FOUND)

            turn_count = Turn.objects.filter(
                place_id=place).count()

            turn_priority = owner.priority if owner.priority else "M"

            turn_number = (turn_count % 999) + 1

            turn_name = f"{turn_priority}-{turn_number:03d}"

            turn = serializer.save(
                turn_priority=turn_priority, turn_name=turn_name)

            response_serializer = TurnSerializer(turn)

            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NextTurnAPIView(APIView):
    permission_classes = [IsAuthenticated, IsWorkerRole]
    
    def get_place(self, pid):
        return Place.objects.filter(place_id=pid).first()

    def get_user(self, uid):
        return CustomUser.objects.filter(id=uid).first()

    def get(self, request, uid, pid):
        place = self.get_place(pid)
        attended_by = self.get_user(uid)

        if not place:
            return Response({'message:' 'Punto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if not attended_by:
            return Response({'message:' 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        for priority in ['H', 'M', 'L']:
            turn = Turn.objects.filter(
                place_id=place, active=True, turn_priority=priority).order_by('date_created').first()

            if turn:
                serializer = TurnSerializer(turn)
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'No hay turnos activos.'}, status=status.HTTP_200_OK)
