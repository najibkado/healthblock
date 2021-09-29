from main.models import User, Patient, Past_Medical_History, Family_And_Social_History, Appointment, Investigation_Request, Financial_Record
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id',
            'first_name',
            'last_name',
            'age',
            'address',
            'telephone',
            'next_of_kin_first_name',
            'next_of_kin_last_name',
            'next_of_kin_address',
            'next_of_kin_telephone',
            'next_of_kin_relationship',
            'status'
        ]

class Family_History_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Family_And_Social_History
        fields = [
            'patient',
            'classification',
            'description'
        ]

class Medical_History_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Past_Medical_History
        fields = [
            'patient',
            'classification',
            'description'
        ]

class Appointment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'patient',
            'doctor',
        ]

class Investigation_Request_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Investigation_Request
        fields = [
            'id',
            'patient',
            'staff',
            'description',
            'is_paid',
        ]

class Financial_Record_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Financial_Record
        fields = [
            'investigation',
            'patient',
            'amount_paid'
        ]