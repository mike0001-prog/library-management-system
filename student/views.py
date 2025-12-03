from django.shortcuts import render
from book_app.models import *
from authentication.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .decorators import student_validator
from django.db.models import Count,Avg
from django.db.models.functions import TruncMonth
from quiz_app.models import UserScores
@login_required
@student_validator
def user_index(request):
    book_cate = Category.objects.all()
    book = Book.objects.all()
    users = UserProfile.objects.all()

    if request.user.is_staff:
        return render(request, "user/index.html", {"book_cates":book_cate, "books":book, "users":users, "department_book":book})
    else:
        user_department = request.user.profile.department
        books_by_category = Book.objects.filter(category = Category.objects.get(title = user_department))
        return render(request, "user/index.html", {"book_cates":book_cate, "books":book, "users":users, "department_book":books_by_category})

# borrowed book
@login_required
def user_borrowed_book(request, user_id):
    user = User.objects.get(id = user_id)
    borrowed_book = BorrowedBook.objects.filter(borrower = request.user)
    for book in borrowed_book:
        print(book.borrow_time)
        
    # if borrowed_book.exists():
    return render(request, "books/borrowed_book.html", {"books":borrowed_book})
    # return render(request, "books/borrowed_book.html", {"books":"No borrowed Books"})

@login_required
def co_student(request):
    student = UserProfile.objects.all()
    return render(request, "user/student.html", {"students":student})


@login_required
def each_student(request, user_id):
    # student = User.objects.get(id = student_id, first_name = student_name)
    student = UserProfile.objects.get(user_id = user_id)
    return render(request, "user/each_user.html", {"student":student})

@login_required
# @student_validator
def books(request):
    books = Book.objects.all()
    student = UserProfile.objects.get(user = request.user)
    return render(request, "books/books.html", {"books":books, "student":student})


def Forbidden(request):
    return render(request, "user/401.html", {"msg":"You're not authorized to view this page!!"})

@login_required
def my_stat(request):
    data_1 = (
        UserScores.objects.filter(user=request.user)
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    data = (
        BorrowedBook.objects.filter(is_approved=True,borrower=request.user)
        .annotate(month=TruncMonth("borrow_time"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )
    
    # Format for Chart.js
    months = [d["month"].strftime("%B %Y") for d in data]  # e.g. "August 2025"
    counts = [d["count"] for d in data]

    months_1 = [d["month"].strftime("%B %Y") for d in data_1]  
    counts_1 = [d["count"] for d in data_1]



    data_2 = (UserScores.objects.filter(user=request.user)
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(avg=Avg("user_score"))
            .order_by("month"))
    months_2 = [d["month"].strftime("%B %Y") for d in data_2]  # e.g. "August 2025"
    avgs_2 = [d["avg"] for d in data_2]
    context = {"counts":counts,
               "months":months,
               "months_1":months_1,
               "counts_1":counts_1,
               "months_2":months_2,
               "avgs_2":avgs_2}
    return render(request, "user/mystat.html", context)