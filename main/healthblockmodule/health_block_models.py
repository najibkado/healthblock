

class Staff:
    pass

class Patient:
    pass

class Address:
    pass

class Treatment:
    def __init__(self, patient, treatment, doctor):
        self.patient = patient
        self.treatment = treatment
        self.doctor = doctor

    def get(self):
        return {
            "patient": self.patient,
            "treatment": self.treatment,
            "doctor": self.doctor
        }


class Investigation:
    def __init__(self, investigation, patient, doctor, lab_technician, is_diagnosed, diagnosis):
        self.investigation = investigation
        self.patient = patient
        self.doctor = doctor
        self.lab_technician = lab_technician
        self.is_diagnosed = is_diagnosed
        self.diagnosis = diagnosis

    def get(self):
        return {
            "patient": self.patient,
            "investigation": self.investigation,
            "doctor": self.doctor,
            "lab_technician": self.lab_technician,
            "is_diagnosed": self.is_diagnosed,
            "diagnosis": self.diagnosis
        }

class Complaint:
    def __init__(self, title, description, doctor, patient):
        self.title = title
        self.description = description
        self.doctor = doctor
        self.patient = patient

    def get(self):
        return {
            "patient": self.patient,
            "title": self.title,
            "description": self.description,
            "doctor": self.doctor
        }
        



