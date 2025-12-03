from django.urls import path
from . import views
from . import views

urlpatterns = [
    # path("", views.quiz_home, name="quiz_home"),
    path("test/", views.home, name="test_home"),
    path("quiz_form/", views.form, name="quiz_form"),
    path("quiz_create/", views.QuestionListCreate.as_view(), name="quiz_create"),
    path("quiz_request/", views.QuestionView.as_view(), name="quiz_request"),
    path("submit/", views.submit, name="submit_quiz"),
    path("view_answer/", views.view_corrections, name="view_answer"),
    path("view_result/", views.view_result, name="view_result"),
    path("add_question/", views.add_question, name="add_question"),
    path("quiz_stat/", views.quiz_stat, name="quiz_stat"),
]
