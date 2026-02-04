from django.urls import path
from .views import *



urlpatterns = [

    # Authentication
   
    path('dashboard/', dashboard, name="dashboard"),
    path('loginPage/', loginPage, name="loginPage"),
    path('', registration, name="registration"),
    path('logout/', logout, name="logout"),
    path('Changepassword/', changepassword, name="changepassword"),

    # =====================
    # Department
    # =====================
    path('department_list/', department_list, name="department_list"),
    path('add_department/', add_department, name="add_department"),
    path('edit_department/<int:id>/', edit_department, name="edit_department"),
    path('delete_department/<int:id>/', delete_department, name="delete_department"),
    path('view_department/<int:id>/', view_department, name="view_department"),

    # department → doctor (required)
    
    path('department_doctor_list/<int:id>/', department_doctor_list, name="department_doctor_list"),


    # Doctor
   
    path('doctor_list/', doctor_list, name="doctor_list"),
    path('add_doctor/', add_doctor, name="add_doctor"),
    path('edit_doctor/<int:id>/', edit_doctor, name="edit_doctor"),
    path('delete_doctor/<int:id>/', delete_doctor, name="delete_doctor"),

    # doctor → patient (required + bonus)
    
    path('doctor_patient_list/<int:id>/', doctor_patient_list, name="doctor_patient_list"),
    path('doctor_profile/<int:id>/', doctor_profile, name="doctor_profile"),

   
    # Patient
 
    path('patient_list/', patient_list, name="patient_list"),
    path('add_patient/', add_patient, name="add_patient"),
    path('edit_patient/<int:id>/', edit_patient, name="edit_patient"),
    path('delete_patient/<int:id>/', delete_patient, name="delete_patient"),

    # patient → appointment (required)
    
    path('patient_appointment_list/<int:id>/', patient_appointment_list, name="patient_appointment_list"),

    # Appointment
  
    path('appointment_list/', appointment_list, name="appointment_list"),
    path('add_appointment/', add_appointment, name="add_appointment"),
    path('edit_appointment/<int:id>/', edit_appointment, name="edit_appointment"),
    path('delete_appointment/<int:id>/', delete_appointment, name="delete_appointment"),
]
















# urlpatterns = [
#     path('dashboard/', dashboard, name="dashboard" ),
#     path('loginPage/', loginPage, name="loginPage" ),
#     path('', registration, name="registration" ),
#     path('logout/', logout, name="logout" ),
#     path('Changepassword/', changepassword, name="changepassword" ),

#     path('department_list/',department_list, name="department_list" ),
#     path('add_department/', add_department, name="add_department" ),
#     path('edit_department/<int:id>/', edit_department, name="edit_department" ),
#     path('delete_department/<int:id>/', delete_department, name="delete_department" ),
#     path('view_department/<int:id>/', view_department, name="view_department" ),  

#     path('doctor_list/',doctor_list, name="doctor_list" ),
#     path('add_doctor/', add_doctor, name="add_doctor" ),
#     path('edit_doctor/<int:id>/', edit_doctor, name="edit_doctor" ),
#     path('delete_department/<int:id>/', delete_department, name="delete_department" ),
#     path('view_department/<int:id>/', view_department, name="view_department" ),


#     path('patient_list/',patient_list, name="patient_list" ),

#     path('appointment_list/',appointment_list, name="appointment_list" ),


    

# ] 


