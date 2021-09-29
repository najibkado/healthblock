from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .models import User, Staff, Patient, Event, Departmet
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
import json
import ast
from .utils import create_event

# Create your views here.
@login_required
def index(request):

    loggedin_user = request.user

    if loggedin_user.is_staff or loggedin_user.is_superuser or loggedin_user.staff_details.get().is_it or loggedin_user.staff_details.get().is_director:
        create_event(request.user, "Loggedin to IT staff portal")
        pass
    else:
        create_event(request.user, "Tried to access IT staff portal")
        messages.error(request, "You have no access!")
        return HttpResponseRedirect(reverse("main:logout"))

    event_count = Event.objects.filter(user=loggedin_user).count

    user_count = User.objects.all().count()
    staff_count = Staff.objects.all().count()
    doctor_count = Staff.objects.filter(is_doctor=True).count()
    patient_count = Patient.objects.all().count()
    staff_name = f"{loggedin_user.first_name} {loggedin_user.last_name}"
    staff_username = loggedin_user.username
    staff_number = loggedin_user.id
    staff_email = loggedin_user.email

    try:
        staff = Staff.objects.get(user=loggedin_user)

        staff_job = staff.job
        staff_department = staff.department.name
        staff_phone = staff.phone
        staff_address = staff.address

        context = {
            "user_count": user_count,
            "staff_count": staff_count,
            "doctor_count": doctor_count,
            "patient_count": patient_count,
            "staff_username": staff_username,
            "staff_name": staff_name,
            "staff_number": staff_number,
            "staff_phone": staff_phone,
            "staff_email": staff_email,
            "staff_job": staff_job,
            "staff_department": staff_department,
            "staff_event_count": event_count,
            "staff_address": staff_address
        }

    except Staff.DoesNotExist:
        
        context = {
            "user_count": user_count,
            "staff_count": staff_count,
            "doctor_count": doctor_count,
            "patient_count": patient_count,
            "staff_username": staff_username,
            "staff_name":staff_name,
            "staff_number":staff_number,
            "staff_email": staff_email,
            "staff_event_count": event_count
        }

    # staff_phone: loggedin_user.phone
    # staff_job = loggedin_user.staff_details.get().job
    # staff_department = loggedin_user.staff_details.get().staff_department.get().name


    return render(request, 'main/index.html', context)

@login_required
def staffs_view(request):

    loggedin_user = request.user

    if loggedin_user.is_staff or loggedin_user.is_superuser or loggedin_user.staff_details.get().is_it or loggedin_user.staff_details.get().is_director:
        pass
    else:
        create_event(request.user, "Tried to access IT staff portal")
        messages.error(request, "You have no access!")
        return HttpResponseRedirect(reverse("main:logout"))

    if request.method == "GET":

        staffs = Staff.objects.all()

        staffs_info = []

        for staff in staffs:
            staff_job = staff.job
            staff_department = staff.department.name
            staff_phone = staff.phone
            staff_address = staff.address
            staff_username = staff.user.username
            staff_name = f"{staff.user.first_name} {staff.user.last_name}"
            staff_number = staff.user.id
            staff_email = staff.user.email
            event_count = Event.objects.filter(user=staff.user).count()


            staff_detail = {
                "staff_username": staff_username,
                "staff_name": staff_name,
                "staff_number": staff_number,
                "staff_phone": staff_phone,
                "staff_email": staff_email,
                "staff_job": staff_job,
                "staff_department": staff_department,
                "staff_event_count": event_count,
                "staff_address": staff_address
            }

            staffs_info.append(staff_detail)

        create_event(request.user, "Accessed staffs page")
        return render(request, "main/staffs.html", {"staffs": staffs_info})

