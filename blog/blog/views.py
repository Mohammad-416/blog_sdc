from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from blog_app.models import CustomUser
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import secrets
import re
import os
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.urls import reverse

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        # Validate username and password
        if not re.match(r'^[a-zA-Z0-9_-]{3,30}$', username):
            return Response({'error': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)
        if not re.match(r'^(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            return Response({'error': 'Password must contain at least 8 characters, one digit, and one special character'}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()

        
        

        return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({'error': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'author_id': str(user.author_id)
        }, status=status.HTTP_200_OK)

class ActivateAccountView(APIView):
    def get(self, request, email_token):
        try:
            user = CustomUser.objects.get(author_id=email_token)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            user.is_active = True
            user.save()
            return Response({'message': 'Account activated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Your account is already active'}, status=status.HTTP_200_OK)

class CreateSuperUserView(APIView):
    def post(self, request):
        secret_key = settings.SUPERUSER_SECRET_KEY
        provided_secret = request.data.get('secret')

        if secret_key != provided_secret:
            return Response({'error': 'Invalid secret key'}, status=status.HTTP_401_UNAUTHORIZED)

        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            CustomUser.objects.create_superuser(username, email, password)
            return Response({'message': 'Superuser created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def get_username(request, author_id):
    user = CustomUser.objects.get(author_id=author_id)
    return JsonResponse({'username : ': user.username}, status=200)
    
def refresh_token(request, token):
    refresh_token = token
    
    try:
        token = RefreshToken(refresh_token)
        access_token = str(token.access_token)
        
        # Set the new access token in the response
        response = {
            'access': access_token,
            'refresh': str(token)
        }
        
        return JsonResponse(response)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
