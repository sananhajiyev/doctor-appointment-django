from django.urls import path

from . import views

urlpatterns = [
    path('crud/', views.AppointmentsAPIView.as_view(), name='appointments'),
    path('getAllDoctors/', views.GetAllDoctorsAPIView.as_view(), name='appointments'),
]