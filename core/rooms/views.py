from django.shortcuts import render, get_object_or_404, get_list_or_404
import json
from accounts.models import User
from accounts.serializers import UserSerializer
from django.conf import settings
from .serializers import MemberSerializer, RoomSerializer
from django.http import HttpResponse
from .models import Room
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny

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
        return obj.host == request.user


class AllRoomView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]
    models = Room

    def get_queryset(self):
        return get_list_or_404(Room)


class RoomDetailView(generics.RetrieveAPIView):
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]

    def get_object(self, queryset=None, **kwargs):
        room_code = self.kwargs.get('code')
        return get_object_or_404(Room, code=room_code)


class IfInRoom(generics.RetrieveAPIView):
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]

    def get(self, request, format=None, **kwargs):
        rooms = Room.objects.all()
        for room in rooms:
            for member in room.member.all():
                if request.user.username == member.username:
                    room_code = room.code
                    your_room = Room.objects.filter(code=room_code).first()
                    return Response(self.serializer_class(your_room).data, status=status.HTTP_200_OK)
        return Response({"False": "Not in Room"}, status=status.HTTP_204_NO_CONTENT)


class RoomCreateView(generics.CreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None, **kwargs):
        serializer = RoomSerializer(data=request.data)
        rooms = Room.objects.all()
        for room in rooms:
            for member in room.member.all():
                if request.user.username == member.username:
                    return Response({"Forbidden": "You are already in a room"}, status=status.HTTP_403_FORBIDDEN)
                
        if serializer.is_valid():
            host = request.user
            room = Room(host=host)
            room.save()
            room.member.add(host)
            return Response(self.serializer_class(room).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class RoomJoinView(generics.RetrieveUpdateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None, **kwargs):
        room_code = self.kwargs.get('code')
        return get_object_or_404(Room, code=room_code)

    def put(self, request, format=None, **kwargs):
        room_code = self.kwargs.get('code')
        rooms = Room.objects.all()
        for room in rooms:
            for member in room.member.all():
                if request.user.username == member.username:
                    return Response({"Forbidden": "You are already in a room"}, status=status.HTTP_403_FORBIDDEN)
                
        queryset = Room.objects.filter(code=room_code)
        if queryset.exists():
            room = queryset[0]
            room.member.add(request.user)
            return Response(self.serializer_class(room).data, status=status.HTTP_200_OK)
        return Response({'Not Found': 'Room does not exists'}, status=status.HTTP_404_NOT_FOUND)

class RoomLeaveView(generics.RetrieveUpdateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None, **kwargs):
        room_code = self.kwargs.get('code')
        return get_object_or_404(Room, code=room_code)

    def put(self, request, format=None, **kwargs):
        room_code = self.kwargs.get('code')
        queryset = Room.objects.filter(code=room_code)
        if queryset.exists():
            room = queryset[0]
            room_serialized = RoomSerializer(room).data
            members_in_room = room_serialized['member']
            if request.user.id in members_in_room:
                # if last user leaves room room is deleted.
                if len(members_in_room) == 1:
                    room.delete()
                room.member.remove(request.user)
                return Response(self.serializer_class(room).data, status=status.HTTP_200_OK)
            return Response({"Forbidden": "You are not in this room."}, status=status.HTTP_403_FORBIDDEN)
        return Response({'Not Found': 'Room does not exists'}, status=status.HTTP_404_NOT_FOUND)


class RoomKickUser(generics.RetrieveUpdateAPIView):
    serializer_class = RoomSerializer
    permission_classes = (UserIsOwner, IsAuthenticated)

    def get_object(self, queryset=None, **kwargs):
        room_code = self.kwargs.get('code')
        return get_object_or_404(Room, code=room_code)

    def put(self, request, format=None, **kwargs):
        room_code = self.kwargs.get('code')
        user_id = self.kwargs.get('id')
        user_queryset = User.objects.filter(id=user_id)
        room_queryset = Room.objects.filter(code=room_code)

        if user_queryset.exists() and room_queryset.exists():
            user = user_queryset[0]
            room = room_queryset[0]
            room_serialized = RoomSerializer(room).data
            eggs = MemberSerializer(room_serialized['member'], many=True).data
            self.check_object_permissions(self.request, obj=room)

            # if owner of room tries to kick himself.
            if user_id == request.user.id:
                return Response(
                    {'Forbidden': 'You cannot kick yourself from your room'}, status=status.HTTP_403_FORBIDDEN)

            # check if user is in the room.
            spam = json.dumps(eggs)
            json_object = json.loads(spam)
            members_in_room = []
            for usr in json_object:
                members_in_room.append(usr['id'])
            if user_id in members_in_room:
                room.member.remove(user)
                return Response(self.serializer_class(room).data, status=status.HTTP_200_OK)
            return Response({"Not In Room": "This User is not in this room"}, status=status.HTTP_403_FORBIDDEN)
        return Response({'Not Found': 'Room or User does not exists.'}, status=status.HTTP_404_NOT_FOUND)
