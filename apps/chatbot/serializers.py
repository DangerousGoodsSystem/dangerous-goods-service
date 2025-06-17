from rest_framework import serializers
from .models import Conversation, Message

class ChatRequestSerializer(serializers.Serializer):
    """Serializer cho request chat"""
    thread_id = serializers.CharField(required=True)
    message = serializers.CharField(max_length=2000)
    
    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty.")
        return value.strip()

class ChatResponseSerializer(serializers.Serializer):
    """Serializer cho response chat"""
    response = serializers.CharField()

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content', 'is_user', 'timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ['id', 'thread_id', 'user_id', 'created_at', 'messages']

class ConversationListSerializer(serializers.ModelSerializer):
    first_user_message = serializers.CharField(read_only=True)
    class Meta:
        model = Conversation
        fields = ['id', 'first_user_message', 'created_at']