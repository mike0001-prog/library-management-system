from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("user/<int:user_id>/<str:first_name>/<str:last_name>/", views.users_view, name="user_view"),
    path("about/", views.about, name="about"),
    path("users/<int:department>/", views.department_users, name="department_user"),
    path("fines/", views.fines, name="fine"),
    path("activate_or_dectivate/", views.activate_or_dectivate_user, name="activate_deactivate"),
]
