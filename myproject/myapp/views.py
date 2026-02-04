from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import *

# Create your views here.


@login_required
def dashboard(request):
    context = {
        'department_count': Department.objects.count(),
        'doctor_count': Doctor.objects.count(),
        'patient_count': Patient.objects.count(),
        'appointment_count': Appointment.objects.count(),
    }
    return render(request, 'dashboard.html', context)

# It's dashboard for dynamic dashboard where doctors,departments,etc count their number automatically.


# @login_required
# def dashboard(request):
#     return render(request, 'dashboard.html')

def registration(request):
    if request.method == "POST":

        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('Confirm_Password')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists!')
            return redirect('registration')

        if password == confirm_password:
            CustomUser.objects.create_user(
                full_name=full_name,
                username=username,
                email=email,
                password=password,
                user_types='user_types',
            )
            messages.success(request, "Account created successfully!")
            return redirect('loginpage')
    return render(request, 'auth/registration.html')


# def registration(request):
#     if request.method == "POST":
#         full_name = request.POST.get('full_name')
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('Confirm_Password')
#         user_type = request.POST.get('user_type')  # form থেকে user type নেওয়া

#         # username check
#         if CustomUser.objects.filter(username=username).exists():
#             messages.warning(request, 'Username already exists!')
#             return redirect('registration')

#         # password check
#         if password != confirm_password:
#             messages.warning(request, 'Passwords do not match!')
#             return redirect('registration')

#         # user create
#         user = CustomUser.objects.create_user(
#             full_name=full_name,
#             username=username,
#             email=email,
#             password=password,
#             user_types=user_type
#         )

#         # Doctor বা Patient table এ entry
#         if user_type == 'Doctor':
#             Doctor.objects.create(user=user, name=full_name)
#         elif user_type == 'Patient':
#             Patient.objects.create(user=user, name=full_name)

#         messages.success(request, "Account created successfully!")
#         return redirect('loginpage')

#     return render(request, 'auth/registration.html')


def loginpage(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.warning(request, 'Invalid credentials!')
    return render(request, 'auth/loginpage.html')


@login_required
def logoutpage(request):
    logout(request)
    return redirect('loginpage')


@login_required
def changepassword(request):
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if check_password(old_password, request.user.password):
            if new_password == confirm_password:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Succesfully Changed password")
                return redirect('dashboard')
    return render(request, "auth/changepassword.html")


@login_required
def department_list(request):
    Dept = Department.objects.all()
    return render(request, 'department/department_list.html', {'Dept': Dept})


@login_required
def add_department(request):
    if request.method == "POST":
        
        Department.objects.create(
            name=request.POST.get('name'),
            location=request.POST.get('location')
        )
        return redirect('department_list')
    return render(request, 'department/add_department.html')


@login_required
def edit_department(request, id):
    dept = Department.objects.get(id=id)
    if request.method == "POST":
        dept.name = request.POST.get('name')
        dept.location = request.POST.get('location')
        dept.save()
        return redirect('department_list')
    return render(request, 'department/edit_department.html', {'Dept': dept})


@login_required
def delete_department(request, id):
    Department.objects.get(id=id).delete()
    return redirect('department_list')


@login_required
def view_department(request, id):
    dept = Department.objects.get(id=id)
    return render(request, 'department/view_department.html', {'Dept': dept})


@login_required
def doctor_list(request):
    doc = Doctor.objects.all()
    return render(request, 'doctor/doctor_list.html', {'doc': doc})


# @login_required
# def doctor_list(request):
#     if request.user.user_types == "Admin":
#         doctors = Doctor.objects.all()
#     elif request.user.user_types == "Doctor":
#         doctors = Doctor.objects.filter(user=request.user)
#     else:  # Patient
#         doctors = Doctor.objects.all()  # patient can view all doctors
#     return render(request, 'doctor/doctor_list.html', {'doc': doctors})


@login_required
def add_doctor(request):
    dept = Department.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        specialization = request.POST.get('specialization')
        department_id = request.POST.get('department')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        username = request.POST.get('username')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, "Doctor already exists!")
            return redirect('add_doctor')

        department = Department.objects.get(id=department_id)

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password="1234",   # for 🔒 fixed password
            user_types="Doctor"
        )

        Doctor.objects.create(
            user=user,
            name=name,
            specialization=specialization,
            phone=phone,
            email=email,
            department=department
        )

        return redirect('doctor_list')

    return render(request, 'doctor/add_doctor.html', {'dept': dept})


@login_required
def edit_doctor(request, id):
    doc = Doctor.objects.get(id=id)
    dept = Department.objects.all()

    if request.method == "POST":
        doc.name = request.POST.get('name')
        doc.specialization = request.POST.get('specialization')
        doc.department = Department.objects.get(
            id=request.POST.get('department'))
        doc.phone = request.POST.get('phone')
        doc.save()
        return redirect('doctor_list')

    return render(request, 'doctor/edit_doctor.html', {
        'doc': doc,
        'dept': dept
    })


@login_required
def delete_doctor(request, id):
    Doctor.objects.get(id=id).delete()
    return redirect('doctor_list')


