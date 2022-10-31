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

ACTIVATE = "activate"
DEACTIVATE = "deactivate"

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
            return render(request, 'index_teacher.html')
        elif Student.objects.filter(user_id=user.id).exists():
            directories = Directory.objects.all().filter(status=True)
            return render(request, 'index_student.html', {'directories': directories})
        else:
            return redirect('failed')

def register(request):
    data = ""
    qualifications = Qualification.objects.all()
    countries = Country.objects.all()
    return render(request, 'register_v2.html', {'data': data, 'qualifications': qualifications, 'countries': countries})

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
            country=post_data['country'],
            dob=post_data['dob'],
            blood_group=post_data['blood_group'],
            photo=file_data['photo'],
        )

        info.save()

        return redirect('success')

# <QueryDict: {'csrfmiddlewaretoken': ['ykJzfEEyP10TYifqEf6O30UnS8aSBldZqwNvZZTVEcdTEgGdnut8tthjgUicK792'], 
# 'name': ['TE'], 'mobile': ['912123'], 
# 'guardian_mobile': ['123'], 'email': ['test@test.com'], 'school': ['MGBHS'], 
# 'qual': ['1'], 'country': ['1', '2', '3']}>
def signUp_v2(request):
    post_data = request.POST
    country_list = post_data.getlist('country')
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
        for ctry in country_list:
            country = Country.objects.get(id=ctry)
            cdx = StudentCountryIndex(
                student = student,
                country = country
            )

            cdx.save()

        return redirect('success')

def studentUpdate(request):
    post_data = request.POST
    student = Student.objects.get(id=post_data['sid'])
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
        country=post_data['country'],
        dob=post_data['dob'],
        blood_group=post_data['blood_group'],
        photo=file_data['photo'],
    )

    info.save()

    return redirect('myprofile')

def successPage(request):
    return render(request, 'success.html')

def failedPage(request):
    return render(request, 'failed.html')

def listTeachers(request):
    data = Teacher.objects.all()    
    qualifications = Qualification.objects.all()
    return render(request, 'list_teachers.html', {'data': data, 'qualifications': qualifications})

def addTeacher(request):
    teachers = Teacher.objects.all()
    post_data = request.POST
    file_data = request.FILES
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
            photo = file_data['photo'],
            user_type = TEACHER_TYPE,            
        )
        teacher.save()
        print("teacher added")
        alert="Teacher Created Successfully"
        return render(request, 'list_teachers.html', {'data': teachers, 'alert': alert})

def listStudents(request):    
    qualifications = Qualification.objects.all()
    users = User.objects.all()
    
    if request.user.is_superuser:
        data = Student.objects.all()    
    else:
        data = Student.objects.filter(assigned_teacher__id=request.user.teacher.id)

    return render(request, 'list_students.html', {'data': data, 'qualifications': qualifications, 'users': users})

def studentDetail(request, sid):

    student = Student.objects.get(id=sid)
    teachers = Teacher.objects.all()
    universities = University.objects.all()

    indexs = StudentUniversityIndex.objects.filter(student__id = sid)

    info = PersonalInfo.objects.get(student__id=sid)
    print("STUDENT DETAIL")
    directories = Directory.objects.all().filter(status=True)
    files = []
    print(directories)
    for directory in directories:
        contents = DirectoryIndex.objects.filter(directory__id=directory.id).filter(student__id=sid)                
        if contents.count() != 0:
            content = {
                'title': directory.title,
                'id': directory.id,
                'data': contents
            }
            files.append(content)
        else:
            content = {
                'title': directory.title,
                'id': directory.id,
                'data': None
            }
            files.append(content)
    
    print(files)
    return render(request, 'student_detail.html', {'student': student, 'teachers': teachers, 'info': info, 'universities': universities, 'indexs': indexs, 'files': files})

def addStudent(request):
    post_data = request.POST
    file_data = request.FILES
    username = post_data['email']
    qualification = Qualification.objects.get(id=post_data['qual'])

    if User.objects.filter(username=username).exists():
        return redirect('failstudentsed')
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
            country=post_data['country'],
            dob=post_data['dob'],
            blood_group=post_data['blood_group'],
            photo=file_data['photo'],
        )

        info.save()

        return redirect('students')

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

