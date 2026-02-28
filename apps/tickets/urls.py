from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import TicketsViewset


router = DefaultRouter()
router.register(r'api/tickets', TicketsViewset, basename="tickets")

urlpatterns = [

]
urlpatterns += router.urls