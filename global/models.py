from django.db import models
from django.contrib.auth.models import User


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
    assigned_teacher = models.ForeignKey(Teacher, related_name='assigned_teacher', on_delete=models.CASCADE, null=True)
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
        return self.directory


# TODO
# DIRECTORY CONTENT CLASS NEED TO REWORK
# UNIVERSITY STATUS FIELD NEEDED