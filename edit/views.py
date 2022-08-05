from django.shortcuts import redirect, render
from django.http import JsonResponse
from her.models import *
import json
# Create your views here.


def is_staff(request):
    if request.user.is_authenticated and request.user.is_staff:
        return True
    else:
        return False

def quiz_user_detail(request, pk):
    if is_staff(request):
        quiz_user = QuizUser.objects.get(pk=pk)
        return render(request, 'settings/quiz_user_detail.html', {'quiz_user': quiz_user})
    else:
        return FALSE(request)


def exams(request):
    if is_staff(request):
        exams = Exam.objects.all()
        return render(request, 'settings/exams.html', {'exams': exams})
    else:
        return FALSE(request)

def exam(request, pk):
    if is_staff(request):
        exam = Exam.objects.get(pk=pk)
        # all quiz users who have taken this exam
        quiz_users = QuizUser.objects.all()
        quizzes = Quiz.objects.filter(exam=exam)
        t = []
        for quiz_user in quiz_users:
            if quiz_user.passed_exams.filter(pk=pk).exists():
                t.append(quiz_user)
        return render(request, 'settings/exam.html', {'exam': exam, 't': t, 'quizzes': quizzes})
    else:
        return FALSE(request)

def quiz_users(request):
    if is_staff(request):
        quiz_users = QuizUser.objects.all()
        return render(request, 'settings/quiz_users.html', {'quiz_users': quiz_users})
    else:
        return FALSE(request)

def add_quiz(request, pk):
    if request.method == "POST":
        data = json.load(request)['hello']
        print(data)
        return JsonResponse({"ok": True, 'status': 'OK'})
    return render(request, 'settings/new_quiz.html', {'exam': Exam.objects.get(pk=pk)})


def add_exam(request):
    if is_staff(request):
        if request.method == "POST":
            data = request.POST
            name = data['exam_name']
            description = data['exam_desc']
            private = data['private']
            private = True if private == 'true' else False
            count_down = data['exam_limit']
            exam = Exam.objects.create(name=name, description=description, private=private, count_down=count_down)
            exam.save()
            print("successfully", exam.name, ' created')
            return redirect('/settings/exams/')
        return render(request, 'settings/new_exam.html')
    else:
        return FALSE(request)


def FALSE(request):
    return JsonResponse({"ok": False, 'status': 'NOT AUTHORIZED'})