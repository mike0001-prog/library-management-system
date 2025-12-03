from django.contrib import admin
from .models import UserProfile, Department, Level

# Register your models here.
admin.site.register(Department)
admin.site.register(UserProfile)
admin.site.register(Level)