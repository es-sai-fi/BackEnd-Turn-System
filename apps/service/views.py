from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ServiceSerializer
from ..custom_user.authentication_mixin import IsUserRole, IsAdminRole
from .models import Service


class ServiceListAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsUserRole()]
        elif self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminRole()]
        return super().get_permissions()
    
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ServiceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsUserRole()]
        elif self.request.method == 'PUT':
            return [IsAuthenticated(), IsAdminRole()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminRole()]
        return super().get_permissions()
    
    def get_service(self, sid):
        return Service.objects.filter(service_id=sid).first()
    
    def get(self, request, sid):
        service = self.get_service(sid)
        serializer = ServiceSerializer(service)

        if not service:
            return Response({'message:' 'Servicio no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, sid):
        service = self.get_service(sid)
        serializer = ServiceSerializer(
            service, data=request.data, partial=True)

        if not service:
            return Response({'message:' 'Servicio no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, sid):
        service = self.get_service(sid)

        if service:
            service.delete()

            return Response({'message': 'Servicio Eliminado.'}, status=status.HTTP_200_OK)

        return Response({'message:' 'Servicio no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