def uniDetail(request, uid):
    university = University.objects.get(id=uid)
    return render(request, 'ajax/detail_uni.html', {'university': university})

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

def deleteUniversity(request, uid):
    uni = University.objects.get(id=uid)
    uni.delete()

    return redirect('universities')

def loadUniversity(request):
    get_data = request.GET    
    uid = get_data.get('uid')
    university = University.objects.get(id=uid)
    return render(request, 'ajax/university.html', {'university': university})

def listDirectory(request):
    data = Directory.objects.all()
    return render(request, 'list_directory.html', {'data': data, 'activate': ACTIVATE, 'deactivate': DEACTIVATE})

def addDirectory(request):
    directory = Directory(
        title = request.POST['title']
    )
    directory.save()

    return redirect('directories')

def statusUpdateDirectory(request, did, status):
    directory = Directory.objects.get(id=did)
    if status == "activate":
        directory.status = True
    elif status == "deactivate":
        directory.status = False

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
    


def teacherDetail(request, tid):
    teacher = Teacher.objects.get(id=tid)
    data = Student.objects.filter(assigned_teacher__id=tid)
    return render(request, 'detail_teacher.html', {'teacher': teacher, 'data': data})
    
def assignTeacher(request):
    post_data = request.POST
    student = Student.objects.get(id=post_data['sid'])
    teacher = Teacher.objects.get(id=post_data['tid'])
    student.assigned_teacher = teacher

    student.save()

    return redirect('studentdetail', post_data['sid'])

def suggestUni(request):
    post_data = request.POST
    student = Student.objects.get(id=post_data['sid'])
    unis = post_data.getlist('universities')
    for uni in unis:
        univ = University.objects.get(id=uni)
        idx = StudentUniversityIndex(
            student = student,
            university = univ
        )
        idx.save()    

    return redirect('studentdetail', post_data['sid'])

def deleteSuggestion(request, iid):
    idx = StudentUniversityIndex.objects.get(id=iid)
    sid = idx.student.id
    idx.delete()

    return redirect('studentdetail', sid)


# STUDENT AREA

def myProfile(request):
    user_type = None

    try:
        student = request.user.student
        teachers = Teacher.objects.all()
        universities = University.objects.all()

        indexs = StudentUniversityIndex.objects.filter(student__id = student.id)
                
        directories = Directory.objects.all().filter(status=True)
        files = []

        for directory in directories:
            contents = DirectoryIndex.objects.filter(directory__id=directory.id).filter(student__id=student.id)                
            if contents.count() != 0:
                content = {
                    'title': directory.title,
                    'id': directory.id,
                    'data': contents
                }
                files.append(content)
            else:
                content = {
                    'title': directory.title,
                    'id': directory.id,
                    'data': None
                }
                files.append(content)

        info = PersonalInfo.objects.get(student__id=student.id)
        return render(request, 'student_detail.html', {'student': student, 'teachers': teachers, 'info': info, 'universities': universities, 'indexs': indexs, 'files': files})
    except:
        teacher = request.user.teacher
        data = Student.objects.filter(assigned_teacher__id=request.user.teacher.id)
        return render(request, 'detail_teacher.html', {'teacher': teacher, 'data': data})

def directoryList(request):
    pass

def directoryIndex(request, did):
    directory = Directory.objects.get(id=did)
    contents = DirectoryIndex.objects.filter(directory__id=did).filter(student__id=request.user.student.id)
    return render(request, 'directory_index.html', {'contents': contents, 'directory': directory})

def uploadContent(request):
    student = request.user.student
    post_data = request.POST
    file_data = request.FILES

    directory = Directory.objects.get(id=post_data['did'])
    contents = file_data.getlist('content')

    for files in contents:
        content = Content(
            file_content = files
        )
        content.save()
        didx = DirectoryIndex(
            directory = directory,
            student = student,
            content = content
        )

        didx.save()

    return redirect('directoryindex', post_data['did'])