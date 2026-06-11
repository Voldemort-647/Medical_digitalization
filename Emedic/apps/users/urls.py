from django.urls import path
from . import views


urlpatterns=[
    path('add',views.add_data),
    path('display',views.display_data)
]