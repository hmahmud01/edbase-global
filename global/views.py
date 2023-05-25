from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils.crypto import get_random_string
import datetime
import csv
from django.http import HttpResponse

from .models import *

from django.conf import settings
import os
import zipfile

TEACHER_TYPE = "Counselor"
STUDENT_TYPE = "Student"
DEFAULT_PASS = "edbase2022"

ACTIVATE = "activate"
DEACTIVATE = "deactivate"


def landing(request):
    header_class = "header-main"
    return render(request, 'landing/index.html', {'header_main': header_class})

@login_required(login_url="/login/")
def landing_videos(request):
    header_class = "header-videos"
    courses = Course.objects.filter(coursetype__title="Video")
    return render(request, 'landing/videos.html', {'header_main': header_class, 'courses': courses})

@login_required(login_url="/login/")
def videos_content(request, cid):
    header_class = "header-physics"
    course = Course.objects.get(id=cid)
    lectures = Lecture.objects.filter(course__id=cid)
    return render(request, 'landing/videos_content.html',  {'header_main': header_class, 'course': course, 'lectures': lectures})

@login_required(login_url="/login/")
def landing_physics(request):
    header_class = "header-physics"
    courses = Course.objects.filter(coursetype__title="Interactives")
    return render(request, 'landing/physics.html', {'header_main': header_class, 'courses': courses})

@login_required(login_url="/login/")
def physics_content(request, cid):
    header_class = "header-physics"
    coursecontent = Course.objects.get(id=cid)
    lectures = Lecture.objects.filter(course__id=cid)
    allowed = True

    if coursecontent.subscriptionReq == False:
        print("SUB NOT REQUIREED:")
        return render(request, 'landing/physics_content.html',  {'header_main': header_class, 'course': course, 'lectures': lectures, 'allowed': allowed})
    else:
        print("SUB REQUIREED:")
        studentCourses = StudentEnlistedCourse.objects.filter(user_id=request.user.id)   
        if len(studentCourses) == 0:
            allowed = False
            print("NOT ALLOWED")    
        else:
            for course in studentCourses:
                print(course)
                if course.course.id == cid:
                    print("ALLOWED")
                    allowed= True                    
                else:
                    allowed= False
                    print("NOT ALLOWED")

        return render(request, 'landing/physics_content.html',  {'header_main': header_class, 'course': coursecontent, 'lectures': lectures, 'allowed': allowed})

@login_required(login_url="/login/")
def student_profile(request):
    available_credit = 0.00
    subscribed_fees = 0.00
    subscriptions = StudentEnlistedCourse.objects.filter(user_id=request.user.id)
    for subs in subscriptions:
        subscribed_fees += subs.course.fee
    wallets = StudentWallet.objects.filter(user_id=request.user.id)
    for wallet in wallets:
        available_credit += wallet.key.amount

    available_credit = available_credit - subscribed_fees

    courses = StudentEnlistedCourse.objects.filter(user_id=request.user.id)
    return render(request, 'landing/profile.html', {'available_credit': available_credit, "courses":courses})

@login_required(login_url="/login/")
def add_fund(request):
    return render(request, 'landing/addfund.html', {'data': ""})

@login_required(login_url="/login/")
def wallet_recharge(request):
    post_data = request.POST
    user = request.user
    print(post_data['code'])
    try:
        key = SubsciptionKey.objects.get(shortKey=post_data['code'])
        print(key.active_status)
        print(key)
        if key.active_status == False:
            wallet = StudentWallet(
                user = user,
                key = key
            )

            wallet.save()
            key.active_status = True
            key.save()
            msg = "YOUR PROFILE HAS BEEN CREDIT WITH THE CODE AMOUNT {}".format(key.amount)
            return render(request, 'landing/subscribe.html', {'msg': msg})
        else:
            msg = "YOUR SUBSCRIPTION CODE IS ALREADY USED. PLEASE CHECK BACK WITH AUTHORIZED PERSON WITH THE CODE"
            return render(request, 'landing/subscribe.html', {'msg': msg})
    except SubsciptionKey.DoesNotExist:
        msg = "YOUR SUBSCRIPTION CODE IS NOT CORRECT. PLEASE CHECK BACK WITH AUTHORIZED PERSON WITH THE CODE"
        return render(request, 'landing/subscribe.html', {'msg': msg})

    key = SubsciptionKey.objects.get(shortKey=post_data['code'])
    

