from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
import django.contrib.auth as djauth
from . import models


# Create your views here.

def index(request):  # Index/Home page
    news = models.News.objects.all()  # Get all the News/Posts
    if request.user.is_authenticated:
        nav = [  # Set the Navbar elements according to user
            ['/', 'Home'],
            ['dashboard', 'Dashboard'],
            ['medicine', 'Medicine'],
            ['appointments', 'Appointment'],
            ['logout', 'Logout']
        ]
    else:
        nav = [
            ['/', 'Home'],
            ['login', 'Login'],
            ['medicine', 'Medicine']
        ]
    return render(request, 'home.html', context={'news': news, 'navs': nav})


def login(request):  # Login Page
    if request.user.is_authenticated:
        messages.info(request, 'You have logged in already')
        return redirect('/')
    nav = [
        ['/', 'Home'],
        ['medicine', 'Medicine']
    ]
    return render(request, 'html/login.html', context={'navs': nav})


def registration(request):  # Registration/Signup Page
    if request.user.is_authenticated:
        nav = [
            ['/', 'Home'],
            ['dashboard', 'Dashboard'],
            ['medicine', 'Medicine']
        ]
    else:
        nav = [
            ['/', 'Home'],
            ['medicine', 'Medicine']
        ]
    return render(request, 'html/registration.html', context={'navs': nav})


def logout(request):  # Logout
    djauth.logout(request)
    messages.warning(request, 'Logout Success')
    return redirect('/')


def medicine(request):  # Medicine Page
    if request.user.is_authenticated:
        nav = [
            ['/', 'Home'],
            ['dashboard', 'Dashboard'],
            ['appointments', 'Appointment']
        ]
    else:
        nav = [
            ['/', 'Home'],
            ['login', 'Login']
        ]
    meds = models.Medicine.objects.all()  # Get all the medicines
    context = {'meds': meds, 'navs': nav}
    return render(request, 'html/medicine.html', context=context)


def appointments(request):  # Appointments Page
    if request.user.is_authenticated:
        nav = [
            ['/', 'Home'],
            ['dashboard', 'Dashboard']
        ]
        options = models.Specialization.objects.all()
        return render(request, 'html/appointments.html', context={'navs': nav, 'opt': options})
    else:
        messages.error(request, 'Login required')
        return redirect('/')


def dashboard(request):  # Dashboard Page
    if request.user.is_authenticated:
        username = request.user  # Get the user info
        usertype = models.UserType.objects.get(username=username)
        nav = [
            ['/', 'Home'],
            ['medicine', 'Medicine'],
            ['appointments', 'Appointments']
        ]
        appointment = None
        if usertype.user_type == 'seller':  # Choose the content to be displayed accordingly
            userinfo = models.SellerUserInfo.objects.get(username=username)
        elif usertype.user_type == 'doctor':
            userinfo = models.DoctorUserInfo.objects.get(username=username)
            appointment = models.Appointments.objects.filter(doctor__icontains=userinfo.username)
        elif usertype.user_type == 'patient':
            userinfo = models.PatientUserInfo.objects.get(username=username)
            appointment = models.Appointments.objects.filter(patient__icontains=userinfo.username)
        else:
            userinfo = models.StaffUserInfo.objects.get(username=username)

        context = {'usr': userinfo, 'navs': nav, 'usr_type': usertype.user_type, 'appointments': appointment}
        return render(request, 'html/dashboard.html', context=context)

    else:
        messages.warning(request, 'Not Authenticated')
        return redirect('/')


def addmeds(request):  # Adding Medicine Page
    if request.user.is_authenticated:
        nav = [
            ['/', 'Home'],
            ['dashboard', 'Dashboard']
        ]
        return render(request, 'html/addmeds.html', context={'navs': nav})
    else:
        messages.error(request, 'Login required')
        return redirect('/')


def handle_med_search(request):  # Handling medicine search
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        search_res = models.Medicine.objects.filter(title__icontains=search_query)

        if request.user.is_authenticated:
            nav = [
                ['/', 'Home'],
                ['dashboard', 'Dashboard']
            ]
        else:
            nav = [
                ['/', 'Home'],
                ['login', 'Login']
            ]
        meds = models.Medicine.objects.all()  # Get all the medicines
        context = {'meds': meds, 'navs': nav}

        if len(search_res) > 0:
            messages.info(request, 'Found few Medicines')
            return render(request, 'html/medicine.html', context={'meds': search_res, 'navs': nav})

        messages.warning(request, 'Medicine not found Try giving exact name')
        return render(request, 'html/medicine.html', context=context)

    return redirect('medicine')


def handle_medicine(request):  # Redirect to Payments Page
    return render(request, 'html/payments.html')


