from .serializers import *
from .models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.decorators import api_view, permission_classes

# Create your views here.


# test view
@api_view(['GET'])
@permission_classes({IsAuthenticated})
def testing(request, *args, **kwargs):
    return Response(data="You are logged in", status=status.HTTP_200_OK)


# check if user is owner of something
class UserIsOwner(BasePermission):

    def has_permission(self, request, view):
        # Only if the user is authenticated.
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # if the user is same as the user that is updating user info.
        return obj == request.user


# detail of every user
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_object(self, queryset=None, **kwargs):
        item_id = self.kwargs.get('pk')
        return get_object_or_404(User, id=item_id)


# update user details
class UserUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = (UserIsOwner, IsAuthenticated)

    def get(self, request, format=None, **kwargs):
        item_id = self.kwargs.get('pk')
        queryset = User.objects.filter(id=item_id)
        if queryset.exists():
            user = queryset[0]
            self.check_object_permissions(self.request, obj=user)
            return Response(self.serializer_class(user).data, status=status.HTTP_200_OK)
        return Response({'Not Found': 'User does not exists.'}, status=status.HTTP_404_NOT_FOUND)


    def put(self, request, format=None, **kwargs):
        item_id = self.kwargs.get('pk')
        queryset = User.objects.filter(id=item_id)
        if queryset.exists():
            user = queryset[0]
            self.check_object_permissions(self.request, obj=user)
            serializer = UserUpdateSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.data.get('email')
                username = serializer.data.get('username')
                first_name = serializer.data.get('first_name')
                last_name = serializer.data.get('last_name')

                queryset = User.objects.filter(id=item_id)
                if not queryset.exists():
                    return Response({'Not Found': 'User does not exists.'}, status=status.HTTP_404_NOT_FOUND)

                user = queryset[0]
                user.email = email
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.save(update_fields=['email', 'username', 'first_name', 'last_name'])
                return Response(self.serializer_class(user).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Not Found': 'User does not exists.'}, status=status.HTTP_404_NOT_FOUND)

