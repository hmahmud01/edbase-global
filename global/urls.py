from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('userlogout/', views.userLogout, name='userlogout'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('teachers/', views.listTeachers, name='teachers'),
    path('addteacher', views.addTeacher, name='addteacher'),
    path('students/', views.listStudents, name='students'),
    path('countries/', views.listCountries, name='countries'),
    path('addcountry/', views.addCountry, name='addcountry'),
    path('universities/', views.listUniversities, name='universities'),
    path('adduniversity', views.addUniversity, name='adduniversity')
    path('directories/', views.listDirectory, name='direcotries'),
    path('adddirectory/', views.addDirectory, name='adddirectory')
    path('qualifications/', views.listQualifications, name='qualifications'),
    path('addqualification', views.addQualification, name='addqualification'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)