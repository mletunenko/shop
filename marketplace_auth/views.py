from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from marketplace_auth.serializer import UserSerializer
from django.contrib.auth import authenticate, login, logout


@api_view(['POST'])
def user_registration(request):
    data = request.data
    serializer = UserSerializer(data=data)
    serializer.is_valid(True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_view(request):
    email = request.data['email']
    password = request.data['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return Response()
    else:
        data = {
            'response': 'Invalid login/password'
        }
        return Response(data)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response()
