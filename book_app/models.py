from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Categories"
    

class Book(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="upload/book_images/", blank=True, default="upload/book_images/default.jpeg")
    author = models.CharField(max_length=20)
    isbn = models.PositiveIntegerField(default=1000000000000)
    edition = models.IntegerField()
    quantity = models.IntegerField(default=1)
    available_quantity = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    about_book = models.TextField(default = "About book......")

    def __str__(self):
        return self.name
    
    def is_available(self):
        if self.available_quantity <= 2:
            return False
        return True
    
    
ret_time = timedelta(hours=168)
# t = timezone.now()+timedelta(hours=2)

class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowed_book")
    borrow_time = models.DateField(auto_now_add=True)
    # return date will be a week after book was borrowed
    due_date = models.DateField(blank=True)
    is_returned = models.BooleanField(default=False)
    is_overdue = models.BooleanField(default=False)
    return_date = models.DateField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    fine = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.book.name} borrowed by {self.borrower.username}"

    def save(self, *args, **kwargs):
        # due time set to 168hrs (a week) after borrow_time
        if not self.pk:
            self.due_date = timezone.now() + timedelta(hours=168)
            # print("testing....")
            # print(self.due_date)
        super().save(*args, **kwargs)

    def check_overdue(self):
        """Update overdue status"""
        if timezone.now() > self.due_date and not self.is_overdue:
            self.is_overdue = True
            self.save()
        return self.is_overdue
    

class ReadBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.title } Read by {self.user.username}"
    
    
class DeletedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{ self.book.title } deleted on {self.date}"
    

class ReturnedBook(models.Model):
    borrowed_book = models.ForeignKey(BorrowedBook, on_delete=models.CASCADE)
    return_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.borrowed_book.book.title} returned on {self.return_date} by {self.borrowed_book.borrower}"