@login_required
def patient_list(request):
    Pat = Patient.objects.all()
    return render(request, 'patient/patient_list.html', {'Pat': Pat})


# @login_required
# def patient_list(request):
#     if request.user.user_types == "Admin":
#         patients = Patient.objects.all()

#     elif request.user.user_types == "Doctor":
#         doctor = Doctor.objects.get(user=request.user)
#         patients = Patient.objects.filter(doctor=doctor)

#     else:  # Patient
#         patients = Patient.objects.filter(user=request.user)

#     return render(request, 'patient/patient_list.html', {'Pat': patients})


@login_required
def add_patient(request):
    doc = Doctor.objects.all()

    if request.method == "POST":

        doctor = Doctor.objects.get(id=request.POST.get('doctor'))

        Patient.objects.create(
            name=request.POST.get('name'),
            age=request.POST.get('age'),
            gender=request.POST.get('gender'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            doctor=doctor,
        )
        return redirect('patient_list')

    return render(request, 'patient/add_patient.html', {'Doc': doc})


@login_required
def edit_patient(request, id):
    pat = Patient.objects.get(id=id)
    doc = Doctor.objects.all()

    if request.method == "POST":
        pat.name = request.POST.get('name')
        pat.age = request.POST.get('age')
        pat.gender = request.POST.get('gender')
        pat.phone = request.POST.get('phone')
        pat.address = request.POST.get('address')
        pat.doctor = Doctor.objects.get(id=request.POST.get('doctor'))
        pat.save()
        return redirect('patient_list')

    return render(request, 'patient/edit_patient.html', {'Pat': pat, 'Doc': doc})


@login_required
def delete_patient(request, id):
    Patient.objects.get(id=id).delete()
    return redirect('patient_list')


# Appointment CRUD

@login_required
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointment/appointment_list.html', {'appointments': appointments})


# @login_required
# def appointment_list(request):
#     if request.user.user_types == "Admin":
#         appointments = Appointment.objects.all()

#     elif request.user.user_types == "Doctor":
#         doctor = Doctor.objects.get(user=request.user)
#         appointments = Appointment.objects.filter(doctor=doctor)

#     elif request.user.user_types == "Patient":
#         appointments = Appointment.objects.filter(patient__user=request.user)

#     else:
#         appointments = Appointment.objects.none()

#     return render(request, 'appointment/appointment_list.html', {
#         'appointments': appointments
#     })


@login_required
def add_appointment(request):
    pat = Patient.objects.all()
    doc = Doctor.objects.all()

    if request.method == "POST":
        Appointment.objects.create(
            patient=Patient.objects.get(id=request.POST.get('patient')),
            doctor=Doctor.objects.get(id=request.POST.get('doctor')),
            appointment_date=request.POST.get('appointment_date'),
            status=request.POST.get('status'),
        )
        return redirect('appointment_list')

    return render(request, 'appointment/add_appointment.html', {'Pat': pat, 'Doc': doc})


@login_required
def edit_appointment(request, id):
    appoin = Appointment.objects.get(id=id)
    pat = Patient.objects.all()
    doc = Doctor.objects.all()

    if request.method == "POST":
        appoin.patient = Patient.objects.get(id=request.POST.get('patient'))
        appoin.doctor = Doctor.objects.get(id=request.POST.get('doctor'))
        appoin.appointment_date = request.POST.get('appointment_date')
        appoin.status = request.POST.get('status')
        appoin.save()
        return redirect('appointment_list')

    return render(request, 'appointment/edit_appointment.html', {
        'Appoin': appoin,
        'Pat': pat,
        'Doc': doc
    })


@login_required
def delete_appointment(request, id):
    Appointment.objects.get(id=id).delete()
    return redirect('appointment_list')


def patient_appointment(request):
    appointments = Appointment.objects.all()
    context = {
        'Appointment': appointments
    }
    return render(request, 'appointment/patient_appointment.html', context)


# # REQUIRED RELATION PAGES


@login_required
def department_doctor_list(request, id):
    dept = Department.objects.get(id=id)
    doc = Doctor.objects.filter(department=dept)

    return render(request, 'department/department_doctor_list.html', {
        'Dept': dept,
        'Doc': doc
    })


@login_required
def doctor_patient_list(request, id):
    doc = Doctor.objects.get(id=id)
    pat = Patient.objects.filter(doctor=doc)

    return render(request, 'doctor/doctor_patient_list.html', {
        'Doc': doc,
        'Pat': pat
    })


@login_required
def patient_appointment_list(request, id):
    pat = Patient.objects.get(id=id)
    appoin = Appointment.objects.filter(patient=pat)

    return render(request, 'patient/patient_appointment_list.html', {
        'Pat': pat,
        'Appoin': appoin
    })


# Doctor Profile

@login_required
def doctor_profile(request, id):
    doc = Doctor.objects.get(id=id)
    pat = Patient.objects.filter(doctor=doc)
    appoin = Appointment.objects.filter(doctor=doc)

    return render(request, 'doctor/doctor_profile.html', {
        'Doc': doc,
        'Pat': pat,
        'Appoin': appoin
    })
