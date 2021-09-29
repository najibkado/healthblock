from .models import User, Patient, Staff

class Helper:

    def verify_patient(self, id):
        try:
            verified_patient = Patient.objects.get(pk=id)
        except Patient.DoesNotExist:
            return False
        return True

    def verify_doctor(self, id):
        try:
            verified_doctor = Staff.objects.get(pk=id)
        except Staff.DoesNotExist:
            return False
        return True