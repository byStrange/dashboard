from django.urls import path
from . import views

app_name = "her"

urlpatterns = [
    path('', views.welcome, name="index"),
    path('quiz/<str:slug>/test/<int:pk>/', views.exam_quiz_view, name="quiz"),
    path('quiz/<str:slug>/test/', views.redirect_exam_quiz, name="exam"),
    path('quiz/<str:slug>/test/<int:pk>/check', views.exam_quiz_check, name="check"),
    path('quiz/<str:slug>/result/', views.exam_result, name="result"),


]
