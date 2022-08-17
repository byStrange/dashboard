from django.urls import path
from . import views 

app_name = "edit"

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.quiz_users, name="quiz_users"),
    path('users/<int:pk>/', views.quiz_user_detail, name="quiz_user_detail"),

    path("exams/", views.exams, name="exams"),
    path("exams/<int:pk>/", views.exam, name="exam"),
    # path("exams/<str:slug>/<int:pk>/", views.quiz_edit, name="exam"),
    path('exams/<int:pk>/add/', views.add_quiz, name="add_quiz"),
    path('exams/<int:pk>/delete/', views.delete_exam, name="delete_exam"),
    path('delete/quiz/<int:quiz_id>/', views.delete_quiz, name="delete_quiz"),
    path('exams/add/', views.add_exam, name="add_exam"),
]
