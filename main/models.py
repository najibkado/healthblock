from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_events")
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User: {self.user.username} | Action: {self.description}"

    def serialize(self):
        return {
            "staff": f"{self.user.first_name} {self.user.last_name}",
            "action": self.description,
            "date": self.created_at.strftime("%b %d %Y %H:%M:%S")
        }

class Departmet(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="staff_details")
    department = models.ForeignKey(Departmet, on_delete=models.CASCADE, related_name="staff_department")
    job = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    is_doctor = models.BooleanField(default=False)
    is_it = models.BooleanField(default=False)
    is_receptionist = models.BooleanField(default=False)
    is_lab = models.BooleanField(default=False)
    is_analyst = models.BooleanField(default=False)
    is_director = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class Patient(models.Model):
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    age = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    telephone = models.CharField(max_length=255, default='')
    next_of_kin_first_name = models.CharField(max_length=255, default='')
    next_of_kin_last_name = models.CharField(max_length=255, default='')
    next_of_kin_address = models.CharField(max_length=255, default='')
    next_of_kin_telephone = models.CharField(max_length=255, default='')
    next_of_kin_relationship = models.CharField(max_length=255, default='')
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Medical_History_Classes(models.Model):
    name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name

class Past_Medical_History(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="patient_medical_history")
    classification  = models.ForeignKey(Medical_History_Classes, on_delete=models.CASCADE, related_name="medical_history_classification")
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.patient.first_name}\'s medical history"

    def serialize(self):
        return {
            "patient": self.patient.id,
            "classification": self.classification.name,
            "description": self.description
        }

class Family_And_Social_History_Classes(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Family_And_Social_History(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="patient_family_and_social_history")
    classification  = models.ForeignKey(Family_And_Social_History_Classes, on_delete=models.CASCADE, related_name="family_and_social_history_classification")
    description = models.CharField(max_length=255)

    def serialize(self):
        return {
            "patient": self.patient.id,
            "classification": self.classification.name,
            "description": self.description
        }


    def __str__(self):
        return f"{self.patient.first_name}\'s social and family history"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="patient_appointment")
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="doctor_appointments")
    is_active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now=True)

class Patient_Monitor(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="patient_monitor")
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor_action_on_patient")
    description = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
            "staff": self.staff.first_name,
            "patient": self.patient.first_name,
            "description": self.description,
            "date": self.date.strftime("%b %d %Y %H:%M:%S")
        }

    def __str__(self):
        return f"{self.patient} activity"

class Investigation_Request(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="patient_investigation_request")
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor_investigation_request_on_patient")
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)

class Financial_Record(models.Model):
    investigation = models.ForeignKey(Investigation_Request, on_delete=models.CASCADE, related_name="item_paid_for")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="patient_payment")
    amount_paid = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)