@login_required
def staff_view(request):

    loggedin_user = request.user

    if loggedin_user.is_staff or loggedin_user.is_superuser or loggedin_user.staff_details.get().is_it or loggedin_user.staff_details.get().is_director:
        pass
    else:
        create_event(request.user, "Tried to access IT staff portal")
        messages.error(request, "You have no access!")
        return HttpResponseRedirect(reverse("main:logout"))

    if request.method == "POST":

        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        username = request.POST['username']
        address = request.POST['address']
        job = request.POST['job']
        department = request.POST['department']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        is_doctor = request.POST.get('is-doctor')
        is_it = request.POST.get('is-it')
        is_receptionist = request.POST.get('is-receptionist')
        is_analyst = request.POST.get('is-analyst')
        is_lab = request.POST.get('is-lab')
        is_director = request.POST.get('is-director')

        if first_name is "" or last_name is "" or username is "" or address is "" or job is "" or department is "" or phone is "" or email is "" or password is "":
            messages.error(request, "Fields can't be empty!")
            create_event(request.user, "Tried to register a new staff from staff portal")
            return HttpResponseRedirect(reverse("main:staff"))

        if is_doctor is None and is_it is None and is_receptionist is None and is_analyst is None and is_lab is None and is_director:
            messages.error(request, "Staffs must have atleast one privilege")
            create_event(request.user, "Tried to register a new staff from staff portal")
            return HttpResponseRedirect(reverse("main:staff")) 

        try:
            new_user = User.objects.create_user(
                username = username,
                password = password,
                email = email,
                first_name = first_name,
                last_name = last_name,
            )
            new_user.save()
            token = Token.objects.create(user=new_user)
        except:
            create_event(request.user, "Tried to register a new staff from staff portal")
            messages.error(request, "Unable to create a user")
            return HttpResponseRedirect(reverse("main:staff"))

        try:
            new_staff = Staff(
                user = new_user,
                department = Departmet.objects.get(pk=int(department)),
                job = job,
                phone = phone,
                address = address,
                is_doctor = True if is_doctor is not None else False,
                is_it = True if is_it is not None else False,
                is_receptionist = True if is_receptionist is not None else False,
                is_lab = True if is_lab is not None else False,
                is_analyst = True if is_analyst is not None else False,
                is_director = True if is_director is not None else False            
            )
            new_staff.save()
        except IntegrityError:
            create_event(request.user, "Tried to register a new staff from staff portal")
            messages.error(request, "Unable to create a new user")
            return HttpResponseRedirect(reverse("main:staff"))


        data = {
            "message":"User created successfully",
            "new_user": f"{new_staff.user.first_name} {new_staff.user.last_name}",
            "new_user_username": new_staff.user.username,
            "date": str(new_staff.user.date_joined )   
        }
        create_event(request.user, f"Registered a new staff | {new_staff.user.first_name} {new_staff.user.last_name}")
        return HttpResponseRedirect(reverse("main:success", args=(data,)))

    if request.method == "GET":

        departments = Departmet.objects.all()
        create_event(request.user, "Accessed staff creation page from IT staff portal")
        return render(request, "main/staff.html", {
            "departments": departments
        })

@login_required
def delete_staff_view(request, id):

    loggedin_user = request.user

    if loggedin_user.is_staff or loggedin_user.is_superuser or loggedin_user.staff_details.get().is_it or loggedin_user.staff_details.get().is_director:
        pass
    else:
        create_event(request.user, "Tried to access IT staff portal")
        messages.error(request, "You have no access!")
        return HttpResponseRedirect(reverse("main:logout"))

    if request.method == "GET":

        try:
            staff_to_delete = User.objects.get(pk=id)
        except User.DoesNotExist:
            messages.error(request, "User not found!")
            return HttpResponseRedirect(reverse("main:staffs"))

        create_event(request.user, f'Accessed staff deletion page for {staff_to_delete.first_name} {staff_to_delete.last_name}')

        return render(request, "main/delete.html", {
            "user_number": staff_to_delete.id,
            "user_to_delete": f'{staff_to_delete.first_name} {staff_to_delete.last_name}'
        })

    if request.method == "POST":
        
        val = request.POST['val']
        try:
            user_to_delete = User.objects.get(pk=val)
        except User.DoesNotExist:
            messages.error(request, "User not found!")
            return HttpResponseRedirect(reverse("main:staffs"))

        create_event(request.user, f'Deleted staff {user_to_delete.first_name} {user_to_delete.last_name}')
        user_to_delete.delete()
        messages.success(request, "User deleted successfully")
        return HttpResponseRedirect(reverse("main:staffs"))


