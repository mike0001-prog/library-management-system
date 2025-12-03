from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from book_app.models import Book, BorrowedBook
from django.contrib.auth.models import User
from .decorators import superuser_validator
from authentication.models import UserProfile, Department
from django.http import HttpResponse
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.contrib import messages
# Create your views here.
def base(request):
    departments = Department.objects.all()
    return render(request, "front/base.html", {"departments":departments})


@login_required
@superuser_validator
def index(request):
    books = Book.objects.all()
    users = User.objects.all()
    borrowed_book = BorrowedBook.objects.all()
    depts = Department.objects.all()
    data = (
        BorrowedBook.objects.filter(is_approved=True)
        .annotate(month=TruncMonth("borrow_time"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )
    print(data)
    # Format for Chart.js
    months = [d["month"].strftime("%B %Y") for d in data]  # e.g. "August 2025"
    counts = [d["count"] for d in data]

    context = {
        "months": months,
        "counts": counts,
        "books":books, 
        "users":users, 
        "borrowed":borrowed_book, 
        "depts":depts
    }
    return render(request, "front/index.html", context)


@login_required
@superuser_validator
def users_view(request, user_id, first_name, last_name):
    user = User.objects.get(id = user_id, first_name = first_name, last_name = last_name)
    return render(request, "front/user.html", {"user":user})

def about(request):
    return render(request, "front/about.html")

def fines(request):
    borrowed_book = BorrowedBook.objects.exclude(fine=0)
    return render(request, "front/fines.html",{"books":borrowed_book})

def activate_or_dectivate_user(request):
    print(request.POST)
    try:
        if request.method == "POST":
            if request.POST["action"] == "deactivate":
                id = request.POST["uid"]
                user = User.objects.get(id=int(id))
                user.is_active = False
                user.save()
                return JsonResponse({"msg": "user deactivated","action":"deactivated"})
            else:
                id = request.POST["uid"]
                user = User.objects.get(id=int(id))
                user.is_active = True
                user.save()
                return JsonResponse({"msg": "user activated","action":"activated"})
    except Exception:
        return JsonResponse({"msg": "an error occured"})


@login_required
@superuser_validator
def department_users(request, department):
    print(department)
    try:
        departments = Department.objects.get(id = department)
        users = UserProfile.objects.filter(department = departments)
        depts = Department.objects.all()
    except Exception:
        messages.error(request,"an error occured")
        return redirect("index")
    return render(request, "front/department-user.html", {"department":users, "department_name":departments, "depts":depts})
