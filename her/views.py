from django.http import JsonResponse
from django.shortcuts import redirect, render
from her.models import QuizUser, Quiz, QuizOption, QuizType, EditorUser, Exam, Result
from django.contrib.auth import login
from django.contrib.auth.models import User
from datetime import datetime
from json import load, loads


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
            slug=slug))
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
    is_last = False
    exam = Exam.objects.get(slug=slug)
    quiz = Quiz.objects.get(pk=pk, exam=exam)
    options = QuizOption.objects.filter(quiz=quiz)
    last_quiz = Quiz.objects.filter(
        exam=Exam.objects.get(slug=slug)).order_by('-id')[0]

    if quiz.id == last_quiz.id:
        is_last = True

    context = {
        'quiz': quiz,
        'options': options,
        'exam': exam, 'is_last': is_last
    }
    if not request.user.is_authenticated:
        return redirect('/my/quiz/' + slug + '/' + 'test/')
    return render(request, 'her/quiz.html', context)


def exam_quiz_check(request, slug, pk):
    if request.method == 'GET':
        data = request.GET
        data = loads(data.get("data"))
        user_answer = data['answer']
        quiz_user = QuizUser.objects.get(pk=request.session['quiz_user'])
        quiz = Quiz.objects.get(pk=pk, exam=Exam.objects.get(slug=slug))
        result = Result.objects.get(
            user=quiz_user, exam=Exam.objects.get(slug=slug))
        result.quiz = quiz
        result.save()
        quiz.user_answer = user_answer
        result.score += 1 if quiz.answer == user_answer else 0
        result.save()
        try:
            next_quiz = Quiz.objects.get(
                id=pk + 1, exam=Exam.objects.get(slug=slug))
        except:
            next_quiz = None
        if next_quiz:
            return JsonResponse({"next_quiz_url": '/my/quiz/' + slug + '/' + 'test/' + str(next_quiz.id) + '/', "next_quiz_id": next_quiz.id, 'quiz_user': quiz_user.name})
        else:
            return JsonResponse({"exam_result_url": '/my/quiz/' + slug + '/' + 'result/', "quiz_user": request.user.username})
    return redirect('/my/quiz/' + slug + '/' + 'test/1/')


def redirect_exam_quiz(request, slug):
    if request.user.is_authenticated:
        return redirect('1/')
    else:
        return render(request, 'her/start.html')


def exam_result(request, slug):
    exam = Exam.objects.get(slug=slug)
    result = Result.objects.get(user=QuizUser.objects.get(
        id=request.session['quiz_user']), exam=exam)
    quizzes = Quiz.objects.filter(exam=exam)
    context = {
        'exam': exam,
        'result': result,
        'quizzes': quizzes
    }
    return render(request, 'her/result.html', context)


def login_view(request):
    pass


def register_view(request):
    return render(request, 'her/register.html')
