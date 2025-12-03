# Create your views here.
from django.shortcuts import render,redirect
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Question,Subject,UserScores
from .serializer import QuestionSerializer
from .utils import Store,Randomizer,QuizAnswer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AddQuestionForm
from .utils import extract_file
from django.db.models.functions import TruncMonth
from django.db.models import Count,Avg
class QuestionView(APIView):
    def get(self,request):
        store = Store(request)
        StoreAnswers = QuizAnswer(request)

        number_of_question = int(store.return_quiz_info()["number_of_question"])
        course_title =  store.return_quiz_info()["course_title"] 
        # random_ids = Randomizer.return_question_id(number_of_questions=number_of_question)
        print(course_title)
        # questions = Question.objects.filter(id__in=random_ids)
        s = Subject.objects.get(name=course_title)
        
        questions = Question.objects.filter(subject=s).order_by("?")[:number_of_question]
        question_id = []
        for q in questions:
            question_id.append(q.id)
            pass
        StoreAnswers.store_question_ids(question_id=question_id)
        print(StoreAnswers.return_queston_ids())
        serializer  = QuestionSerializer(questions,many=True)
        return Response(serializer.data)
def home(request):
    store = Store(request)
    if store.return_quiz_info():
        course_title =  store.return_quiz_info()["course_title"] 
        # request.session["submitted"] = True
        if request.method == "POST":
            question_id = request.POST["id"]
            question_answers = request.POST["options"]
            print(request.POST)
            print(request.POST["id"])
            quizanswer = QuizAnswer(request)
            quizanswer.add(id=question_id,answer=question_answers)
            print(quizanswer.return_answer())
            return JsonResponse({"response":True})
        return render(request,"qiuz/quiz.html",{"course": course_title})
    else:
        return redirect("quiz_form")
@login_required
def form(request):
    store = Store(request)
    subjects = Subject.objects.all()
    quizanswer = QuizAnswer(request)
    answers = quizanswer.return_answer()
    try:
        if answers:
            quizanswer.delete()
            quizanswer.delete_queston_ids()
    except Exception as e:
        messages.error(request,"An error occured")
      
    if request.method == "POST":
        # print(request.POST)
        number_of_question = request.POST["number_of_question"]
        course_title =request.POST["course_title"]
        store.add(number_of_question=number_of_question,course_title=course_title)
        return redirect("test_home")
    return render(request,"qiuz/form.html",{"subjects":subjects})

def submit(request):
    store = Store(request)
    #check if the user as submitted before
    # then redirect the user back to the quiz selection page
    if request.method == "POST":
        condition = request.POST["condition"]
        if condition == "yes":
            if store.return_quiz_info():
                store = Store(request)
                quizanswer = QuizAnswer(request)
                answers = quizanswer.return_answer()
                print(answers.keys())
                keys = answers.keys()
                question = Question.objects.all()
                store = Store(request)
                number_of_question = int(store.return_quiz_info()["number_of_question"])
                total_passed = 0
                for key,item in answers.items():
                    id = int(key)
                    for q in question:
                        if id == q.id:
                            if item == q.answer:
                                total_passed+=1
                print(total_passed)
                #percent = float((total_passed/number_of_question) * 100)
                percent = round((total_passed*100)/number_of_question)
                total_attempted = len(keys)
                total_missed = total_attempted-total_passed

                # quizanswer.delete()
                UserScores.objects.create(user=request.user,
                                        user_score=percent,
                                        attempted=total_attempted,
                                        number_of_questions=number_of_question,
                                        passed=total_passed,
                                        failed=total_passed)
                # delete any information of the previous quiz that was submitted
                store.delete_quiz_info()
                context = {"percent":percent,
                            "passed":total_passed,
                            "failed":total_missed,
                            "attempted":total_attempted,
                            "total": number_of_question}
                return render(request,"qiuz/submit.html",context)
            else:
                messages.success(request,"you have submitted check your quiz history to review your score")
                return redirect("quiz_form")
        elif condition == "no":
            store.delete_quiz_info()
            return redirect("user_index")
class QuestionListCreate(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

def view_corrections(request):
    quizanswer = QuizAnswer(request)
    answers = quizanswer.return_answer()
    print(answers)
    question_ids = quizanswer.return_queston_ids()
    print(question_ids)
    questions = Question.objects.filter(id__in=question_ids)
    # for q in questions:
    #     for key,item in answers.items():
    #         id = int(key)
    #         if id == q.id:
    #             if item == q.answer:
    #                 print("yes")
    #             else:
    #                 print("no")
    return render(request,"qiuz/view_answer.html",{"questions":questions,"answers":answers})

def view_result(request):
    if request.user.is_superuser:
        user_scores = UserScores.objects.all()   
    else:
        user_scores = UserScores.objects.filter(user=request.user)
    # for s in user_scores:
    #     print(s.user_score)
    return render(request,"qiuz/view_result.html",{"results":user_scores})


@login_required
def add_question(request):
    form = AddQuestionForm()
    if request.method =="POST":
        if request.POST['type'] == "single":
            form = AddQuestionForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"question added successfully")
                return redirect("add_question")
            else:
                messages.warning(request,"invalid form inputs")
                return redirect("add_question")
        elif request.POST["type"] == "multiple":
            print(request.POST,request.FILES)
            file = request.FILES["file"]
            extract_file(request,file)
            return redirect("add_question")
    return render(request,"qiuz/add_questions.html",{"form":form})

@login_required
def quiz_stat(request):
    data_1 = (
        UserScores.objects
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )
    data = (UserScores.objects
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(avg=Avg("user_score"))
            .order_by("month"))

    months = [d["month"].strftime("%B %Y") for d in data]  # e.g. "August 2025"
    avgs = [d["avg"] for d in data]

    months_1 = [d["month"].strftime("%B %Y") for d in data_1]  
    counts = [d["count"] for d in data_1]
    context = {"counts":counts,"months":months,"months_1":months_1,"avgs":avgs}
    return render(request,"qiuz/quiz_stat.html",context)
# def add_multiple_questions(request):
#     if request.method =="POST":
#         print(request.POST,request.FILES)
#         file = request.FILES["file"]
#         d = file.read().decode("utf-8").splitlines()
#         reader = csv.DictReader(d)
#         subject_creation_condition = True
#         for line in reader:
#             print(line,subject_creation_condition)
#             if subject_creation_condition:
#                 Subject.objects.create(name=line["subject"])
#             subject = Subject.objects.get(name=line["subject"])
#             Question.objects.create(question=line["question"],
#                                     option_one=line["option_one"],
#                                     option_two=line["option_two"],
#                                     option_three=line["option_three"],
#                                     option_four=line["option_four"],
#                                     answer=line["answer"],
#                                     solution=line["solution"],
#                                     subject=subject)
#             subject_creation_condition = False
#     return  render(request,"qiuz/add_questions.html")


