from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TicketsViewset


router = DefaultRouter()
router.register(r'', TicketsViewset, basename="ticket")

urlpatterns = [
    path('', include(router.urls))
]