from rest_framework import exceptions, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes
    )
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from core.serializers import SchoolSerilizer
from core.models import Role
from core.authentication import JWTAuthentication
from core import serializers, models
from core.permissions import IsStaff
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserAPIView(generics.CreateAPIView):
    """Creating new View"""
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny, )


class CreateTokenAPIView(ObtainAuthToken):
    """Create a new token for a user"""
    serializer_class = serializers.AuthTokenSerializer
    permission_classes = (AllowAny, )
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage authenticated user"""
    serializer_class = serializers.UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = models.User.objects.filter(email=email).first()

    if user is None:
        raise exceptions.AuthenticationFailed(
            'User not found',
            )

    if not user.check_password(password):
        raise exceptions.AuthenticationFailed(
            'Incorrect password',
            )

    response = Response()

    token = authentication.generate_access_token(user)
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {'jwt': token}

    return response


@api_view(['POST'])
def logout(_):  # Replace params with _ if not be used.
    response = Response()
    response.delete_cookie(key='jwt')
    response.data = {'message': 'Success'}
    return response


class AuthenticatedUser(APIView):
    authentication_classes = [
        authentication.TokenAuthentication,
        JWTAuthentication
        ]

    def get(self, request):
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)


class PermissionAPIView(APIView):

    authentication_classes = [
        authentication.TokenAuthentication,
        JWTAuthentication
        ]

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.PermissionSerializer(
            models.Permission.objects.all(),
            many=True
            )

        return Response(serializer.data)


class RoleViewSets(ModelViewSet):
    '''User roles Viewsets'''

    authentication_classes = (
        JWTAuthentication,
        authentication.TokenAuthentication
        )
    queryset = Role.objects.all()
    permission_classes = (IsStaff, )

    serializer_class = serializers.RoleSerializer


@api_view(['GET'])
@authentication_classes([
    JWTAuthentication,
    authentication.TokenAuthentication
    ])
@permission_classes([IsStaff])
def current_school(request):
    '''Current School Information'''

    school = request.user.school
    serializer = SchoolSerilizer(school)
    return Response(serializer.data)


class CRUDViewSets(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet
        ):
    permission_classes = (IsStaff, )

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(
            created_by=self.request.user.email,
            school=self.request.user.school
            )

    def perform_update(self, serializer):
        return serializer.save(
            updated_by=self.request.user.email
            )
