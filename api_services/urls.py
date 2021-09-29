from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('accounts/login/', views.Login_View.as_view()),
    path('accounts/logout/', views.Logout_View.as_view()),
    path('mine', views.Mine_Blockchain_View.as_view()),
    path('chain', views.Get_Blockchain_View.as_view()),
    path('validity', views.Blockchain_Validity_View.as_view()),
    path('patients', views.Patient_View.as_view()),
    path('patients/information/<int:id>', views.Patient_Information.as_view()),
    path('add_data', views.Add_Data_View.as_view()),
    path('connect_node', views.Connect_Node_View.as_view()),
    path('replace_chain', views.Replace_Chain_View.as_view()),
    path('summary', views.Summary_View.as_view()),
    path('appointment', views.Appointment_View.as_view()),
    path('appointment/information', views.Patient_Appointment.as_view()),
    path('patients/family-history/<int:id>', views.Patient_Family_History_View.as_view()),
    path('patients/social-history/<int:id>', views.Patient_Medical_History_View.as_view()),
    path('staff/events', views.Event_View.as_view()),
    path('patients/reports/<int:id>', views.Patient_Report.as_view()),
    path('patients/investigation', views.Investgation_Request_View.as_view()),
    path('patients/<int:id>/complaints', views.Complaints_View.as_view()),
    path('patients/finance', views.Finance_Request_View.as_view()),
    path('patients/<int:id>/treatments', views.Treatments_View.as_view()),
    path('appointment/update/<int:id>', views.Appointment_View.as_view()),
]