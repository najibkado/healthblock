from .models import Event, Patient_Monitor

def create_event(user, note):
    try:
        event = Event(
            user=user,
            description=note
        )
        event.save()
    except:
        pass

def create_monitor_patient(user, patient, note):
    try:
        monitor = Patient_Monitor(
            patient=patient,
            staff=user,
            description=note
        )
        monitor.save()
    except:
        pass
