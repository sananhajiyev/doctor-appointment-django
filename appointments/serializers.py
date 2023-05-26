from rest_framework import serializers

from appointments.models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def create(self, validated_data):
        appointment = Appointment.objects.create(
            title = validated_data['title'],
            start = validated_data['start'],
            end = validated_data['end'],
            employee_id = validated_data['employee_id'],
            patient_id = validated_data['patient_id'],
        )
        return appointment