from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response

from marketplace_auth.serializer import UserSerializer


@api_view(['POST'])
def user_registration(request):
    data = request.data
    serializer = UserSerializer(data=data)
    serializer.is_valid(True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
