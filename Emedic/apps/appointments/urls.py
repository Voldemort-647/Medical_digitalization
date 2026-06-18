from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet
from . import views

router = DefaultRouter()

router.register(
    r'api',
    views.AppointmentViewSet,
    basename='appointments_api'
)

urlpatterns =[ 
    path('',views.appointment_dashboard, name = 'appoitments_dashboard'),
    path('data/',include (router.urls))
    ]