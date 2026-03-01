from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from django.conf import settings
from django.db import models


from .serializers import TicketSerializer, TicketUpdateSerializer, TicketCreateSerializer
from .models import Ticket

User = settings.AUTH_USER_MODEL

@extend_schema_view(
    list=extend_schema(
        summary="List all tickets",
        description="Get a paginated list of all tickets. Supports filtering by status and priority.",
        parameters=[
            OpenApiParameter(
                name='status',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by ticket status',
                enum=['open', 'in_progress', 'resolved', 'closed']
            ),
            OpenApiParameter(
                name='priority',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by priority level',
                enum=['low', 'medium', 'high', 'critical']
            ),
        ],
        tags=['Tickets'],
    ),
    retrieve=extend_schema(
        summary="Get ticket details",
        description="Retrieve detailed information about a specific ticket.",
        tags=['Tickets'],
    ),
    create=extend_schema(
        summary="Create a new ticket",
        description="Create a new ticket. The authenticated user will be set as the creator.",
        request=TicketCreateSerializer,
        responses={201: TicketSerializer},
        examples=[
            OpenApiExample(
                'Ticket Example',
                value={
                    'title': 'Login button not working',
                    'description': 'The login button on the homepage is unresponsive on mobile devices',
                    'priority': 'high'
                },
                request_only=True,
            )
        ],
        tags=['Tickets'],
    ),
    update=extend_schema(
        summary="Update a ticket",
        description="Update an existing ticket's information.",
        request=TicketUpdateSerializer,
        responses={200: TicketSerializer},
        tags=['Tickets'],
    ),
    partial_update=extend_schema(
        summary="Partially update a ticket",
        description="Update specific fields of a ticket.",
        request=TicketUpdateSerializer,
        responses={200: TicketSerializer},
        tags=['Tickets'],
    ),
    destroy=extend_schema(
        summary="Delete a ticket",
        description="Permanently delete a ticket.",
        tags=['Tickets'],
    ),
)

class TicketsViewset(viewsets.ModelViewSet):
    """ViewSet for managing tickets"""

    permission_classes = [permissions.IsAuthenticated]

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return TicketCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TicketUpdateSerializer
        return TicketSerializer
       
    def get_queryset(self):
        queryset = Ticket.objects.all()

        # Filter by status
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Filter by priority
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @extend_schema(
        summary="Assign ticket to user",
        description="Assign a ticket to a specific user.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'integer', 'description': 'ID of user to assign'}
                },
                'required': ['user_id']
            }
        },
        responses={200: TicketSerializer},
        tags=['Tickets']
    )

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """Assign ticket to a user"""
        ticket = self.get_object()
        user_id = request.data.get('user_id')
        
        from apps.accounts.models import User
        try:
            user = User.objects.get(id=user_id)
            ticket.assigned_to = user
            ticket.save()
            serializer = self.get_serializer(ticket)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        summary="Get my tickets",
        description="Get all tickets created by or assigned to the authenticated user.",
        tags=['Tickets'],
    )
    @action(detail=False, methods=['get'])
    def my_tickets(self, request):
        """Get tickets for current user"""
        tickets = Ticket.objects.filter(
            models.Q(created_by=request.user) | models.Q(assigned_to=request.user)
        ).distinct()
        
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)
