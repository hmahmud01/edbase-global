from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from .models import *

TEACHER_TYPE = "Teacher"
STUDENT_TYPE = "Student"
DEFAULT_PASS = "edbase2022"


def userLogout(request):
    logout(request)
    return redirect('/')

def home(request):
    data = ""
    return render(request, 'index.html', {'data': data})

def login(request):
    data = ""
    return render(request, 'login.html', {'data': data})

def verifyLogin(request):
    post_data = request.POST
    pass

def register(request):
    data = ""
    return render(request, 'register.html', {'data': data})

def listTeachers(request):
    data = Teacher.objects.all()    
    qualifications = qualifcation.objects.all()
    return render(request, 'list_teachers.html', {'data': data, 'qualifications': qualifications})

def addTeacher(request):
    teacher = Teacher.objects.all()
    post_data = request.POST
    username = post_data['email']
    if User.objects.filter(username=username).exists():
        alert="Teacher Already Exists"
        return render(request, 'list_teachers.html', {'data': teacher, 'alert': alert})
    else:
        user = User.objects.create_user(post_data['email'], post_data['email'], DEFAULT_PASS)
        qualifcation = Qualification.objects.get(id=post_data['qual'])
        teacher = Teacher(
            user = user,
            name = post_data['namae'],
            phone = post_data['phone'],
            email = post_data['email'],
            level = post_data['level'],
            qualification = qualifcation,
            user_type = TEACHER_TYPE,            
        )
        teacher.save()
        alert="Teacher Created Successfully"
        return render(request, 'list_teachers.html', {'data': teacher, 'alert': alert})


def listStudents(request):
    data = Student.objects.all()    
    return render(request, 'list_students.html', {'data': data})

def detailStudent(request):
    pass

def listCountries(request):
    data = Country.objects.all()
    return render(request, 'list_countries.html', {'data': data})

def addCountry(request):
    post_data = request.POST
    country = Country(
        name = post_data['name'],
        short = post_data['short']
    )

    country.save()
    return redirect('countries')

def listUniversities(request):
    data = University.objects.all()
    countries = Country.objects.all()
    return render(request, 'list_universities.html', {'data': data, 'countries': countries})

def addUniversity(req_user):
    post_data = request.POST
    file_data = request.FILES
    country = Country.objects.get(id=post_data['country_id'])
    university = University(
        name = post_data['name'],
        country = country,
        url = post_data['url'],
        description = post_data['post_data'],
        image = file_data['image']
    )
    university.save()
    return redirect('universities')

def listDirectory(request):
    data = Directory.objects.all()
    return render(request, 'list_direcotries.html', {'data': data})

def addDirectory(request):
    directory = Directory(
        title = request.POST['title']
    )
    directory.save()

    return redirect('directories')

def listQualifications(request):
    data = Student.objects.all()    
    return render(request, 'list_qualifications.html', {'data': data})

def addQualification(request):
    post_data = request.POST
    qual = Qualification(
        title = post_data['title'],
        level = post_data['level']
    )

    qual.save()

    return redirect('qualifications')