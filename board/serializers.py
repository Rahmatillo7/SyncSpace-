from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Board, Stroke, ChatMessage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class BoardSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner', 'created_at', 'slug', 'is_public']

class StrokeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Stroke
        fields = ['id', 'board', 'user', 'content', 'timestamp']