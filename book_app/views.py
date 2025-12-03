from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, BorrowedBook
from django.http import HttpResponse
from .forms import AddBookForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from library_admin.decorators import superuser_validator
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .utils import extract_file
# Create your views here.
@login_required
def books(request):
    books = Book.objects.all()
    return render(request, "books/books.html", {"books":books})

# def add_book(request):
#     form = AddBookForm()
#     if request.method == "POST":
#         form = AddBookForm(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 print("test")
#                 pre_form = form.save(commit=False)
#                 pre_form.available_quantity = form.quantity
#                 pre_form.save()
#                 return redirect('index')
#             except Exception as e:
#                 return HttpResponse(f"Server responded with {e}")
#                 print(e)
            
#     else:
#         return render(request, "forms/add_book.html", {"form":form})
    
@login_required
@superuser_validator
def add_book(request):
    form = AddBookForm()
    if request.method == "POST":
        if request.POST["type"] == "single":
            print(request.POST)
            form = AddBookForm(request.POST, request.FILES)
            if form.is_valid():
                preform = form.save()
                preform.available_quantity = request.POST['quantity']
                preform.save()
                messages.success(request, "book added sucessfully")
            return redirect('add_book')
        elif request.POST["type"] == "multiple":
            # print(request.POST,request.FILES)
            if form.is_valid():
                if  request.FILES:
                    try:
                        file = request.FILES["csv_file"]
                        images = request.FILES["zip_file"]
                        extract_file(request,file,images)
                    except Exception:
                        messages.error(request,"error extracting files")
                        return redirect('add_book')
                    return redirect('add_book')
                else:
                    messages.error(request,"cannot submit empty fields")
                    return redirect('add_book')
            else:
                messages.error(request,"all fields are required")
                return redirect('add_book')
            
    else:
        return render(request, "forms/add_book.html", {"form":form})
    


@login_required
@superuser_validator
def delete_book(request, book_id):
    book = Book.objects.get(id = book_id)
    book.delete()
    return redirect("index")

@login_required
@superuser_validator
def update_book(request, book_id):
    book = get_object_or_404(Book, id = book_id)
    form = AddBookForm(request.POST or None, instance = book)
    if request.method == "POST":
        print(request.FILES)
        form = AddBookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            try:
                form.save()
                messages.add_message(request, 2, "Updated Successfully!")
                return redirect("book_list")
            except Exception as e:
                return HttpResponse(f"server responded with {e}")
    return render(request, "forms/update_book.html", {"form":form})


def borrow_book(request, book_id, isbn):
    book = Book.objects.get(id = book_id, isbn = isbn)
    if book.is_available:
        if request.user.is_superuser:
            return HttpResponse("Admin can't borrow book")
        else:
            borrowed = BorrowedBook(book = book, borrower = request.user)
            borrowed.due_date = timezone.now() + timedelta(hours=168)
            borrowed.save()
            book.available_quantity -= 1
            book.save()
            messages.success(request,"Book successfully borrowed visit library for approval")

        return redirect("user_index")
    messages.warning(request,"Book not available check back")
    return redirect("user_index")

@login_required
def book_list(request):
    book = Book.objects.all()
    return render(request, "front/book_list.html", {"books":book})

@login_required
# @superuser_validator
def book(request, book_id, isbn, book_name):
    condition = True
    borrowedbook =  BorrowedBook.objects.filter(borrower=request.user)
    
    
    print(type(borrowedbook))
    # checks if the user have borrowed a book before
    print(len(borrowedbook))
    
    # checks if all borrowed books are returned
    if borrowedbook:
        for book in borrowedbook:
            if book.is_returned:
                condition = True
            else:
                condition = False
  
    book = Book.objects.get(id = book_id, isbn = isbn, name = book_name)
    is_available=book.is_available()
    print(is_available)
    return render(request, "front/book.html", {"book":book,"condition":condition,"is_available":is_available})

@login_required
@superuser_validator
def borrowed_books(request):
    book = BorrowedBook.objects.all().order_by("borrow_time")
    if request.method == "POST":
        ID  = request.POST["id"]
        approval = request.POST["Approval"]
        if approval == "yes":
            print(request.POST)
            borrowed_book = BorrowedBook.objects.get(id=int(ID))
            borrowed_book.is_approved =  True
            borrowed_book.save()
            messages.success(request,"Borrow request approved")
            return redirect("borrowed_books")
        else:
            borrowed_book = BorrowedBook.objects.get(id=int(ID))
            borrowed_book.is_approved =  False
            borrowed_book.save()
            messages.success(request,"Borrow request cancelled")
            return redirect("borrowed_books")
    return render(request, "front/borrowed-books.html", {"books":book})

def return_books(request):
    if request.method =="POST":
        id = int(request.POST["id"])
        
        book = BorrowedBook.objects.get(id = id)
        book.is_returned = True
        book.return_date = timezone.now()
        book.save()
        
        book_1 = Book.objects.get(id = book.book.id)
        book_1.available_quantity += 1
        book_1.save()
        print(book.is_returned)
        # print(book.is_returned)
        # print(book)
        messages.success(request,"Book successfully returned visit library for approval")
    return redirect("user_index")


def book_stat(request):
    data = ( BorrowedBook.objects
             .annotate(month = TruncMonth("borrow_time"))
             .values("month")
             .annotate(num=Count("name")))
    context = {"data":data}
    return render(request,"front/book_stat.html", context)