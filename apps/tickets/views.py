from rest_framework import viewsets, views, generics, authentication
from rest_framework import permissions
from django.conf import settings

from .serializers import TicketSerializer
from .models import Ticket

User = settings.AUTH_USER_MODEL

class TicketsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
       
        