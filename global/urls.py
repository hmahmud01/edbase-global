from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='site'),
    path('home/', views.home, name='home'),
    path('userlogout/', views.userLogout, name='userlogout'),
    path('login/', views.login, name='login'),
    path('verifylogin/', views.verifyLogin, name='verifylogin'),
    path('register/', views.register, name='register'),
    path('registerv2/', views.signUp_v2, name='registerv2'),
    path('studentupdate/', views.studentUpdate, name='studentupdate'),
    path('success/', views.successPage, name='success'),
    path('failed/', views.failedPage, name='failed'),
    path('signupdata/', views.signupData, name='signupdata'),
    path('teachers/', views.listTeachers, name='teachers'),
    path('addteacher', views.addTeacher, name='addteacher'),
    path('students/', views.listStudents, name='students'),
    path('addstudent', views.addStudent, name='addstudent'),
    path('countries/', views.listCountries, name='countries'),
    path('addcountry/', views.addCountry, name='addcountry'),
    path('universities/', views.listUniversities, name='universities'),
    path('unidetail/<int:uid>/', views.uniDetail, name='unidetail'),
    path('deleteuni/<int:uid>', views.deleteUniversity, name='deleteuni'),
    path('loaduniversity/', views.loadUniversity, name='loaduniversity'),
    path('adduniversity', views.addUniversity, name='adduniversity'),
    path('directories/', views.listDirectory, name='directories'),
    path('adddirectory/', views.addDirectory, name='adddirectory'),
    path('statusupdate/<int:did>/<str:status>', views.statusUpdateDirectory, name='statusupdate'),
    path('qualifications/', views.listQualifications, name='qualifications'),
    path('addqualification', views.addQualification, name='addqualification'),
    path('studentdetail/<int:sid>/', views.studentDetail, name='studentdetail'),
    path('teacherdetail/<int:tid>/', views.teacherDetail, name='teacherdetail'),
    path('assignteacher/', views.assignTeacher, name='assignteacher'),
    path('suggestuni/', views.suggestUni, name='suggestuni'),
    path('deletesuggestion/<int:iid>', views.deleteSuggestion, name='deletesuggestion'),
    path('myprofile/', views.myProfile, name='myprofile'),
    path('studentunis/', views.studentUnis, name='studentunis'),
    path('poststudentuni/', views.postStudentUni, name='poststudentuni'),
    path('directoryindex/<int:did>', views.directoryIndex, name='directoryindex'),
    path('uploadcontent/', views.uploadContent, name='uploadcontent')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)