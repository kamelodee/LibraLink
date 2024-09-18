# In your views.py file

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import ChangePasswordSerializer, CustomUserSerializer, UserLoginSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated




class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CustomUserSerializer

    @extend_schema(
        request=CustomUserSerializer,
        responses={201: CustomUserSerializer},
        description="Register a new user and obtain user info with access and refresh tokens"
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    @extend_schema(
        request=UserLoginSerializer,
        responses={200: CustomUserSerializer},
        description="Login and obtain user info with access and refresh tokens"
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = CustomUserSerializer(user)
            
            return Response({
                'user': user_serializer.data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_object(self):
        """
        Retrieve the user object.
        For actions that operate on a specific user, always return the logged-in user.
        This ensures users can only access/modify their own data.
        """
        return self.request.user

    @extend_schema(description="Register a new user")
    def create(self, request, *args, **kwargs):
        """
        Create a new user (register).
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(description="Retrieve the logged-in user's details")
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the logged-in user's details.
        The pk parameter in the URL is ignored; it always returns the current user.
        """
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(description="Update the logged-in user's details")
    def update(self, request, *args, **kwargs):
        """
        Update the logged-in user's details.
        The pk parameter in the URL is ignored; it always updates the current user.
        """
        return super().update(request, *args, **kwargs)

   

    @extend_schema(description="Delete the logged-in user's account")
    def destroy(self, request, *args, **kwargs):
        """
        Delete the logged-in user's account.
        The pk parameter in the URL is ignored; it always deletes the current user.
        """
        return super().destroy(request, *args, **kwargs)

    @extend_schema(description="List all users (admin only)")
    def list(self, request, *args, **kwargs):
        """
        List all users. This should typically be restricted to admin users.
        """
        if not request.user.is_staff:
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)

    @extend_schema(description="Change the logged-in user's password")
   
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.validated_data['old_password']):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "Incorrect old password."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)