from django.db import models
from django.contrib.auth.models import User
import uuid


class Subscription(models.Model):
    title = models.CharField(max_length=128)
    cost = models.FloatField()
    # models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    subscriptionStatus = models.BooleanField(default=False)
    subscriptionType = models.OneToOneField(Subscription, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.subscriptionStatus

class SubscriptionCode(models.Model):
    code = models.CharField(max_length=256)
    ref = models.OneToOneField(Subscription, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    timePeriod = models.IntegerField(default=0)
    user = models.OneToOneField(UserSubscription, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.code

class Qualification(models.Model):    
    title = models.CharField(max_length=128)
    level = models.CharField(max_length=128)

    def __str__(self):
        return self.title

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, null=True, blank=True)    
    phone = models.CharField(max_length=128, null=True, blank=True)  
    email = models.CharField(max_length=128, null=True, blank=True) 
    level = models.CharField(max_length=128, null=True, blank=True)
    qualification = models.ForeignKey(Qualification, related_name='teacher_qualification', on_delete=models.CASCADE)
    user_type = models.CharField(max_length=64, default='teacher', blank=True, null=True)
    photo = models.FileField('teacher_image', upload_to='teacher_photos', blank=True, null=True)
    status = models.BooleanField(default=True)
    password_change = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
    short = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.short

class University(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    country = models.ForeignKey(Country, related_name='university_country', on_delete=models.CASCADE)
    url = models.CharField(max_length=128, null=True, blank=True)
    image = models.FileField('university_image', upload_to='university', blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=64, default='student', blank=True, null=True)
    status = models.BooleanField(default=True)
    password_change = models.BooleanField(default=False)
    name = models.CharField(max_length=128, null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    guardian_mobile = models.CharField(max_length=11, null=True, blank=True)
    email = models.EmailField(max_length=128, null=True, blank=True)
    school = models.CharField(max_length=128, null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)    
    qualification = models.ForeignKey(Qualification, related_name='student_qualification', on_delete=models.CASCADE)
    assigned_teacher = models.OneToOneField(Teacher, related_name='assigned_teacher', on_delete=models.CASCADE, null=True)
    taken_care = models.BooleanField(default=False)
    visited = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

class PersonalInfo(models.Model):
    student = models.OneToOneField(Student, related_name='student_personal_info', on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=26, null=True, blank=True)
    acceptance = models.BooleanField(default=False, null=True, blank=True)
    passport = models.CharField(max_length=128, null=True, blank=True)
    father = models.CharField(max_length=128, null=True, blank=True)
    mother = models.CharField(max_length=128, null=True, blank=True)
    father_mobile = models.CharField(max_length=128, null=True, blank=True)
    mother_mobile = models.CharField(max_length=128, null=True, blank=True)
    parent_email = models.EmailField(max_length=128, null=True, blank=True)
    street_1 = models.CharField(max_length=128, null=True, blank=True)
    street_2 = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    zip_code = models.CharField(max_length=128, null=True, blank=True)
    country = models.CharField(max_length=128, null=True, blank=True)
    dob = models.CharField(max_length=128, null=True, blank=True)
    blood_group = models.CharField(max_length=128, null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    photo = models.FileField('student_image', upload_to='student_photos', blank=True, null=True)

    def __str__(self):
        return self.student.name

class Social(models.Model):
    user = models.OneToOneField(User, related_name='user_social', on_delete=models.CASCADE)
    fb = models.TextField(null=True, blank=True)
    skype = models.TextField(null=True, blank=True)
    linkedin = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user.id)

class StudentCountryIndex(models.Model):
    student = models.ForeignKey(Student, related_name='student_country', on_delete=models.CASCADE)
    country = models.ForeignKey(Country, related_name='ctry_student', on_delete=models.CASCADE)

    def __str__(self):
        return self.student.name

class StudentUniversityIndex(models.Model):
    student = models.ForeignKey(Student, related_name='student_university', on_delete=models.CASCADE)
    university = models.ForeignKey(University, related_name='uni_student', on_delete=models.CASCADE)

    def __str__(self):
        return self.student.name

class Directory(models.Model):
    title = models.CharField(max_length=64, null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Content(models.Model):
    file_content = models.FileField('app_files', upload_to='content', blank=True, null=True)

    def __str__(self):
        return self.file

class DirectoryIndex(models.Model):
    directory = models.ForeignKey(Directory, related_name='directory', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='directory_student', on_delete=models.CASCADE)
    content = models.ForeignKey(Content, related_name='directory_content', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.directory.title

    def fileName(self):
        return self.content.file_content
        # name = self.content.file_content.rsplit("/")
        # return name[1]

class SystemLog(models.Model):
    title = models.CharField(max_length=64, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    seen = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title

# TODO
# DIRECTORY CONTENT CLASS NEED TO REWORK
# UNIVERSITY STATUS FIELD NEEDED

# TODO
# REWORKING ON SUBSCRIPTION PART

class CourseType(models.Model):
    title = models.CharField(max_length=256)
    def __str__(self):
        return self.title

class SubsciptionKey(models.Model):
    subscriptionKey=models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    shortKey = models.CharField(max_length=12, null=True, unique=True)
    amount = models.FloatField()
    active_status = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.shortKey

class Course(models.Model):
    title = models.CharField(max_length=256)
    detail = models.TextField()
    fee = models.FloatField()
    subscriptionReq = models.BooleanField(default=False)
    coursetype = models.ForeignKey(CourseType, on_delete=models.CASCADE)
    thumb = models.FileField('course_image', upload_to='courses', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title

class Lecture(models.Model):
    title = models.CharField(max_length=256)
    detail = models.TextField()
    videoUrl = models.CharField(max_length=256, null=True, blank=True)
    zipContent = models.FileField('interactives', upload_to='interactives', null=True, blank=True)
    zipurl = models.CharField(max_length=256, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    thumb = models.FileField('lecture_image', upload_to='lectures', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title

class LectureMedia(models.Model):
    title = models.CharField(max_length=256)
    detail = models.TextField()
    videoUrl = models.CharField(max_length=256)
    thumb = models.FileField('free_lecture_image', upload_to='free_lectures', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title

class ArticleCategory(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title
        
class Article(models.Model):
    title = models.CharField(max_length=128)
    detail = models.TextField()
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE)
    thumb = models.FileField('article_image', upload_to='articles', blank=True, null=True)

    def __str__(self):
        return self.title

class StudentWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.OneToOneField(SubsciptionKey, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        msg = "user {} credited to {} for {} dollars."
        done = msg.format(self.user.username, self.key.shortKey, self.key.amount)
        return done

class StudentEnlistedCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        msg = "user {} subscribed to {}"
        done = msg.format(self.user.username, self.course.title)
        return done


# COURSE HIERERCHY MODELS B -> L -> S -> T
class Batch(models.Model):
    title = models.CharField(max_length=64)
    detail = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title

class Level(models.Model):
    title = models.CharField(max_length=64)
    detail = models.TextField(null=True, blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title

class Subject(models.Model):
    title = models.CharField(max_length=64)
    detail = models.TextField(null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

class Topic(models.Model):
    