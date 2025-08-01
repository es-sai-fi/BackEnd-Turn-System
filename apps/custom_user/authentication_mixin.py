from rest_framework import authentication, exceptions
from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import BasePermission
from .authenticate import ExpiringTokenAuthentication

class Authentication(authentication.BaseAuthentication):
    user = None

    def get_user(self,request):
        """
        Return:
            * user      : User Instance or
            * message   : Error Message or
            * None      : Corrup Token
        """
        token = get_authorization_header(request).split()
        
        if token:
            try:
                token = token[1].decode()
            except:
                return None

            token_expire = ExpiringTokenAuthentication()
            user = token_expire.authenticate_credentials(token)

            if user != None:
                self.user = user
                return user

        return None

    def authenticate(self, request):
        self.get_user(request)
        if self.user is None:
            raise exceptions.AuthenticationFailed('No se han enviado las credenciales.')

        return (self.user, 1)

class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role_id.role_id == 1

class IsWorkerRole(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role_id.role_id == 3

class IsUserRole(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role_id.role_id == 2