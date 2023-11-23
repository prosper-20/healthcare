from django.urls import path
from .views import ALLPatients,PatientDetailpage,PatientSignup

urlpatterns = [
    path("all_patient/", ALLPatients.as_view(), name="home"),
    path("register/", PatientSignup.as_view(), name="signup"),
    path("<uuid:id>/", PatientDetailpage.as_view(), name="patient")
]