from django.urls import path
from . import views

app_name = "her"

urlpatterns = [
    path('', views.welcome, name="index"),
    path('test/<int:pk>/', views.quiz_view, name="test"),
    path('quiz/<str:slug>/test/<int:pk>/', views.exam_quiz_view, name="quiz"),
    path('quiz/<str:slug>/test/', views.redirect_exam_quiz, name="quiz"),
]
