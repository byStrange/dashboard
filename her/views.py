from django.shortcuts import redirect, render
from her.models import QuizUser, Quiz, QuizOption, QuizType, EditorUser, Exam, Result
from django.contrib.auth import login
from django.contrib.auth.models import User
from datetime import datetime

SPLITTER = "_"
# Create your views here.


def welcome(request):
    exams = Exam.objects.filter(private=False)
    [x.set_quiz_length() for x in exams]
    context = {
        'exams': exams,
    }
    return render(request, 'her/welcome.html', context)


def exam_quiz_view(request, slug, pk):
    if request.method == 'POST':
        data = request.POST
        name = data['username']
        quiz_user = QuizUser.objects.create(
            name=name, created_at=datetime.now(), updated_at=datetime.now())
        quiz_user.save()
        result = Result.objects.create(user=quiz_user, exam=Exam.objects.get(
            slug=slug), started_at=datetime.now())
        result.save()
        request.session['quiz_user'] = quiz_user.id
        try:
            user = User.objects.create_user(name, '', '')
        except:
            user = User.objects.create_user(
                name + SPLITTER + str(quiz_user.id), '', '')
        user.save()
        login(request, user)
        return redirect('/my/quiz/' + slug + '/' + 'test/1/')
    exam = Exam.objects.get(slug=slug)
    quiz = Quiz.objects.get(pk=pk, exam=exam)
    options = QuizOption.objects.filter(quiz=quiz)

    context = {
        'quiz': quiz,
        'options': options,
        'exam': exam
    }
    if not request.user.is_authenticated:
        return redirect('/my/quiz/' + slug + '/' + 'test/')
    return render(request, 'her/quiz.html', context)


def redirect_exam_quiz(request, slug):
    if request.user.is_authenticated:
        return redirect('1/')
    else:
        return render(request, 'her/start.html')


def login_view(request):
    pass


def register_view(request):
    return render(request, 'her/register.html')
