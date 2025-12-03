from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView,PasswordResetDoneView,PasswordResetCompleteView
urlpatterns = [
    path("register/", views.register, name="register"),
    path("register/student/", views.student_register, name="student_register"),
    path("register/staff/", views.staff_register, name="staff_register"),
    path("register/department/", views.department_form, name="department"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("change_password/", views.change_password, name="change_pwd"),
    path("reset_password/", views.CustomPasswordReset.as_view() , name="forgot_pwd"),
    path("reset_password/done/", PasswordResetDoneView.as_view(template_name="access/password_reset_done.html") , name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.CustomPasswordResetConfirmView.as_view() , name="password_reset_confirm"),
    path("reset/done/", PasswordResetCompleteView.as_view(template_name="access/password_reset_completed.html") , name="password_reset_complete"),


]
