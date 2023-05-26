from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from appointments.models import Appointment
from authentication.models import User
from authentication.serializers import UserSerializer

from .serializers import AppointmentSerializer

from authentication.permissions import IsEmployee

# Create your views here.

class AppointmentsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmployee]
    
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        appointments = request.user.employee.all()

        if serializer.validated_data['start'] > serializer.validated_data['end']:
            return Response(status.HTTP_400_BAD_REQUEST)

        for app in appointments:
            if serializer.validated_data['start'] < app.end or serializer.validated_data['end'] < app.start:
                return Response(status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(status.HTTP_201_CREATED)

    def get(self, request):
        appointments = request.user.patient.all()

        response = Response()

        response.data = {}

        response.data['details'] = []

        for app in appointments:
            response.data['details'].append(AppointmentSerializer(app).data)
        
        response.status_code = 200

        return response
    
    def put(self, request):
        data = request.data
        appointment = Appointment.objects.get(id=data['requested_id'])

        serializer = AppointmentSerializer(appointment)

        try:
            serializer.update(appointment, validated_data=data)
            return Response(status.HTTP_202_ACCEPTED)
        except:
            return Response(status.HTTP_409_CONFLICT)

    def delete(self, request):
        appointment = Appointment.objects.get(id=request.data['appointment_id'])
        appointment.delete()

        return Response(status.HTTP_200_OK)
    
class GetAllDoctorsAPIView(APIView):
    def get(self, request):
        doctor_list = User.objects.filter(groups__name='Employee')
        data = []
        for doctor in doctor_list:
            data.append(self.get_user_json(doctor))
        return Response(data=data)
    
    def get_user_json(self, user):
        data = {}
        raw = UserSerializer(user).data
        data['is_employee'] = user.groups.filter(name='Employee').exists()
        data['id'] = raw['id']
        data['first_name'] = raw['first_name']
        data['last_name'] = raw['last_name']
        data['age'] = raw['age']
        data['phone_number'] = raw['phone_number']
        data['is_employee'] = raw['is_employee']
        data['email'] = raw['email']
        data['gender'] = raw['gender']
        return data