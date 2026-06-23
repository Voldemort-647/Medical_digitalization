from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet
from . import views

router = DefaultRouter()

router.register(
    r'api',
    views.AppointmentViewSet,
    basename='appointments_api',
)
router.register(
    r'booking',
    views.BookingViewSet,
    basename='booking'
)

urlpatterns =[ 
    path('',views.appointment_dashboard, name = 'appointments_dashboard'),
    path('book/<int:doctor_id>/',views.patientbooking,name='book_appointment'),
    path('booking/<int:doctor_id>/', views.BookingViewSet.as_view({'post': 'create'}),name='booking_create'),
    path( "receptionist/", views.receptionist_dashboard,name="receptionist_dashboard"),
    path( "approve/<int:appointment_id>/", views.update_appointment_status,name="update_appointment_status"),
    path('data/',include (router.urls))
    ]