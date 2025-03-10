from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, logout
from .serializers import LoginSerializer, SignUpSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CarAuctionSerializer
from auctions.models import CarAuction
from django.utils import timezone
import logging
from django.db.models import F

# Set up logging
logger = logging.getLogger(__name__)

# Create your views here.

class LoginView(APIView):
    def post(self, request):
        logger.debug("=== 🔐 Login Attempt ===")
        logger.debug("📨 Headers: %s", request.headers)
        logger.debug("📦 Body: %s", request.data)
        
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            logger.debug("✅ Serializer valid: %s", serializer.validated_data)
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            logger.debug("👤 User authenticated: %s", user)
            
            if user:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                
                logger.debug("🎟️ Generated tokens:")
                logger.debug("Access token: %s...", access_token[:10])
                logger.debug("Refresh token: %s...", refresh_token[:10])
                
                return Response({
                    'message': 'Login successful',
                    'is_admin': user.is_staff,
                    'tokens': {
                        'access': access_token,
                        'refresh': refresh_token
                    },
                    'username': user.username,
                    'email': user.email
                }, status=status.HTTP_200_OK)
            
            logger.warning("❌ Authentication failed")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        logger.error("❌ Serializer errors: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

class SignUpView(APIView):
    def post(self, request):
        logger.debug("==== Signup Attempt ====")
        logger.debug("Request data: %s", request.data)
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({
                    'message': 'User created successfully'
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error("Error creating user: %s", str(e))
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        logger.error("Serializer errors: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        data = [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined,
            'is_staff': user.is_staff
        } for user in users]
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            if user.is_staff:
                return Response(
                    {'error': 'Cannot delete admin users'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class TestAuthView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        print("\n=== 🔒 Protected Endpoint Access ===")
        print(f"👤 Authenticated user: {request.user.username}")
        return Response({
            'message': 'You have access to this protected endpoint',
            'user': request.user.username
        })

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        active_auctions = CarAuction.objects.filter(
            seller=user,
            start_time__lte=timezone.now(),
            duration_hours__gt=0
        )
        previous_auctions = CarAuction.objects.filter(
            seller=user,
            start_time__lt=timezone.now(),
            duration_hours__lte=0
        )

        active_auctions_data = [
            {
                'title': auction.name,
                'current_bid': auction.current_bid,
                'time_left': auction.time_left,
            } for auction in active_auctions
        ]

        previous_auctions_data = [
            {
                'title': auction.name,
                'final_price': auction.current_bid,
                'date': auction.created_at,
            } for auction in previous_auctions
        ]

        profile_data = {
            'username': user.username,
            'email': user.email,
            'profile_picture': None,  # Default to None
            'active_auctions': active_auctions_data,
            'previous_auctions': previous_auctions_data,
        }

        # Check if the user has a profile
        if hasattr(user, 'profile'):
            profile_data['profile_picture'] = user.profile.profile_picture.url if user.profile.profile_picture else None

        return Response(profile_data)
