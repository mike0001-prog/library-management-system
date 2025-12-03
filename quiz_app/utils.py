from random import random
import csv
from .models import Question
from .models import Subject
from django.contrib import messages
from django.shortcuts import redirect
class Randomizer():
    def __init__(self):
        self.dic = {}

    def return_question_id(self, number_of_questions):
        for i in range(5):
            x = int(random() * 100)
            self.dic[f"{x}"] = x
        return self.dic.keys()


class Store():
    def __init__(self, request):
        self.session = request.session
        store =self.session.get("key")
        if "key" not in self.session:
            store = self.session["key"] = {}
        self.store = store

    def add(self, number_of_question, course_title):
        self.store["number_of_question"] = number_of_question
        self.store["course_title"] = course_title
        self.session.modified =True

    def return_quiz_info(self):
        return self.store
    
    def delete_quiz_info(self):
        del self.session["key"]


class QuizAnswer():
    def __init__(self, request):
        self.session = request.session
        store =self.session.get("answers")
        if "answers" not in self.session:
            store = self.session["answers"] = {}
        self.store = store

    def add(self, id, answer):
        question_id = str(id)
        question_answer = str(answer)
        if question_id in self.store:
            self.store[id] = question_answer
        else:
            self.store[id] = question_answer
        self.session.modified =True

    def return_answer(self):
        return self.store
    
    def delete(self):
        del self.session["answers"]
    
    def store_question_ids(self,question_id):
        self.session["question_id"] = question_id

    def return_queston_ids(self):
        return self.session["question_id"]
    
    def delete_queston_ids(self):
        del self.session["question_id"]



def extract_file(request,file):
    f = file.name
    if not f.endswith("csv"):
        messages.error(request,"file type not supported accepts only csv")
        return redirect("add_question")
    d = file.read().decode("utf-8").splitlines()
    reader = csv.DictReader(d)
    required_fields = ["subject","option_one","option_two","option_three","option_four","solution","answer"]
    if not all(field in reader.fieldnames for field in required_fields):
        messages.error(request,"fields in excel/csv file should be align with sample provided in help")
        return redirect("add_question")
    for line in reader:
        print(line)
        try:
            subject = Subject.objects.get(name=line["subject"])
        except Exception:
            Subject.objects.create(name=line["subject"])
            subject = Subject.objects.get(name=line["subject"])
            print("created")
        
        Question.objects.create(question=line["question"],
                                option_one=line["option_one"],
                                option_two=line["option_two"],
                                option_three=line["option_three"],
                                option_four=line["option_four"],
                                answer=line["answer"],
                                solution=line["solution"],
                                subject=subject)
        messages.success(request,"questions added successfully")