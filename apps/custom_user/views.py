from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .authentication_mixin import IsAdminRole
from .serializers import UserSerializer, UserListSerializer, UserCreationSerializer, UserEmployeeListSerializer, UserEmployeeCreationSerializer
from .models import CustomUser
from .serializers import CustomTokenObtainPairSerializer


def get_user(self, uid):
    return CustomUser.objects.filter(id=uid).first()


@api_view(['GET', 'POST', 'DELETE'])
def user_employee_api_view(request):
    permission_classes = [IsAuthenticated,IsAdminRole]
    if request.method == 'GET':
        users = CustomUser.objects.filter(role_id=3)
        serializer = UserEmployeeListSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserEmployeeCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def user_api_view(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, uid):
    if request.method == 'GET':
        user = CustomUser.objects.filter(id=uid).first()
        serializer = UserSerializer(user)
        if user is None:
            return Response({"error": "Usuario no encontrado"}, status=404)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Sesión cerrada"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'Message': 'Error al iniciar sesión.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
