from django.contrib import admin

from .models import *


admin.site.register([TopicInformation, StudentEnlistedBundles, Bundle, BundleContent, BundleWallet, Topic, TopicContent, TopicExercise, Qualification, Teacher, Student, PersonalInfo, Country, University, Directory, Content, DirectoryIndex, SystemLog, Social,CourseType, Course, Lecture, LectureMedia, SubsciptionKey, ArticleCategory, Article])