from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('teachers/', views.listTeachers, name='teachers'),
    path('students/', views.listStudents, name='students'),
    path('countries/', views.listCountries, name='countries'),
    path('universities/', views.listUniversities, name='universities'),
    path('directories/', views.listDirectory, name='direcotries'),
    path('qualifications/', views.listQualifications, name='qualifications'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)