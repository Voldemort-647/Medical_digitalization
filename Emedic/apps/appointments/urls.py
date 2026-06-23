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

urlpatterns = [ 
    path('',views.appointment_dashboard, name = 'appointments_dashboard'),
    path('book/<int:doctor_id>/',views.patientbooking,name='book_appointment'),
    path('booking/<int:doctor_id>/', views.BookingViewSet.as_view({'post': 'create'}),name='booking_create'),
    path( "receptionist/", views.receptionist_dashboard,name="receptionist_dashboard"),
    path( "approve/<int:appointment_id>/", views.update_appointment_status,name="update_appointment_status"),
    path('history/<int:pk>',views.patientHistory),
    path('display',views.display),
    path('add',views.add),

    path(
         'today/',
         views.AppointmentsToday.as_view(),
         name='appointment_list'
        ),

     path(
         'doctor/me/',
         views.AppoinmentsByDoctor.as_view(),
         name='appointments_by_doctor'
     ),

     path(
         'create/',
         views.AppointmentsCreate.as_view(),
         name='appointment_create'
     ),

     path(
         'detail/<int:pk>/',
         views.AppointmentsDetail.as_view(),
         name='appointment_detail'
     ),

     path(
         'update/<int:pk>/',
         views.AppointmentsUpdate.as_view(),
         name='appointment_update'
     ),

     path(
        'cancel/<int:pk>/',
         views.AppointmentCancel.as_view(),
         name='appointment_cancel'
     ),
    
    path('',views.appointment_dashboard, name = 'appoitments_dashboard'),
    path('data/',include (router.urls))
    ]
