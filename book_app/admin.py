from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(BorrowedBook)
admin.site.register(ReadBook)
admin.site.register(ReturnedBook)
admin.site.register(DeletedBook)