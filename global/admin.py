from django.contrib import admin

from .models import *


admin.site.register([Qualification, Teacher, Student, PersonalInfo, Country, University, Directory, Content, DirectoryIndex, SystemLog, Social])