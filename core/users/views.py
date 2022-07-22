from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# Create your views here.


@api_view(['GET'])
@permission_classes({IsAuthenticated})
def testing(request, *args, **kwargs):
    return Response(data="You are logged in", status=status.HTTP_200_OK)
