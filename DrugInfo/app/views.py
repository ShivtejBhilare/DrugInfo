from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .models import CustomUser, Drug, Doctor, DrugDoctor
from datetime import datetime

@login_required
def admin_dashboard(request):
    users = CustomUser.objects.all()
    return render(request, 'admin/dashboard.html', {'users': users})

def home(request):
    try:
        return render(request, 'app/home.html')
    except Exception as ex:
        return render(request, 'app/home.html', {'message': ex})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'app/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'app/login.html')

def add_drug(request):
    if 'alogin' in request.session and request.session['alogin']:
        message = ''
        try:
            if request.method == "POST":
                if request.FILES:
                    name = str(request.POST.get('name')).strip()
                    photo = request.FILES['photo']
                    with open(f'media/drug/{name}.jpg', 'wb') as fw:
                        fw.write(photo.read())
                    drug = Drug()
                    drug.name = name
                    drug.info = request.POST.get('info')
                    drug.child = request.POST.get('child')
                    drug.adult = request.POST.get('adult')
                    drug.women = request.POST.get('women')
                    drug.banned = request.POST.get('banned')
                    drug.why = request.POST.get('why')
                    drug.save(force_insert=True)
                    message = 'Drug details added successfully...'
                else:
                    raise Exception('Photo uploading error')
        except Exception as ex:
            message = ex
        return render(request, 'admin/add_drug.html', {'message': message})
    else:
        return redirect(login_view)

def drug_master(request):
    if 'alogin' in request.session and request.session['alogin']:
        drugs = None
        message = ''
        try:
            if request.method == "POST":
                drug = Drug.objects.get(name=request.POST.get("name"))
                drug.delete()
                message = 'Drug details deleted successfully..'
            drugs = Drug.objects.all()
        except Exception as ex:
            message = ex
        return render(request, 'admin/drug_master.html', {'message': message, 'drugs': drugs})
    else:
        return redirect(login_view)

def add_doctor(request):
    if 'alogin' in request.session and request.session['alogin']:
        message = ''
        try:
            if request.method == 'POST':
                if request.FILES:
                    id_ = datetime.now().strftime('%d%m%y%I%M%S')
                    photo = request.FILES['photo']
                    with open(f'media/doctor/{id_}.jpg', 'wb') as fw:
                        fw.write(photo.read())
                    doctor = Doctor()
                    doctor.id = id_
                    doctor.name = request.POST.get('name')
                    doctor.qualification = request.POST.get('qualification')
                    doctor.mobile = str(request.POST.get('mobile')).strip()
                    doctor.email = str(request.POST.get('email')).strip()
                    doctor.address = request.POST.get('address')
                    doctor.gender = request.POST.get('gender')
                    doctor.agegroup = request.POST.get('agegroup')
                    doctor.experience = request.POST.get('experience')
                    doctor.speciality = request.POST.get('speciality')
                    doctor.save(force_insert=True)
                    message = 'Doctor profile added successfully...'
                else:
                    raise Exception('Photo uploading error')
        except Exception as ex:
            message = ex
        return render(request, 'admin/add_doctor.html', {'message': message})
    else:
        return redirect(login_view)

def doctor_master(request):
    if 'alogin' in request.session and request.session['alogin']:
        doctors = None
        message = ''
        try:
            if request.method == "POST":
                doctor = Doctor.objects.get(id=request.POST.get("id"))
                doctor.delete()
                message = 'Doctor details deleted successfully..'
            doctors = Doctor.objects.all()
        except Exception as ex:
            message = ex
        return render(request, 'admin/doctor_master.html', {'message': message, 'doctors': doctors})
    else:
        return redirect(login_view)

def assign_doctor(request):
    if 'alogin' in request.session and request.session['alogin']:
        message = ''
        drugs = None
        doctors = None
        try:
            drugs = Drug.objects.all()
            doctors = Doctor.objects.all()
            if request.method == 'POST':
                dd = DrugDoctor()
                dd.drug = Drug.objects.get(name=request.POST.get('drug'))
                dd.doctor = Doctor.objects.get(id=request.POST.get('doctor'))
                dd.save(force_insert=True)
                message = 'Doctor assigned successfully...'
        except IntegrityError:
            message = "Doctor already assigned to this drug... please select other doctor profile...."
        except Exception as ex:
            message = ex
        return render(request, 'admin/assign_doctor.html', {'message': message, 'drugs': drugs, 'doctors': doctors})
    else:
        return redirect(login_view)

def drug_doctor_master(request):
    if 'alogin' in request.session and request.session['alogin']:
        dds = None
        message = ''
        try:
            if request.method == "POST":
                dd = DrugDoctor.objects.get(drug=request.POST.get("drug"), doctor=request.POST.get("doctor"))
                dd.delete()
                message = 'Drug Doctor details deleted successfully..'
            dds = DrugDoctor.objects.all()
        except Exception as ex:
            message = ex
        return render(request, 'admin/drug_doctor_master.html', {'message': message, 'dds': dds})
    else:
        return redirect(login_view)

def search_drug(request):
    message = ''
    drugs = None
    banned = "yes"
    try:
        banned = request.GET.get("banned")
        drugs = Drug.objects.filter(banned=banned)
        if request.method == "POST":
            name = str(request.POST.get('name')).strip()
            drugs = Drug.objects.filter(name__icontains=name)
    except Exception as ex:
        message = ex
    return render(request, 'app/search_drug.html', {'message': message, 'banned': banned, 'drugs': drugs})

def view_doctors(request):
    message = ''
    doctors = None
    try:
        drug = request.GET.get("drug")
        dd = DrugDoctor.objects.filter(drug=drug)
        doctors = Doctor.objects.filter(id__in=list(dd.values_list('doctor', flat=True)))
    except Exception as ex:
        message = ex
    return render(request, 'app/view_doctors.html', {'message': message, 'doctors': doctors})
