from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import User
from .serializers import (
    UserSerializer,
    UserDetailSerializer,
    UserRegistrationSerializer,
    LoginSerializer
)


@extend_schema(
    summary="User registration",
    description="Register a new user account and receive an authentication token.",
    request=UserRegistrationSerializer,
    responses={201: UserDetailSerializer},
    tags=['Authentication'],
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user)
        return Response({
            'user': UserDetailSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="User login",
    description="Login with username and password to receive an authentication token.",
    request=LoginSerializer,
    responses={
        200: {
            'type': 'object',
            'properties': {
                'token': {'type': 'string'},
                'user': {'type': 'object'}
            }
        }
    },
    tags=['Authentication'],
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login and get auth token"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserDetailSerializer(user).data
            })
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="User logout",
    description="Logout and delete the authentication token.",
    request=None,
    responses={200: {'description': 'Successfully logged out'}},
    tags=['Authentication'],
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout and delete token"""
    request.user.auth_token.delete()
    return Response({'message': 'Successfully logged out'})


@extend_schema_view(
    list=extend_schema(
        summary="List all users",
        tags=['Users'],
    ),
    retrieve=extend_schema(
        summary="Get user details",
        tags=['Users'],
    ),
)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get current user profile",
        tags=['Users'],
    )
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
