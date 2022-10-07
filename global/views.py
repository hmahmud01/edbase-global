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

def landing(request):
    return render(request, 'landing/index.html')

def userLogout(request):
    logout(request)
    return redirect('/')

def login(request):
    data = ""
    return render(request, 'login.html', {'data': data})

def verifyLogin(request):
    post_data = request.POST
    if post_data['username'] and post_data['pass']:
        user = authenticate(
            request,
            username = post_data['username'],
            password = post_data['pass']
        )
        if user is None:
            return redirect('login')
        else:
            auth_login(request, user)
            return redirect('home')
    else:
        return redirect('login')
        
def home(request):
    data = ""
    user  = request.user
    if user.is_superuser:    
        return render(request, 'index.html', {'data': data})
    else:
        if Teacher.objects.filter(user_id=user.id).exists():
            print("TEACHER")
            print(Teacher.objects.get(user_id=user.id))
            return render(request, 'index_teacher.html')
        elif Student.objects.get(user_id=user.id).exists():
            print("STUDENT")
            print(Student.objects.filter(user_id=user.id))
            return render(request, 'index_student.html')
        else:
            return redirect('failed')
        # try:            
        #     req_user = Teacher.objects.get(user=user.id)
        #     print("TEACHER")
        #     print(req_user)
        #     return render(request, 'index_teacher.html')
        # except:
        #     req_user = Student.objects.get(user=user.id)
        #     print("STUDENT")
        #     print(req_user)
        #     return render(request, 'index_student.html')

def register(request):
    data = ""
    qualifications = Qualification.objects.all()
    return render(request, 'register.html', {'data': data, 'qualifications': qualifications})

# <QueryDict: {'csrfmiddlewaretoken': ['7Bo3ThkJZP34z5MvGa2pNDLEKNxNj5wvBLk5mW4pkOzB0SoSK6wYjYRAuJqgsOGB'], 
# 'name': ['Alomgir'], 'mobile': ['1545212'], 'guardian_mobile': ['123561'], 'email': ['alomgir@chacha'], 
# 'school': ['MGBHS'], 'qual': ['3'], 'passport': ['fafe22222'], 'mother': ['Someone'], 'father': ['Else'], 
# 'parent_phone': ['12635454'], 'parent_email': ['parlent@ermgail.com'], 'street_1': ['Str111'], 'street_2': ['Str222'], 
# 'city': ['Dhaka'], 'zip_code': ['1214'], 'country': ['BD'], 'dob': ['2005-11-10'], 'blood_group': ['0+']}>
# <MultiValueDict: {'photo': [<InMemoryUploadedFile: avatar-2.jpg (image/jpeg)>]}>

def signupData(request):
    post_data = request.POST
    file_data = request.FILES
    username = post_data['email']
    qualification = Qualification.objects.get(id=post_data['qual'])

    if User.objects.filter(username=username).exists():
        return redirect('failed')
    else:
        user = User.objects.create_user(post_data['email'], post_data['email'], DEFAULT_PASS)
        student = Student(
            user = user,
            name = post_data['name'],
            mobile = post_data['mobile'],
            guardian_mobile = post_data['guardian_mobile'],
            email = post_data['email'],
            school = post_data['school'],
            qualification = qualification,
        )

        student.save()

        unique_id = "STD" + str(student.id)
        info = PersonalInfo(
            student=student,
            unique_id=unique_id,
            passport=post_data['passport'],
            father=post_data['father'],
            mother=post_data['mother'],
            father_mobile=post_data['parent_phone'],
            mother_mobile=post_data['parent_phone'],
            parent_email=post_data['parent_email'],
            street_1=post_data['street_1'],
            street_2=post_data['street_2'],
            city=post_data['city'],
            zip_code=post_data['zip_code'],
            dob=post_data['dob'],
            blood_group=post_data['blood_group'],
            photo=file_data['photo'],
        )

        info.save()

        return redirect('success')

def successPage(request):
    return render(request, 'success.html')

def failedPage(request):
    return render(request, 'failed.html')

def listTeachers(request):
    data = Teacher.objects.all()    
    qualifications = Qualification.objects.all()
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
            name = post_data['name'],
            phone = post_data['phone'],
            email = post_data['email'],
            level = post_data['level'],
            qualification = qualifcation,
            user_type = TEACHER_TYPE,            
        )
        teacher.save()
        print("teacher added")
        alert="Teacher Created Successfully"
        return render(request, 'list_teachers.html', {'data': teacher, 'alert': alert})


def listStudents(request):
    data = Student.objects.all()    
    qualifications = Qualification.objects.all()
    users = User.objects.all()
    print(users)
    return render(request, 'list_students.html', {'data': data, 'qualifications': qualifications, 'users': users})

def detailStudent(request):
    pass

def listCountries(request):
    data = Country.objects.all()
    return render(request, 'list_country.html', {'data': data})

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

def addUniversity(request):
    post_data = request.POST
    file_data = request.FILES
    print(post_data)
    print(file_data)
    country = Country.objects.get(id=post_data['country_id'])
    university = University(
        name = post_data['name'],
        country = country,
        url = post_data['url'],
        description = post_data['description'],
        image = file_data['image']
    )
    university.save()
    return redirect('universities')

def listDirectory(request):
    data = Directory.objects.all()
    return render(request, 'list_directory.html', {'data': data})

def addDirectory(request):
    directory = Directory(
        title = request.POST['title']
    )
    directory.save()

    return redirect('directories')

def listQualifications(request):
    data = Qualification.objects.all()    
    return render(request, 'list_qualifications.html', {'data': data})

def addQualification(request):
    post_data = request.POST
    print(post_data)
    qual = Qualification(
        title = post_data['title'],
        level = post_data['level']
    )

    qual.save()

    return redirect('qualifications')
    

TODO
def studentDetail(request, sid):
    pass
    
def assignTeacher(request):
    pass

def assignUniversity(request):
    pass

def directoryList(request):
    pass

def directoryIndex(request, did):
    pass