@login_required(login_url="/login/")
def subscribe(request, cid):
    available_credit = 0.00
    subscribed_fees = 0.00
    subscriptions = StudentEnlistedCourse.objects.filter(user_id=request.user.id)
    for subs in subscriptions:
        subscribed_fees += subs.course.fee
    wallets = StudentWallet.objects.filter(user_id=request.user.id)
    for wallet in wallets:
        available_credit += wallet.key.amount

    available_credit = available_credit - subscribed_fees
    
    course = Course.objects.get(id=cid)
    msg = ""
    disabled = False
    if available_credit >= course.fee:
        msg = "You have Enough Credit to Subscribe to this course"
        disabled = False
    else:
        msg = "Your Credit is not Enough for This Course please Recharge Your Profile Credit"
        disabled = True
    return render(request, 'landing/coursesubscription.html', {"course": course, "credit": available_credit, "msg": msg, "disabled": disabled})

def confirmSubscription(request, cid):
    course = Course.objects.get(id=cid)
    enlist = StudentEnlistedCourse(
        user = request.user,
        course = course
    )

    enlist.save()
    msg = "Congrats! You Have subscribed to this course. Please visit other courses for your necessity"

    return render(request, 'landing/confirmsubscription.html', {"msg": msg})

def articleIndex(request):
    return render(request, 'eskayadmin/articles.html', {'data': ""})

def videoIndex(request):
    return render(request, 'eskayadmin/videos.html', {'data': ""})

def physicsIndex(request):
    return render(request, 'eskayadmin/physics.html', {'data': ""})


def courseIndex(request):
    courses = Course.objects.all()
    lectures = Lecture.objects.all()
    course_types = CourseType.objects.all()
    
    return render(request, 'eskayadmin/courses.html', {'courses': courses, 'lectures': lectures, 'coursetypes': course_types})

def addCourse(request):
    post_data = request.POST
    file_data = request.FILES
    subscriptionReq = False
    print(post_data)
    print(file_data)

    req = post_data['subscriptionReq']
    if req == "1":
        subscriptionReq = True

    coursetype = CourseType.objects.get(id=post_data['coursetype'])
    
    course = Course(
        title=post_data['title'],
        detail=post_data['detail'],
        fee=post_data['fee'],
        subscriptionReq=subscriptionReq,
        coursetype=coursetype,
        thumb=file_data['thumb']
    )

    course.save()

    return redirect('courseindex')

def addCourseType(request):
    post_data = request.POST
    coursetype = CourseType(
        title = post_data['title']
    )

    coursetype.save()
    return redirect('courseindex')

def addLecture(request):
    post_data = request.POST
    file_data = request.FILES
    parent_dir = "/"

    try:
        content = file_data['zipcontent']

        content_dir_name = os.path.basename(content.name)[:-4]
        dir_name = "interactives"
        path = os.path.join(settings.MEDIA_ROOT, dir_name) 
        print(path)
        if os.path.exists(path):
            print("Path exists")
        else:
            os.mkdir(path)
        
        os.chdir(path)
        index_source = settings.MEDIA_URL + dir_name + "/" + content_dir_name + "/index.html"

        with zipfile.ZipFile(content) as f:
            f.extractall()
    except:
        index_source = ""

    course = Course.objects.get(id=post_data['course'])

    lecture = Lecture(
        title = post_data['title'],
        detail = post_data['detail'],
        videoUrl = post_data['videoUrl'],
        zipurl = index_source,
        course = course,
        thumb = file_data['thumb']
    )

    lecture.save()
    return redirect('courseindex')

def deleteLecture(request, lid):
    lecture = Lecture.objects.get(id=lid)
    lecture.delete()
    return redirect('courseindex')

