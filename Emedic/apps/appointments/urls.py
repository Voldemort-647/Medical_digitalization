from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet
from . import views
router = DefaultRouter()

router.register(
    r'',
    views.AppointmentViewSet,
    basename='appointments'
)

urlpatterns = [
    path('history/<int:pk>',views.patientHistory),
    path('display',views.display),
    path('add',views.add)

    # path(
    #      'today/',
    #      views.AppointmentsToday.as_view(),
    #      name='appointment_list'
    #     ),

    #  path(
    #      'doctor/me/',
    #      views.AppoinmentsByDoctor.as_view(),
    #      name='appointments_by_doctor'
    #  ),

    #  path(
    #      'create/',
    #      views.AppointmentsCreate.as_view(),
    #      name='appointment_create'
    #  ),

    #  path(
    #      'detail/<int:pk>/',
    #      views.AppointmentsDetail.as_view(),
    #      name='appointment_detail'
    #  ),

    #  path(
    #      'update/<int:pk>/',
    #      views.AppointmentsUpdate.as_view(),
    #      name='appointment_update'
    #  ),

    #  path(
    #     'cancel/<int:pk>/',
    #      views.AppointmentCancel.as_view(),
    #      name='appointment_cancel'
    #  ),
     
]