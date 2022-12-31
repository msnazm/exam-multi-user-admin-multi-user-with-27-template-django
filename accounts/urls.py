from django.urls import path,re_path
from . import views


urlpatterns = [
    path('signup/', views.SignUp, name='signup'),
    re_path(r'^(?P<pk>\d+)/signupExam/$', views.SignUpExam, name='signup_exam'),
    path('password/', views.change_password, name='change_password'),
    path('listuser/', views.ListUser, name='list_user'),
    re_path(r'^UserChangePassword/(?P<pk>\d+)/$',views.UserChangePasswordView,name='user-change-password'),
    re_path(r'^VerificationExam/$',views.VerificationExam,name='verification_exam'),
    re_path(r'^Verification/$',views.Verification,name='verification'),
    re_path(r'^UserDelete/(?P<id>\d+)/$',views.UserDeleteView,name='user_delete'),
    re_path(r'^UserPerm/(?P<id>\d+)/$',views.AddPermView,name='user_perm'),
    re_path(r'^ProfileUser/(?P<id>\d+)/$',views.ProfileUserView,name='profile_user'),
    re_path(r'^ProfileAdmin/(?P<id>\d+)/$',views.ProfileAdminView,name='profile_admin'),
    re_path(r'^(?P<pk>\d+)/LoginUserExam/$', views.loginExamUser,name='login-user-exam'),
    re_path(r'^LoginAdminExam/$', views.loginExamAdmin,name='login-admin-exam'),
    re_path(r'^LoginAdmin/$', views.loginAdmin,name='login-admin'),
    re_path(r'^(?P<pk>\d+)/LogoutUserExam/$', views.LogoutUserExam,name='loginout-user-exam'),
    re_path(r'^LogoutAdminExam/$', views.LogoutAdminExam,name='loginout-admin-exam'),
    re_path(r'^LogoutAdmin/$', views.LogoutAdmin,name='loginout-admin'),
    re_path(r'^Verifications/$', views.SignUpResend,name='adminexam_resend'),
]