def filterCourse(request):
    print("inside filter")
    get_data = request.GET
    data = get_data.get('type')
    subscriptionReq = False
    if data == "2":
        subscriptionReq = True

    courses = Course.objects.filter(subscriptionReq=subscriptionReq)
    print(courses)
    return render(request, 'ajax/courses.html', {"courses": courses})

def subscriptionToggle(request, cid):
    pass

def subscriptionKeyList(request):
    keys = SubsciptionKey.objects.all()
    return render(request, 'eskayadmin/keylist.html', {"keys": keys})

def generateKeys(request):
    post_data = request.POST
    iterator = post_data['iterator']
    today = datetime.date.today()
    year = today.year
    for i in range(int(iterator)):
        generator = get_random_string(7)
        code = "ESK" + generator + str(year)[-2:]
        subscriptionkey = SubsciptionKey(
            shortKey=code,
            amount=post_data['amount']
        )
        subscriptionkey.save()

    return redirect('subscriptionkeylist')

def exportCsvKeys(request):
    keys = SubsciptionKey.objects.filter(active_status=False)
    key_vals = keys.values_list('subscriptionKey','shortKey', 'amount')

    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=SubscriptionKeys.csv'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Code', 'Amount'])
    for val in key_vals:
        writer.writerow(val)

    print(writer)
    return response

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
            alert = "Username or Password is not Correct"
            return render(request, 'login.html', {'alert': alert})
        else:
            auth_login(request, user)
            try:
                print("printing USER AGENT")
                print(request.user_agent.device)
                print(request.user_agent.device.family)
                print(request.user_agent.os)
                print(request.user_agent.os.family)
                print(request.user_agent.os.version)
            except:
                pass

            if user.is_superuser:
                return redirect('home')
            else:
                return redirect('/')
    else:
        alert = "Either username or password is empty"
        return render(request, 'login.html', {'alert': alert})
        
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
            profile = request.user.student
            institutes = []
            countries = Country.objects.all()

            for country in countries:
                universities = StudentUniversityIndex.objects.filter(university__country__id=country.id).filter(student__id=request.user.student.id)
                if universities.count() != 0:
                    content = {
                        'country': country.name,
                        'short': country.short,
                        'id': country.id,
                        'data': universities
                    }
                    institutes.append(content)
                else:
                    content = {
                        'country': country.name,
                        'short': country.short,
                        'id': country.id,
                        'data': None
                    }
                    institutes.append(content)
            return render(request, 'index_student.html', {'directories': directories, 'student': profile, 'institutes': institutes})

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

        title = "New Student Created"
        description = "A new student has been registered to the System."
        link = f'<a href="/studentdetail/{student.id}">Student link</a>'

        log = SystemLog(
            title = title,
            description = description,
            link = link
        )

        log.save()

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

        unique_id = "STD" + str(student.id)

        info = PersonalInfo(
            student=student,
            unique_id=unique_id,
        )

        info.save()

        title = "New Student Created"
        description = "A new student has been registered to the System."
        link = f'<a href="/studentdetail/{student.id}">Student link</a>'

        log = SystemLog(
            title = title,
            description = description,
            link = link
        )

        log.save()

        return redirect('success')

def resetPassword(request):
    return render(request, "passwordreset.html")

def changePassword(request):
    user = request.user
    post_data = request.POST

    if post_data['pass'] != post_data['pass_conf']:
        alert = "Please enter same password for both input"
        return render(request, 'passwordreset.html', {"alert": alert})
    else:
        user.set_password(post_data['pass'])
        user.save()

        title = "Password Change"
        description = "A Student Has Changed his/her password."
        link = f'<a href="/studentdetail/{request.user.student.id}">Student link</a>'

        log = SystemLog(
            title = title,
            description = description,
            link = link
        )

        log.save()
        logout(request)
        return redirect('login')

