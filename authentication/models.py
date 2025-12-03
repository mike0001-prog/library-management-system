from django.db import models
from django.contrib.auth.models import User
import PIL

# Create your models here.
class Department(models.Model):
    department = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.department
    


class Level(models.Model):
    level = models.CharField(max_length=50)

    def __str__(self):
        return self.level
    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    passport = models.ImageField(upload_to="media/user_profile", default="user_profile/default.png")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, default=1)
    gender = models.CharField(default="------", choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('------', '------')
    ], max_length=25)
    d_o_b = models.DateField()

    def __str__(self):
        return f"{self.user.username}'s profile"
    