from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from marketplace_auth.serializer import UserSerializer
from django.contrib.auth import authenticate, login, logout
from marketplace.serializers import BucketSerializer


@api_view(['POST'])
def user_registration(request):
    data = request.data
    serializer = UserSerializer(data=data)
    serializer.is_valid(True)
    serializer.save()
    serializer.instance.set_password(data['password'])
    serializer.instance.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_view(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response(status=status.HTTP_200_OK)
    else:
        data = {
            'response': 'Invalid login/password'
        }
        return Response(data)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response()