def studentUpdate(request):
    post_data = request.POST
    student = Student.objects.get(id=post_data['sid'])
    info = PersonalInfo.objects.get(student=student)
    file_data = request.FILES

    info.passport = post_data['passport']
    info.father = post_data['father']
    info.mother = post_data['mother']
    info.father_mobile = post_data['parent_phone']
    info.mother_mobile = post_data['parent_phone']
    info.parent_email = post_data['parent_email']
    info.street_1 = post_data['street_1']
    info.street_2 = post_data['street_2']
    info.city = post_data['city']
    info.zip_code = post_data['zip_code']
    info.country = post_data['country']
    info.dob = post_data['dob']
    info.blood_group = post_data['blood_group']
    info.photo=file_data['photo']

    info.save()

    title = "Student Profile Update"
    description = "A Student Has Updated his/her profile."
    link = f'<a href="/studentdetail/{student.id}">Student link</a>'

    log = SystemLog(
        title = title,
        description = description,
        link = link
    )

    log.save()

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
        alert="Counselor Already Exists"
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

        title = "Counselor Created"
        description = "A New Counselor Has been created to the System"
        link = f'<a href="/teacherdetail/{teacher.id}">Counselor link</a>'

        log = SystemLog(
            title = title,
            description = description,
            link = link
        )

        log.save()
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

    institutes = []
    countries = Country.objects.all()

    for country in countries:
        universities = StudentUniversityIndex.objects.filter(university__country__id=country.id).filter(student__id=sid)
        if universities.count() != 0:
            content = {
                'country': country.name,
                'short': country.short,
                'id': country.id,
                'data': universities
            }
            institutes.append(content)
        else:
            content = {
                'country': country.name,
                'short': country.short,
                'id': country.id,
                'data': None
            }
            institutes.append(content)

    social_data = Social.objects.filter(user_id=student.user.id)
    if len(social_data) > 0:
        social = social_data[0]
        print(social)
    else:
        social = {'fb': None, 'skype': None, 'linkedin': None}
    
    return render(request, 'student_detail.html', {'student': student, 'teachers': teachers, 'info': info, 'universities': universities, 'indexs': indexs, 'files': files, 'institutes': institutes, 'social': social})

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

        title = "New Student Created"
        description = "A new student has been registered to the System."
        link = f'<a href="/studentdetail/{student.id}">Student link</a>'

        log = SystemLog(
            title = title,
            description = description,
            link = link
        )

        log.save()

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

    title = "A New Country Added"
    description = f"{country.name} is added to the Country list for the system to appear in application functionalities."
    link = f'<a href="/countries">Country list</a>'

    log = SystemLog(
        title = title,
        description = description,
        link = link
    )

    log.save()
    
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

    title = "New University Added"
    description = f"{university.name} has been added to the University List."
    link = f'<a href="/unidetail/{university.id}">University link</a>'

    log = SystemLog(
        title = title,
        description = description,
        link = link
    )

    log.save()
    return redirect('universities')

def deleteUniversity(request, uid):
    uni = University.objects.get(id=uid)
    name = uni.name
    uni.delete()

    title = "University Deleted"
    description = f"{name} has been deleted from the System"
    link = None

    log = SystemLog(
        title = title,
        description = description,
        link = link
    )

    log.save()

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

    title = "New Directory Created"
    description = f"{directory.title} has been added to the directory list for file uploads."
    link = f'<a href="/directories">Directory list</a>'

    log = SystemLog(
        title = title,
        description = description,
        link = link
    )

    log.save()

    return redirect('directories')

def statusUpdateDirectory(request, did, status):
    directory = Directory.objects.get(id=did)
    if status == "activate":
        directory.status = True
    elif status == "deactivate":
        directory.status = False

    directory.save()

    title = "Directory Status"
    description = f"{directories.title} status has been udpated"
    link = f'<a href="/directories">Directory Link</a>'

    log = SystemLog(
        title = title,
        description = description,
        link = link
    )

    log.save()

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

    title = "New Qualification Added"
    description = f"{qual.title} has been added to the Qualifaction list."
    link = f'<a href="/qualifications">Qualification list</a>'

    log = SystemLog(
        title = title,
        description = description,
        link = link
    )

    log.save()

    return redirect('qualifications')
    

