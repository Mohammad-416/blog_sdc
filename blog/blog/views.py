from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=username,
            password=make_password(password),  # Hash the password
            email=email
        )
        user.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.check_password(password):
                # Obtain tokens for the user
                refresh = RefreshToken.for_user(user)
                print("Access Token:", str(refresh.access_token))
                print("Refresh Token:", str(refresh))
                return Response({'Access Token' : str(refresh.access_token) , 'Refresh Token' : str(refresh)}, status=status.HTTP_200_OK)


