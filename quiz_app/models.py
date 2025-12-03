from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Subject(models.Model):
    name = models.CharField(default="", max_length=100)

    def __str__(self):
        return  self.name


class Question(models.Model):
    question = models.TextField(max_length=600)
    option_one = models.CharField(max_length=100)
    option_two = models.CharField(max_length=100)
    option_three = models.CharField(max_length=100)
    option_four = models.CharField(max_length=100)
    answer = models.CharField(max_length=100,default="")
    solution = models.TextField(max_length=700,default="")
    subject = models.ForeignKey(Subject,on_delete=models.PROTECT)

    def __str__(self):
 
       return f"question {self.id}"

class UserScores(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.CharField(default="not available",max_length=20)
    user_score = models.CharField(max_length=4,default="0%")
    attempted  = models.IntegerField(default=0)
    number_of_questions = models.IntegerField(default=0)
    passed = models.IntegerField(default=0)
    failed = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    class Meta:
        verbose_name = 'User Score'
        verbose_name_plural = 'User Scores'

    def __str__(self):
        return f"{self.user}'s score {self.user_score}"

# class CsvUploads(models.Model):
#     file = models.FileField(upload_to="/csv")

#     def __str__(self):
#         return self.file.name