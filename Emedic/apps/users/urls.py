from django.urls import path
from . import views


urlpatterns=[
    path('add',views.add_data),
    path('display',views.display_data),
    path('modify/<int:pk>/',views.modify_data),
    path('dashboard/<int:pk>/',views.dshbrd),
    path('dashboard/html/',views.htmltest)
]