def handle_added_meds(request):  # Handle added Medicines
    user = None
    if request.user.is_authenticated:
        user = request.user
    if request.method == 'POST':
        title = request.POST.get('title', '')
        price = request.POST.get('price', '')
        image = request.FILES.get('image', '')
        description = request.POST.get('description', '')

        med = models.Medicine(
            title=title,
            price=price,
            image=image,
            description=description
        )
        med.save()
        try:
            seller = models.SellerUserInfo.objects.get(username=user)
        except:
            messages.error(request, 'You are not logged in as Seller')
            return redirect('addmeds')
        seller.total_no_medicines += 1  # Increase seller's no of medicines
        seller.save()

        messages.success(request, 'Medicine Added')
        return redirect('addmeds')

    messages.error(request, 'Adding Medicine Failed')
    return redirect('addmeds')


def handle_registration(request):  # Handle Registration/Signup
    if request.method == 'POST':
        user = request.POST.get('user', '')
        username = request.POST.get('username', '')
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')

        try:
            my_user = User.objects.create_user(username=username, password=password)  # Create User
        except:
            messages.error(request, 'Username is already taken Try again with different username')
            return redirect('registration')
        my_user.save()

        user_type_info = models.UserType(
            user_type=user,
            username=username
        )
        user_type_info.save()

        if user == 'staff':
            my_user_info = models.StaffUserInfo(
                username=username,
                name=name,
                email=email,
                phone=phone,
                address=address
            )  # Create a new User object with additional Fields
            my_user_info.save()
        elif user == 'patient':
            my_user_info = models.PatientUserInfo(
                username=username,
                name=name,
                email=email,
                phone=phone,
                address=address
            )  # Create a new User object with additional Fields
            my_user_info.save()
        elif user == 'doctor':
            my_user_info = models.DoctorUserInfo(
                username=username,
                name=name,
                email=email,
                phone=phone,
                address=address
            )  # Create a new User object with additional Fields
            my_user_info.save()
        elif user == 'seller':
            my_user_info = models.SellerUserInfo(
                username=username,
                name=name,
                email=email,
                phone=phone,
                address=address
            )  # Create a new User object with additional Fields
            my_user_info.save()

        messages.success(request, 'Registration Success and Logged in')
        user = djauth.authenticate(request, username=username, password=password)
        if user is not None:
            djauth.login(request, user)
            return redirect('/')

    messages.error(request, 'Registration Failed')
    return redirect('registration')


def handle_appointments(request):       # Handle Appointments
    if request.method == 'POST':
        option = request.POST.get('option', '')
        illness = request.POST.get('illness', '')
        issue = request.POST.get('issue', '')
        try:
            patient = models.PatientUserInfo.objects.get(username=request.user)
        except:
            messages.error(request, 'You are not Logged in as Patient Unable to make an appointment')
            return redirect('appointments')
        doctor = models.DoctorUserInfo.objects.get(specialization=option)

        appointment = models.Appointments(
            illness=illness,
            issue=issue,
            patient=patient,
            doctor=doctor
        )
        appointment.save()
        patient.total_appointments += 1
        doctor.total_appointments += 1
        patient.save()
        doctor.save()

        messages.success(request, 'Appointment Success')
        return redirect('appointments')

    messages.error(request, 'Appointment Failed')
    return redirect('appointments')


def handle_login(request):  # Handle Login
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = djauth.authenticate(request, username=username, password=password)

        if user is not None:
            djauth.login(request, user)
            messages.success(request, 'Login Success')
            return redirect('/')

    messages.error(request, 'Login Failed')
    return redirect('/')


def handle_specialization(request):     # Handle added Specialization by Doctor
    if request.method == 'POST':
        specialization = request.POST.get('specialization', '')
        doc = models.DoctorUserInfo.objects.get(username=request.user)
        print(doc.specialization)
        doc.specialization = specialization
        doc.save()
        try:
            specialization_obj = models.Specialization(
                specialization=specialization
            )
        except:
            messages.error(request,'Specialization is already present')
            return redirect('dashboard')
        specialization_obj.save()
        messages.success(request, 'Specialization has been added')
        return redirect('dashboard')

    messages.error('Specialization has not been added')
    return redirect('/')


def handle_news(request):       # Handle News posted by user
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')

        news = models.News(
            title=title,
            text=content
        )
        news.save()
        messages.success(request, 'News Added')
        return redirect('dashboard')

    messages.error(request, 'News was not added')
    return redirect('dashboard')


def handle_appointment_treated(request):        # Handle appointments as treated by doctor
    if request.method == 'POST':
        apn = request.POST.get('apn', '')
        appointment = models.Appointments.objects.get(apn=apn)
        appointment.treated = True
        appointment.save()
        patient = models.PatientUserInfo.objects.get(username=appointment.patient)
        doctor = models.DoctorUserInfo.objects.get(username=appointment.doctor)
        patient.treated_appointments += 1
        doctor.treated_appointments += 1
        patient.save()
        doctor.save()

        messages.success(request, 'Marked as Treated')
        return redirect('dashboard')

    messages.error(request, 'Failed to Mark as Treated')
    return redirect('dashboard')
