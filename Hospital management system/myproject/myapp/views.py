from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import *
# Create your views here.


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import *


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def registration(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('Confirm_Password')
        user_types = request.POST.get('user_types')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists')
            return redirect('registration')

        if password == confirm_password:
            CustomUser.objects.create_user(
                full_name=full_name,
                username=username,
                email=email,
                password=password,
                user_types=user_types,
            )
            messages.success(request, "Account created successfully")
            return redirect('loginpage')

    return render(request, 'auth/registration.html')


def loginPage(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.warning(request, 'Invalid credentials')
    return render(request, 'auth/loginpage.html')


def logout(request):
    auth_logout(request)
    return redirect('loginpage')


@login_required
def changepassword(request):
    if request.method == "POST":
        if check_password(request.POST.get('old_password'), request.user.password):
            if request.POST.get('new_password') == request.POST.get('confirm_password'):
                request.user.set_password(request.POST.get('new_password'))
                request.user.save()
                update_session_auth_hash(request, request.user)
                return redirect('dashboard')
    return render(request, "auth/changepassword.html")


@login_required
def department_list(request):
    return render(request, 'department/department_list.html', {
        'Dept': Department.objects.all()
    })


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
    return render(request, 'department/view_department.html', {
        'Dept': dept
    })
    

@login_required
def doctor_list(request):
    return render(request, 'doctor/doctor_list.html', {
        'Doc': Doctor.objects.all()
    })


@login_required
def add_doctor(request):
    dept = Department.objects.all()
    if request.method == "POST":
        department = Department.objects.get(
            id=request.POST.get('department_id'))

        Doctor.objects.create(
            name=request.POST.get('name'),
            specialization=request.POST.get('specialization'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            department=department,
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
    return render(request, 'patient/patient_list.html', {
        'Pat': Patient.objects.all()
    })


@login_required
def add_patient(request):
    doc = Doctor.objects.all()
    if request.method == "POST":
        doctor = Doctor.objects.get(id=request.POST.get('doctor_id'))

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

    return render(request, 'patient/edit_patient.html', {
        'Pat': pat,
        'Doc': doc
    })


@login_required
def delete_patient(request, id):
    Patient.objects.get(id=id).delete()
    return redirect('patient_list')


# Appointment CRUD

@login_required
def appointment_list(request):
    return render(request, 'appointment/appointment_list.html', {
        'Appoin': Appointment.objects.all()
    })


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

    return render(request, 'appointment/add_appointment.html', {
        'Pat': pat,
        'Doc': doc
    })


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


# REQUIRED RELATION PAGES


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


# @login_required
# def dashboard(request):
#     return render(request,'dashboard.html')

# def registration(request):
#     if request.method=="POST":
#         full_name=request.POST.get('full_name')
#         username=request.POST.get('username')
#         email=request.POST.get('email')
#         password=request.POST.get('password')
#         Confirm_Password=request.POST.get('Confirm_Password')
#         user_types=request.POST.get('user_types')

#         user_exist=CustomUser.objects.filter(username=username).exists()
#         if user_exist:
#             messages.warning(request, 'Username Already exist')
#             return redirect('registration')
#         if password==Confirm_Password:

#             CustomUser.objects.create_user(
#                 full_name=full_name,
#                 username=username,
#                 email=email,
#                 password=password,
#                 user_types=user_types,
#             )
#             messages.success(request, "Account Successfully Created!")
#             return redirect('loginpage')
#         else:
#             messages.warning(request, 'Password Did not matche!')
#             return redirect('registration')
#     return render(request, 'auth/registration.html')


# def loginPage(request):
#     if request.method=="POST":
#         username=request.POST.get('username')
#         password=request.POST.get('password')

#         user=authenticate(request, username=username, password=password)

#         if user:
#             login(request, user)
#             messages.success(request, 'Succesfully Login!')
#             return redirect('dashboard')
#         else:
#             messages.warning(request, 'Invalid Credentials!')
#             return redirect('loginpage')
#     return render(request, 'auth/loginpage.html')


# def logout(request):
#     logout(request)
#     return redirect('loginpage')


# @login_required
# def changepassword(request):
#     if request.method=="POST":
#         old_password=request.POST.get('old_password')
#         new_password=request.POST.get('new_password')
#         confirm_password=request.POST.get('confirm_password')

#         if check_password(old_password, request.user.password):
#             if new_password==confirm_password:
#                 request.user.set_password(new_password)
#                 request.user.save()
#                 update_session_auth_hash(request, request.user)
#                 messages.success(request, "Succesfully Changed password")
#                 return redirect('dashboard')
#     return render(request, "auth/changepassword.html")


# @login_required
# def department_list(request):
#     dept=Department.objects.all()
#     return render(request, 'department/department_list.html',{'Dept':dept})


# @login_required
# def add_department(request):
#     if request.method=="POST":
#         Department.objects.create(
#             name=request.POST.get('name'),
#             location=request.POST.get('location'),
#         )
#         messages.success(request, "Succesfully Added data")
#         return redirect('department_list')
#     return render(request, 'department/add_department.html')


# @login_required
# def edit_department(request, id):
#     dept=Department.objects.get(id=id)
#     if request.method=="POST":
#         dept.name=request.POST.get('name')
#         dept.location=request.POST.get('location')
#         dept.save()
#         messages.success(request, "Succesfully Added data")
#         return redirect('department_list')
#     return render(request, 'department/edit_department.html', {'Dept':dept})


# @login_required
# def delete_department(request, id):
#     Department.objects.get(id=id).delete()
#     return redirect('department_list')


# @login_required
# def view_department(request, id):
#     view=Department.objects.get(id=id)
#     return render(request,'department/view_department.html',{'view':view})


# @login_required
# def doctor_list(request):
#     doc=Doctor.objects.all()
#     return render(request, 'doctor/doctor_list.html',{'Doc':doc})

# def add_doctor(request):
#     dept=Department.objects.all()
#     context={
#         'dept':dept,
#     }
#     if request.method=="POST":

#         name=request.POST.get('name')
#         specialization=request.POST.get('specialization')
#         department_id=request.POST.get('department_id')
#         phone=request.POST.get('phone')
#         email=request.POST.get('email')
#         username=request.POST.get('username')
#         department=Department.objects.get(id=department_id)

#         user_exist=CustomUser.objects.filter(username=username).exists()

#         if user_exist:
#             messages.warning(request,"Doctor already exist!")
#             return redirect('add_doctor')
#         user=CustomUser.objects.create_user(
#             email=email,
#             username=username,
#             password="1234",
#             user_types="Doctor",

#         )
#         if user:
#             Doctor.objects.create(
#                 name=name,
#                 specialization=specialization,
#                 phone=phone,
#                 department=department,
#             )
#             return redirect('doctor_list')
#     return redirect(request,'doctor/doctor_list.html',context)


# def edit_doctor(request,id):
#     doc=Doctor.objects.get(id=id)
#     dept=Department.objects.all()
#     context={
#         'dept':dept,
#         'doc':'doc',
#     }
#     if request.method=="POST":
#         name=request.post.get('name')
#         specialization=request.POST.get('specialization')
#         department_id=request.POST.get('department')
#         phone=request.POST.get('phone')

#         doc.name=name,
#         doc.specialization=specialization,
#         doc.department=department,
#         doc.save()
#         return redirect('doctor_list')
#     return render(request,'doctor/edit_doctor.html',context)

# def delete_doctor(request,id):
#     Doctor.objects.get(id=id)
#     return redirect(doctor_list)


# @login_required
# def patient_list(request):
#     pat=Patient.objects.all()
#     return render(request, 'patient/patient_list.html',{'Pat':pat})


# @login_required
# def appointment_list(request):
#     appoin=Appointment.objects.all()
#     return render(request, 'appointment/appointment_list.html',{'Appoin':appoin})
