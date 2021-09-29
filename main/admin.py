from django.contrib import admin
from .models import User, Event, Staff, Patient, Departmet, Family_And_Social_History, Family_And_Social_History_Classes, Medical_History_Classes, Past_Medical_History, Patient_Monitor, Investigation_Request

# Register your models here.

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Staff)
admin.site.register(Patient)
admin.site.register(Departmet)
admin.site.register(Family_And_Social_History_Classes)
admin.site.register(Family_And_Social_History)
admin.site.register(Past_Medical_History)
admin.site.register(Medical_History_Classes)
admin.site.register(Patient_Monitor)
admin.site.register(Investigation_Request)