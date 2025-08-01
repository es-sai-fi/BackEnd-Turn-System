from rest_framework import serializers
from .models import CustomUser, Role
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['user'] = UserListSerializer(user).data
        data['role_id'] = self.user.role_id.role_id
        data['message'] = "Logueado"
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        priority = 'Alta' if data['priority'] == 'H' else (
            'Media' if data['priority'] == 'M' else 'Estándar')
        return {'id': data['id'],  
                'role_id': data['role_id'],
                'Nombre del usuario': data['name'],
                'Correo electronico:': data['email'],
                'Prioridad': priority,
                }


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'name', 'age', 'condition']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['role_id'] = Role.objects.get(role_id=2)
        if validated_data['condition'] == True and (validated_data['age'] > 55 or validated_data['age'] < 12):
            validated_data['priority'] = "H"

        elif (validated_data['age'] > 55 or validated_data['age'] < 12) or validated_data['condition'] == True:
            validated_data['priority'] = "M"
        else:
            validated_data['priority'] = "L"
        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserEmployeeCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'name', 'last_name','age', 'condition']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.role_id = Role.objects.get(role_id=3)
        user.save()
        return user
    
class UserEmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['Nombre del usuario'] = data['name']
        data['Correo electronico'] = data['email']
        return data