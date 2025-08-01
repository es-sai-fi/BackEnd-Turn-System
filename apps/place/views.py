from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import PlaceSerializer, PlaceGETSerializer, PlaceCustomUserSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..custom_user.models import CustomUser
from ..custom_user.authentication_mixin import IsUserRole,IsAdminRole,IsWorkerRole
from .models import Place, PlaceCustomUser


class PlaceListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        places = Place.objects.all()
        serializer = PlaceGETSerializer(places, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PlaceCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminRole]
    
    def post(self, request):
        serializer = PlaceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PlaceDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'PUT':
            return [IsAuthenticated(), IsAdminRole()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def get_place(self, pid):
        return Place.objects.filter(place_id=pid).first()
    
    def get(self, request, pid):
        place = self.get_place(pid)
        if place:
            serializer = PlaceGETSerializer(place)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message:' 'Punto de Atención no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pid):
        place = self.get_place(pid)
        serializer = PlaceSerializer(place, data=request.data, partial=True)

        if place:
            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message:' 'Punto de Atención no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pid):
        place = self.get_place(pid)

        if place:
            place.delete()

            return Response({'message': 'Punto Eliminado.'}, status=status.HTTP_200_OK)

        return Response({'message:' 'Punto de Atención no encontrado.'}, status=status.HTTP_404_NOT_FOUND)


class UserPlacesDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_place(self, pid):
        return CustomUser.objects.filter(place_id=pid).first()

    def get_user(self, uid):
        return CustomUser.objects.filter(id=uid).first()
    
    def get(self, request, uid):
        user = self.get_user(uid)
        if not user:
            return Response({'message:' 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        user_places = PlaceCustomUser.objects.filter(custom_user_id=user)
        serializer = PlaceCustomUserSerializer(user_places, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AddUserToPlaceAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]
    
    def get_place(self, pid):
        return Place.objects.filter(place_id=pid).first()
    
    def get_user(self, uid):
        return CustomUser.objects.filter(id=uid).first()
    
    def post(self, request, uid, pid):
        data = {"custom_user_id":uid, "place_id":pid}
        serializer = PlaceCustomUserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
