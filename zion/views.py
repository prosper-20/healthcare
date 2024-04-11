from django.shortcuts import render
from .models import Patient
from .serializers import PatientSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

#Endpoints for retrieving all Patients By Admin Users(doctors and nurses) only
class ALLPatients(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request,format=None):
        all_patient = Patient.objects.all()
        serialized_patient = PatientSerializer(all_patient,many=True)
        return Response(serialized_patient.data,status=status.HTTP_200_OK)
    
#Endpoint patient sign up
class PatientSignup(APIView):
    def post(self,request,format=None):
        new_Patient=PatientSerializer(data=request.data)
        new_Patient.is_valid(raise_exception=True)
        new_Patient.save()
        message={"Success":"Patient has been added successfully"}
        return Response(message,status=status.HTTP_201_CREATED)


#Endpoint for a patient to retrieve,Update,Delete their profile
class PatientDetailpage(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request, id, format=None, **kwargs):
        if request.user.username != Patient.objects.get(id=id).name:
            return Response({"Error": "You don't have such permission"})
        try:
            current_patient = Patient.objects.get(id=id)
        except Patient.DoesNotExist:
            return Response({"Error":"Patient not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serialized_patient = PatientSerializer(current_patient, many=False)
        return Response(serialized_patient.data,status=status.HTTP_200_OK)  
    
    def put(self,request, id, format=None, **kwargs):
        if request.user.username != Patient.objects.get(id=id).name:
            return Response({"Error": "You don't have such permission"})
        try:
                current_patient = Patient.objects.get(id=id)
        except Patient.DoesNotExist:
            return Response({"Error":"Patient does not exist"}, status=status.HTTP_404_NOT_FOUND)
        Edit_Patient=PatientSerializer(current_patient,data=request.data,partial=True)
        Edit_Patient.is_valid(raise_exception=True)
        Edit_Patient.save()
        message={"Success":"Patient Updated successfully"}
        return Response(message,status=status.HTTP_202_ACCEPTED)
    
    def delete(self,request, id, format=None, **kwargs):
        if request.user.username != Patient.objects.get(id=id).name:
            return Response({"Error": "You don't have such permission"})
        try:
            current_patient = Patient.objects.get(id=id)
        except Patient.DoesNotExist:
            return Response({"Error":"Patient already deleted"}, status=status.HTTP_404_NOT_FOUND)
        current_patient.delete()
        message={"Success":"Patient Deleted successfully"}
        return Response(message,status=status.HTTP_410_GONE)
