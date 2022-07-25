from django.shortcuts import render
from .serializers import RoomSerializer
from django.http import HttpResponse
from .models import Room
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission

# Create your views here.
def testing(request):
  return HttpResponse('<h1>Room testing.</h1>')


# check if user is owner of something
class UserIsOwner(BasePermission):

    def has_permission(self, request, view):
        # Only if the user is authenticated.
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # if the user is same as the user that is updating user info.
        return obj == request.user


class RoomCreateView(generics.CreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None, **kwargs):
        serializer = RoomSerializer(data=request.data)
        try:
          if request.user.room is not None:
            return Response({"Forbidden": "You can have only one room at a time."}, status=status.HTTP_403_FORBIDDEN)
        except BaseException:
          if serializer.is_valid():
            host = request.user
            room = Room(host=host)
            room.save()
            room.member.add(host)
            return Response(self.serializer_class(room).data, status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



