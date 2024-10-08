from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import User

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name',)

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = "__all__"