def teacherDetail(request, tid):
    teacher = Teacher.objects.get(id=tid)
    data = Student.objects.filter(assigned_teacher__id=tid)

    social_data = Social.objects.filter(user_id=teacher.user.id)
    if len(social_data) > 0:
        social = social_data[0]
        print(social)
    else:
        social = {'fb': None, 'skype': None, 'linkedin': None}
    return render(request, 'detail_teacher.html', {'teacher': teacher, 'data': data, 'social': social})
    
def assignTeacher(request):
    post_data = request.POST
    student = Student.objects.get(id=post_data['sid'])
    teacher = Teacher.objects.get(id=post_data['tid'])
    student.assigned_teacher = teacher

    student.save()

    sid = post_data['sid']

    title = "Teacher Assigned"
    description = "Description"
    link = f'<a href="/studentdetail/{sid}">Link</a>'

    log = SystemLog(
        title = title,
        description = description,
        link = link
    )

    log.save()

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

    title = "University Suggested"
    description = f"{student.name} has been suggested universities by {request.user.teacher.name}"
    link = f'<a href="/studentdetail/{student.id}">Student link</a>'

    log = SystemLog(
        title = title,
        description = description,
        link = link
    )

    log.save()   

    return redirect('studentdetail', post_data['sid'])

def deleteSuggestion(request, iid):
    idx = StudentUniversityIndex.objects.get(id=iid)
    sid = idx.student.id
    idx.delete()

    return redirect('studentdetail', sid)


# STUDENT AREA

def myProfile(request):
    user_type = None

    social_data = Social.objects.filter(user_id=request.user.id)

    if len(social_data) > 0:
        social = social_data[0]
        print(social)
    else:
        social = {'fb': None, 'skype': None, 'linkedin': None}

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

        institutes = []
        countries = Country.objects.all()

        for country in countries:
            universities = StudentUniversityIndex.objects.filter(university__country__id=country.id).filter(student__id=student.id)
            if universities.count() != 0:
                content = {
                    'country': country.name,
                    'short': country.short,
                    'id': country.id,
                    'data': universities
                }
                institutes.append(content)
            else:
                content = {
                    'country': country.name,
                    'short': country.short,
                    'id': country.id,
                    'data': None
                }
                institutes.append(content)

        info = PersonalInfo.objects.get(student=student)

        # social = Social.objects.filter(user_id=request.user.id)[0]
        # print(social)
        return render(request, 'student_detail.html', {'student': student, 'teachers': teachers, 'universities': universities, 'indexs': indexs, 'files': files, 'info': info, 'institutes': institutes, 'social': social})
    except:
        teacher = request.user.teacher
        data = Student.objects.filter(assigned_teacher__id=request.user.teacher.id)
        # social = Social.objects.filter(user=request.user)[0]
        return render(request, 'detail_teacher.html', {'teacher': teacher, 'data': data, 'social':social})
        
def studentUnis(request):
    get_data = request.GET    
    cid = get_data.get('cid')
    unis = University.objects.filter(country__id=cid)
    country = Country.objects.get(id=cid)
    return render(request, 'ajax/uni_list.html', {'unis': unis, 'country': country})

# def postStudentUni(request):
#     post_data = request.POST
#     print(request.POST)
#     student = Student.objects.get(id=post_data['sid'])
#     unis = post_data.getlist('unis')

#     for uni in unis:
#         university = University.objects.get(id=uni)
#         studentUni = StudentUniversityIndex(
#             student = student,
#             university = university
#         )

#         studentUni.save()
    
#     return redirect('myprofile')


# def studentUnis(request):
#     get_data = request.GET    
#     cid = get_data.get('cid')
#     unis = University.objects.filter(country__id=cid)
#     return render(request, 'ajax/uni_list.html', {'unis': unis})