@login_required
def departments_view(request):
    loggedin_user = request.user

    if loggedin_user.is_staff or loggedin_user.is_superuser or loggedin_user.staff_details.get().is_it or loggedin_user.staff_details.get().is_director:
        pass
    else:
        create_event(request.user, "Tried to access IT staff portal")
        messages.error(request, "You have no access!")
        return HttpResponseRedirect(reverse("main:logout"))

    if request.method == "GET":
        departments = Departmet.objects.all()
        create_event(request.user, f'Accessed departments listing')
        return render(request, "main/departments.html", {
            "departments": departments
        })

    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']

        if title == "" or description == "":
            messages.error(request, "Fields can't be empty!")
            return HttpResponseRedirect(reverse("main:departments"))

        try:
            new_department = Departmet(
                name = title,
                description = description
            )
            new_department.save()
            create_event(request.user, f'Created a department {new_department.name}')
        except IntegrityError:
            create_event(request.user, f'Tried to create a new department')
            messages.error(request, "Unable to create department, please try again")
            return HttpResponseRedirect(reverse("main:departments"))

        messages.success(request, "Department created successfully")
        return HttpResponseRedirect(reverse("main:departments"))


@login_required
def department_view(request, id):
    loggedin_user = request.user

    if loggedin_user.is_staff or loggedin_user.is_superuser or loggedin_user.staff_details.get().is_it or loggedin_user.staff_details.get().is_director:
        pass
    else:
        create_event(request.user, "Tried to access IT staff portal")
        messages.error(request, "You have no access!")
        return HttpResponseRedirect(reverse("main:logout"))

    if request.method == "GET":
        try:
            department_to_delete = Departmet.objects.get(pk=id)
        except Departmet.DoesNotExist:
            messages.error(request, "Department not found")
            create_event(request.user, f'Tried to delete department with id {id}')
            return HttpResponseRedirect(reverse("main:departments"))

        create_event(request.user, f'Deleted department {department_to_delete.name}')
        department_to_delete.delete()
        messages.success(request, "Department deleted successfully")
        return HttpResponseRedirect(reverse("main:departments"))

def success_view(request, data):
    loggedin_user = request.user

    if loggedin_user.is_staff or loggedin_user.is_superuser or loggedin_user.staff_details.get().is_it or loggedin_user.staff_details.get().is_director:
        pass
    else:
        create_event(request.user, "Tried to access IT staff portal")
        messages.error(request, "You have no access!")
        return HttpResponseRedirect(reverse("main:logout"))

    context = ast.literal_eval(data)
    return render(request, "main/success.html", context)

def login_view(request):
    if request.method == 'GET':
        return render(request, 'main/auth/login.html', {
            'tab': 'login'
        })

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            create_event(user, f'Loggedin')

            redirect_to = request.GET.get('next')
            if redirect_to:
                return HttpResponseRedirect(redirect_to)

            return HttpResponseRedirect(reverse('main:index'))

        else:
            messages.error(request, 'Invalid user details')
            return HttpResponseRedirect(reverse('main:login'))


def register_view(request):
    if request.method == 'GET':
        return render(request, 'main/auth/login.html', {
            'tab': 'register'
        })

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if len(username) < 4:
            messages.warning(request, 'Username too short')
            return HttpResponseRedirect(reverse('main:register'))

        if len(password) < 6:
            messages.warning(request, 'Password too weak')
            return HttpResponseRedirect(reverse('main:register'))

        try:
            check_username = User.objects.get(username=username)
            if check_username:
                messages.error(request, 'Invalid username or password')
                return HttpResponseRedirect(reverse('main:register'))
        except User.DoesNotExist:
            pass

        try:
            new_user = User.objects.create_user(
                username = username,
                password = password,
                email = email
            )
            new_user.save()
            create_event(new_user, f'Registered as a new user {new_user}')
            token = Token.objects.create(user=new_user)
        except:
            return HttpResponse('Unable to create a user')

        return HttpResponseRedirect(reverse('main:index'))


@login_required
def logout_view(request):
    create_event(request.user, f'Logged out')
    logout(request)
    return HttpResponseRedirect(reverse('main:login'))



