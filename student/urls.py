from django.urls import path
from . import views

urlpatterns = [
    path("user_index/", views.user_index, name="user_index"),
    path("borrowed_book_user/<int:user_id>/", views.user_borrowed_book, name="user_borrowed_book"),
    path("students/", views.co_student, name="students"),
    path("each_user/<int:user_id>/", views.each_student, name="each_student"),
    path("books/", views.books, name="books"),
    path("forbidden!/", views.Forbidden, name="forbidden"),
    path("mystat/", views.my_stat, name="mystat"),
]
