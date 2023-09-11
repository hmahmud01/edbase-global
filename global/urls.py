from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='site'),
    path('home/', views.home, name='home'),
    path('videos/', views.landing_videos, name='videos'),
    path('subjects/<int:sid>', views.landing_subjects, name='subjects'),
    path('videostopic/<int:tid>', views.landing_subjectTopics, name="videostopic"),
    path('videoscontent/<int:cid>/', views.videos_content, name='videoscontent'),
    path('physics/', views.landing_physics, name='physics'),
    path('physicscontent/<int:cid>/', views.physics_content, name='physicscontent'),
    path('profile/', views.student_profile, name='profile'),
    path('addfund/', views.add_fund, name='addfund'),
    path('walletReceharge/', views.wallet_recharge, name='recharge'),
    path('bundlesubscription/', views.bundle_subscription, name='bundlesubscription'),
    path('subscribe/<int:cid>/', views.subscribe, name='subscribe'),
    path('confirmsubscription/<int:cid>', views.confirmSubscription, name='confirmsubscription'),
    path('articleindex/', views.articleIndex, name='articleindex'),
    path('videoindex/', views.videoIndex, name='videoindex'),
    path('physicsindex/', views.physicsIndex, name='physicsindex'),
    path('courseindex/', views.courseIndex, name='courseindex'),
    path('addcourse/', views.addCourse, name='addcourse'),
    path('addcoursetype/', views.addCourseType, name='addcoursetype'),
    path('addlecture/', views.addLecture, name='addlecture'),
    path('deletelecture/<int:lid>', views.deleteLecture, name='deletelecture'),
    path('filtercourse/', views.filterCourse, name='filtercourse'),
    path('subscriptiontoggle/<int:cid>/', views.subscriptionToggle, name='subscriptiontoggle'),
    path('subscriptionkeylist/', views.subscriptionKeyList, name='subscriptionkeylist'),
    path('generatekeys/', views.generateKeys, name='generatekeys'),
    path('csvkeys', views.exportCsvKeys, name='csvkeys'),
    path('userlogout/', views.userLogout, name='userlogout'),
    path('login/', views.login, name='login'),
    path('verifylogin/', views.verifyLogin, name='verifylogin'),
    path('register/', views.register, name='register'),
    path('registerv2/', views.signUp_v2, name='registerv2'),
    path('resetpassword', views.resetPassword, name='resetpassword'),
    path('changepassword', views.changePassword, name='changepassword'),
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
    path('addboard', views.addBoard, name='addboard'),
    path('studentdetail/<int:sid>/', views.studentDetail, name='studentdetail'),
    path('teacherdetail/<int:tid>/', views.teacherDetail, name='teacherdetail'),
    path('assignteacher/', views.assignTeacher, name='assignteacher'),
    path('suggestuni/', views.suggestUni, name='suggestuni'),
    path('deletesuggestion/<int:iid>', views.deleteSuggestion, name='deletesuggestion'),
    path('myprofile/', views.myProfile, name='myprofile'),
    path('studentunis/', views.studentUnis, name='studentunis'),
    path('poststudentuni/', views.postStudentUni, name='poststudentuni'),
    path('directoryindex/<int:did>', views.directoryIndex, name='directoryindex'),
    path('uploadcontent/', views.uploadContent, name='uploadcontent'),
    path('updatesocial/', views.updateSocial, name='updatesocial'),
    path('systemlog/', views.systemLog, name='systemlog'),
    path('articles/', views.articles, name='articles'),
    path('checkout/', views.checkout, name="checkout"),
    path('cart/', views.cart, name="cart"),
    path('pricing/', views.pricing, name="pricing"),
    path('batchlevel/', views.batchlevel, name="batchlevel"),
    path('addbatch/', views.addBatch, name="addbatch"),
    path('addlevel/', views.addLevel, name="addlevel"),
    path('subjecttopics/', views.subjecttopics, name="subjecttopics"),
    path('topicstatustoggle/<int:tid>', views.topicStatusToggle, name="topicstatustoggle"),
    path('addinteractive/', views.addInteractive, name="addinteractive"),
    path('showint/<int:id>/<int:tid>', views.showint, name="showint"),
    path('addsubject/', views.addSubject, name="addsubject"),
    path('addtopicmaster/', views.addTopicMaster, name="addtopicmaster"),
    path('addtopics/', views.addTopics, name="addtopics"),
    path('addtopicinfo/', views.addTopicInformation, name="addtopicinfo"),
    path('bundle/', views.bundle, name="bundle"),
    path('addbundle/', views.addBundle, name="addbundle"),
    path('unsubscribebundle/<int:bid>', views.bundle_unsubscribe, name="unsubscribebundle"),
    path('reactivebundle/<int:bid>', views.bundle_reactivate, name="reactivebundle"),
    path('addkeys/', views.addKeys, name="addkeys"),
    path('exportbundlewallets/', views.exportBundleWallets, name="exportbundlewallets"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)