def postStudentUni(request):
    post_data = request.POST
    print(request.POST)
    student = Student.objects.get(id=post_data['sid'])
    unis = post_data.getlist('unis')

    for uni in unis:
        university = University.objects.get(id=uni)
        studentUni = StudentUniversityIndex(
            student = student,
            university = university
        )

        studentUni.save()

    title = "Student University Selected"
    description = f"{student.name} has Selected University"
    link = f'<a href="/studentdetail/{student.id}">Student link</a>'

    log = SystemLog(
        title = title,
        description = description,
        link = link
    )

    log.save()

    return redirect('myprofile')

# def studentUnis(request):
#     get_data = request.GET    
#     cid = get_data.get('cid')
#     unis = University.objects.filter(country__id=cid)
#     return render(request, 'ajax/uni_list.html', {'unis': unis})

# def postStudentUni(request):
#     post_data = request.POST
#     print(request.POST)
#     student = Student.objects.get(id=post_data['sid'])
#     unis = post_data.getlist('unis')

#     for uni in unis:
#         university = University.objects.get(id=uni)
#         studentUni = StudentUniversityIndex(
#             student = student,
#             university = university
#         )

#         studentUni.save()

#     return redirect('myprofile')

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

    title = "Student Uploaded Content"
    description = f"{student.name} has Uploaded Content in {directory.title}"
    link = f'<a href="/studentdetail/{student.id}">Student link</a>'

    log = SystemLog(
        title = title,
        description = description,
        link = link
    )

    log.save()

    return redirect('directoryindex', post_data['did'])

def updateSocial(request):
    post_data = request.POST

    social_data = Social.objects.filter(user_id=request.user.id)

    if len(social_data) > 0:
        social = social_data[0]

        social.fb = post_data['fb']
        social.skype = post_data['skype']
        social.linkedin = post_data['linkedin']

        social.save()
    
    else:
        social = Social(
            user = request.user,
            fb = post_data['fb'],
            skype = post_data['skype'],
            linkedin = post_data['linkedin']
        )

        social.save()

    try:
        student = request.user.student

        title = "Social Updated"
        description = f"{student.name} has updated his Social Information"
        link = f'<a href="/studentdetail/{student.id}">Student link</a>'

        log = SystemLog(
            title = title,
            description = description,
            link = link
        )

        log.save()

        return redirect('studentdetail', student.id)
    except:
        teacher = request.user.teacher

        title = "Social Update"
        description = f"{teacher.name} has updated his Social Information"
        link = f'<a href="/teacherdetail/{teacher.id}">Counselor link</a>'

        log = SystemLog(
            title = title,
            description = description,
            link = link
        )

        log.save()

        return redirect('teacherdetail', teacher.id)


def systemLog(request):
    logs = SystemLog.objects.all()

    return render(request, 'systemlog.html', {'logs': logs})


# ALL SUBSCRIPTION PLAN

def articles(request):
    articles = Article.objects.all()

    return render(request, 'subscription/article.html', {'articles': articles})

def courses(request):
    courses = Course.objects.all()

    return render(request, 'subscription/article.html', {'courses': courses})

def lecture(request, cid):
    lectures = Lecture.objects.filter(course___=cid)

    return render(request, 'subscription/article.html', {'lectures': lectures})

def lectureDetail(request, did):
    lecture = Lecture.objects.get(id=did)

    return render(request, 'subscription/article.html', {'lecture': lecture})

def lectureMedia(request):
    freelectures = LectureMedia.objects.all()

    return render(request, 'subscription/article.html', {'freelectures': freelectures})

def activateSubscription(request):
    user = request.user
    post_data = request.POST

    code = post_data['code']

    if SubscriptionCode.objects.filter(code=code).exists():
        code_obj = SubscriptionCode.object.get(code=code)
        if code.status:
            msg = "Your Code is already activated"
        else:
            msg = "Your Code has been actiavated"
            usersubscription= UserSubscription(
                user = user,
                subscriptionStatus = True,
                subscriptionType = code_obj.ref
            )

            user.save()
            code_obj.user = usersubscription
            code_obj.status = False
            code_obj.save()
    else:
        msg = "CODE IS INVALID"