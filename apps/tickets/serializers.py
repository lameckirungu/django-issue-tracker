from rest_framework import serializers
from .models import Ticket
from apps.accounts.serializers import UserSerializer

class TicketSerializer(serializers.ModelSerializer):
    """Serializer fot Ticket model"""
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']


class TicketCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tickets"""

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority']

class TicketUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating tickets"""
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'status', 'priority', 'assigned_to']