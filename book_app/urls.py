from django.urls import path
from . import views

urlpatterns = [
    path("BOOKS", views.books, name="BOOK"),
    path("add_book/", views.add_book, name="add_book"),
    path("delete_book/<int:book_id>/", views.delete_book, name="delete_book"),
    path("update_book/<int:book_id>/", views.update_book, name="update_book"),
    path("books/", views.book_list, name="book_list"),
    path("book/<int:book_id>/<int:isbn>/<str:book_name>/", views.book, name="book"), 
    path("borrow/<int:book_id>/<int:isbn>/", views.borrow_book, name="borrow_book"),
    path("borrowed-books/", views.borrowed_books, name="borrowed_books"),
    path("return-books/", views.return_books, name="return_books"),
]