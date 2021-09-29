from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from main.models import Departmet, Family_And_Social_History, Past_Medical_History, Patient, Staff, User, Appointment, Event, Patient_Monitor, Investigation_Request
from .serializers import UserSerializer, PatientSerializer, Family_History_Serializer, Medical_History_Serializer, Appointment_Serializer, Investigation_Request_Serializer, Financial_Record_Serializer
from django.contrib.auth import authenticate, login, logout
from main.healthblockmodule.healthblock import Blockchain
from rest_framework import status 
from main.utils import create_event, create_monitor_patient


# Create your views here.

blockchain = Blockchain()

class Login_View(APIView):

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')

        authenticated_user = authenticate(request, username=username, password=password)

        if authenticated_user is not None:

            serializer = UserSerializer(authenticated_user)
            token = Token.objects.get(user=authenticated_user).key
            create_event(request.user, f'Logged in')
            return Response({ 'user_id': authenticated_user.id, 'user':serializer.data ,'token': token }, status=status.HTTP_200_OK)

            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class Logout_View(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        create_event(request.user, f'Logged out')
        logout(request)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class Mine_Blockchain_View(APIView):

    def get(self, request):
        previous_block = blockchain.get_previous_block()
        previous_nonce = previous_block['nonce']
        nonce = blockchain.proof_of_work(previous_nonce)
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(nonce, previous_hash)
        response = {'message': 'Congratulations, you just mined a block!',
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'nonce': block['nonce'],
                    'previous_hash': block['previous_hash']}   
        return Response(response)

class Get_Blockchain_View(APIView):

    def get(self, request):
        response = {'chain': blockchain.chain,
                    'length': len(blockchain.chain)}
        return Response(response)

class Blockchain_Validity_View(APIView):

    def get(self, request):
        is_valid = blockchain.is_chain_valid(blockchain.chain)
        if is_valid:
            response = {'message': 'All good. The Blockchain is valid.'}
        else:
            response = {'message': 'Dude, we have a problem. The Blockchain is not valid.'}
        return Response(response)

class Patient_View(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        create_event(request.user, f'Viewed patients')
        return Response(serializer.data)

    def post(self, request):
        serializer = PatientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            create_event(request.user, f'Registered a new patient')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Patient_Information(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        
        try:
            patient = Patient.objects.get(pk=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        medical_history = Past_Medical_History.objects.filter(patient=patient)
        family_history = Family_And_Social_History.objects.filter(patient=patient)

        response = {
            "patient": {
                "id": patient.id,
                "name": f"{patient.first_name} {patient.last_name}",
                "age": patient.age,
                "address": patient.address,
                "telephone": patient.telephone,
                "next_of_kin": f"{patient.next_of_kin_first_name} {patient.next_of_kin_last_name}",
                "next_of_kin_telephone": patient.next_of_kin_telephone,
                "next_of_kin_address": patient.next_of_kin_address,
                "next_of_kin_relationship": patient.next_of_kin_relationship,
                "status": 'Admitted' if patient.status else 'Not admitted',
            }
        }

        create_monitor_patient(request.user, patient, f'{patient.first_name} arrived at doctor {request.user.first_name} for appointment')
        create_event(request.user, f'Viewed patient {patient.first_name} Information')

        if medical_history.exists():
            history = [history.serialize() for history in medical_history]
            response['medical_history'] = history
        else:
            response['medical_history'] = []

        if family_history.exists():
            history = [history.serialize() for history in family_history]
            response['family_history'] = history
        else:
            response['family_history'] = []

        return Response(response, status=status.HTTP_200_OK)

class Patient_Medical_History_View(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        
        
        try:
            patient = Patient.objects.get(pk=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        create_monitor_patient(request.user, patient, f'{patient.first_name} arrived at doctor {request.user.first_name} to update past medical history')

        serializer = Medical_History_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            create_event(request.user, f'Registered patient past {patient.first_name} medical history')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Patient_Family_History_View(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        
        try:
            patient = Patient.objects.get(pk=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        create_monitor_patient(request.user, patient, f'{patient.first_name} arrived at doctor {request.user.first_name} to update family and social history')

        serializer = Family_History_Serializer(data=request.data)
        if serializer.is_valid():
            create_event(request.user, f'Registered patient {patient.first_name} social and family history')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Add_Data_View(APIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        received_json = request.data
        transaction_keys = ['patient', 'practicioner', 'meta_data', 'patient_data','time']
        if not all(key in received_json for key in transaction_keys):
            response = {'message': 'missing data'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        patient = Patient.objects.get(pk=int(received_json['patient']))

        if received_json['meta_data'] == "complaint_data":
            create_monitor_patient(request.user, patient, f'{patient.first_name} complaint was recorded by {request.user.first_name}')
            create_event(request.user, f'Registered patient complaint')
        elif received_json['meta_data'] == "treatment_data":
            create_monitor_patient(request.user, patient, f'{patient.first_name} treatment was recorded by {request.user.first_name}')
            create_event(request.user, f'Registered patient treatment')
        elif received_json['meta_data'] == "investigation_data":
            create_monitor_patient(request.user, patient, f'{patient.first_name} investgation was recorded by {request.user.first_name}')
            create_event(request.user, f'Registered patient investigation')
            investigation = received_json['patient_data']['investigation_id']
            try:
                investigation = Investigation_Request.objects.get(pk=int(investigation))
                investigation.is_active = False
                investigation.save()
            except Investigation_Request.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif received_json['meta_data'] == "exam_data":
            create_monitor_patient(request.user, patient, f'{patient.first_name} clinical exam was recorded by {request.user.first_name}')
            create_event(request.user, f'Registered patient clinical examiniation')
        elif received_json['meta_data'] == "finance_data":
            create_monitor_patient(request.user, patient, f'{patient.first_name} financial data was recorded by {request.user.first_name}')
            create_event(request.user, f'Registered patient finance data')

        index = blockchain.add_data(received_json['patient'], received_json['practicioner'], received_json['meta_data'], received_json['patient_data'], received_json['time'])
        response = {'message': f'This data will be added to Block {index}'}
        return Response(response, status=status.HTTP_201_CREATED)

class Connect_Node_View(APIView):

    def post(self, request):
        received_json = request.data
        nodes = received_json.get('nodes', '')
        if nodes is None:
            response = {'message': 'missing node'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        for node in nodes:
            blockchain.add_node(node)
        response = {
            'message': 'All the nodes are now connected. The Healthblock Blockchain now contains the following nodes:',
            'total_nodes': list(blockchain.nodes)
            }
        return Response(response, status=status.HTTP_200_OK)

class Replace_Chain_View(APIView):

    def get(self, request):
        is_chain_replaced = blockchain.replace_chain()
        if is_chain_replaced:
            response = {
                'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                'new_chain': blockchain.chain
                }
        else:
            response = {
                'message': 'All good. The chain is the largest one.',        
                'actual_chain': blockchain.chain
                }
        return Response(response, status=status.HTTP_200_OK)


class Summary_View(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        staff = Staff.objects.get(user=request.user)
        department = staff.department
        patients = Patient.objects.filter(status=True)


        response = {
            "name": f"{staff.user.first_name} {staff.user.last_name}",
            "job": staff.job,
            "is_doctor": staff.is_doctor,
            "department": {
                "name": department.name,
                "description": department.description,
                },
            "patients_count": len(patients)
            }
        
        create_event(request.user, f'Staff summary')

        return Response(response, status=status.HTTP_200_OK)

class Appointment_View(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        appointments = Appointment.objects.filter(is_active=True)
        serializer = Appointment_Serializer(appointments, many=True)
        create_event(request.user, f'Viewed patients with appointment')
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = Appointment_Serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            patient = Patient.objects.get(pk=serializer.data.get('patient', ''))
            create_monitor_patient(request.user, patient, f'{patient.first_name} arrived at reception to book for an appointment by {request.user.first_name}')
            create_event(request.user, f'Registered appointment')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Patient_Appointment(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        appointments = Appointment.objects.filter(is_active=True)
        data = {
            "appoinmtents": [{
                "id": appointment.patient.id, 
                "name": appointment.patient.first_name,
                "status": "Admitted" if appointment.patient.status else "Not addmited",
                } for appointment in appointments]
        }
        create_event(request.user, f'Viewed patients with appointments')
        return Response(data, status=status.HTTP_200_OK)

class Event_View(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Event.objects.all()
        response = {
            "events":[event.serialize() for event in events]
        }
        create_event(request.user, f'Viewed staff logs with mobile app')
        return Response(response, status=status.HTTP_200_OK)

class Patient_Report(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        create_event(request.user, f'Viewed patient {id} report history')

        try:
            patient = Patient.objects.get(pk=id)
        except Patient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        medical_history = Past_Medical_History.objects.filter(patient=patient)
        family_history = Family_And_Social_History.objects.filter(patient=patient)
        patient_activites = Patient_Monitor.objects.filter(patient=patient)

        response = {
            "patient": {
                "id": patient.id,
                "name": f"{patient.first_name} {patient.last_name}",
                "age": patient.age,
                "address": patient.address,
                "telephone": patient.telephone,
                "next_of_kin": f"{patient.next_of_kin_first_name} {patient.next_of_kin_last_name}",
                "next_of_kin_telephone": patient.next_of_kin_telephone,
                "next_of_kin_address": patient.next_of_kin_address,
                "next_of_kin_relationship": patient.next_of_kin_relationship,
                "status": 'Admitted' if patient.status else 'Not admitted',
            }
        }

        create_event(request.user, f'Viewed patient {patient.first_name} report history')
        create_monitor_patient(request.user, patient, f'{patient.first_name} report has been viewed')

        if medical_history.exists():
            history = [history.serialize() for history in medical_history]
            response['medical_history'] = history
        else:
            response['medical_history'] = []

        if family_history.exists():
            history = [history.serialize() for history in family_history]
            response['family_history'] = history
        else:
            response['family_history'] = []

        if patient_activites.exists():
            activites = [activity.serialize() for activity in patient_activites]
            response['patient_activites'] = activites
        else:
            response['patient_activites'] = []

        patient_block_data = blockchain.get_patient_data(id)

        response['treatment_data'] = [
            {
            "patient": 1,
            "doctor": 1,
            "hdata_type": "treatment_data",
            "title": "sample title",
            "description": "sample description",
            "date": "10:12:20:10"
            },
            {
            "patient": 1,
            "doctor": 1,
            "hdata_type": "treatment_data",
            "title": "sample title",
            "description": "sample description",
            "date": "10:12:20:10"
            }
        ]
        response['complaint_data'] = [
            {
            "patient": 1,
            "doctor": 1,
            "hdata_type": "complaint_data",
            "title": "sample title",
            "description": "sample description",
            "date": "10:12:20:10"
            }
        ]
        response['exam_data'] = [
            {
            "patient": 1,
            "doctor": 1,
            "hdata_type": "exam_data",
            "title": "sample title",
            "description": "sample description",
            "date": "10:12:20:10",
            "diagnosis": [{
                "hdata_type": "diagnosis_data",
                "description": "sample description",
                "date": "10:12:20:10"
                }]
            }
        ]
        response['investigation_data'] = [
            {
            "patient": 1,
            "doctor": 1,
            "hdata_type": "investigation_data",
            "title": "sample title",
            "description": "sample description",
            "date": "10:12:20:10"
            }
        ]

        for data in patient_block_data:
            if data['hdata_type'] == 'treatment_data':
                response['treatment_data'].append(data)
            elif data['hdata_type'] == 'complaint_data':
                response['complaint_data'].append(data)
            elif data['hdata_type'] == 'exam_data':
                response['exam_data'].append(data)
            elif data['hdata_type'] == 'investigation_data':
                response['investigation_data'].append(data)

        return Response(response, status=status.HTTP_200_OK)

        data = {
            "patient": 1,
            "doctor": 1,
            "hdata_type": "",
            "title": "sample title",
            "description": "sample description",
            "data": "10:12:20:10"
        }


class Investgation_Request_View(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requests = Investigation_Request.objects.filter(is_active=True)
        serializer = Investigation_Request_Serializer(requests, many=True)
        create_event(request.user, f'Viewed active investgation requests')
        #create_monitor_patient(request.user, patient, f'{patient.first_name} report has been viewed')
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = Investigation_Request_Serializer(data=request.data)
        try:
            patient = Patient.objects.get(pk=request.data.get('patient', ''))
        except Patient.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            create_event(request.user, f'request for investgation on patient')
            create_monitor_patient(request.user, patient, f'{patient.first_name} report has been viewed')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        create_event(request.user, f'Tried to request for patient investigation')
        return Response(status=status.HTTP_400_BAD_REQUEST)

class Complaints_View(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        
        data = blockchain.get_patient_data(id)
        complaints = []

        for item in data:
            if item['hdata_type'] == 'complaint_data':
                complaints.append(item)

        response = {
            "complaints": complaints
        }

        return Response(response, status=status.HTTP_200_OK)

class Treatments_View(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        
        data = blockchain.get_patient_data(id)
        treatments = []
        investigations = []
        exams = []

        for item in data:
            if item['hdata_type'] == 'treatment_data':
                treatments.append(item)
            elif item['hdata_type'] == 'exam_data':
                exams.append(item)
            elif item['hdata_type'] == 'investigation_data':
                investigations.append(item)
            else:
                pass

        response = {
            "treatments": treatments,
            "exams": exams,
            "investigations": investigations
        }

        return Response(response, status=status.HTTP_200_OK)

class Finance_Request_View(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requests = Investigation_Request.objects.filter(is_paid=False)
        serializer = Investigation_Request_Serializer(requests, many=True)
        create_event(request.user, f'Viewed active payment requests')
        #create_monitor_patient(request.user, patient, f'{patient.first_name} report has been viewed')
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = Financial_Record_Serializer(data=request.data)

        try:
            patient = Patient.objects.get(pk=request.data.get('patient', ''))
        except Patient.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try: 
            investigation = Investigation_Request.objects.get(pk=request.data.get('investigation', ''))
        except Investigation_Request.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


        if serializer.is_valid():
            serializer.save()
            investigation.is_paid = True
            investigation.save()
            create_event(request.user, f'recorded patient {patient.first_name} payment')
            create_monitor_patient(request.user, patient, f'{patient.first_name} paid for investigation')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        create_event(request.user, f'tried to record patient payment')
        return Response(status=status.HTTP_400_BAD_REQUEST)

class Update_Appointment_View(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        appointment = Appointment.objects.get(pk=id)
        appointment.is_active = False
        appointment.save()
        return Response(status=status.HTTP_200_OK)


        
