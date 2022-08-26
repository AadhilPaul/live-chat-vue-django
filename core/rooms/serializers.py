from .models import Room
from accounts.models import User
from rest_framework import serializers

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id')
        # fields = "__all__"

class RoomSerializer(serializers.ModelSerializer):
    member = MemberSerializer(many=True)
    class Meta:
        model = Room
        fields = "__all__"


class RoomUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['code']

