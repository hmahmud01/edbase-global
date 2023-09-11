from django.contrib import admin

from .models import *


admin.site.register([InteractiveModule, TopicInformation, StudentEnlistedBundles, Bundle, BundleContent, BundleWallet, Topic, TopicContent, TopicQualifications, TopicExercise, Qualification, Teacher, Student, PersonalInfo, Subject, Country, University, Directory, Content, DirectoryIndex, SystemLog, Social,CourseType, Course, Lecture, LectureMedia, SubsciptionKey, ArticleCategory, Article])