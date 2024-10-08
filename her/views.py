from django.http import JsonResponse
from django.shortcuts import redirect, render
from her.models import QuizUser, Quiz, QuizOption, Exam, Result, UserAnswer
from django.contrib.auth import login
from django.contrib.auth.models import User
from datetime import datetime
from json import loads
import requests
from .config import CHAT_ID, BOT_TOKEN
CHAT_ID = str(CHAT_ID)
BOT_TOKEN = str(BOT_TOKEN)

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
        return redirect('/my/quiz/' + slug + '/' + 'test/')
    is_last = False
    exam = Exam.objects.get(slug=slug)
    quiz = Quiz.objects.get(pk=pk, exam=exam)
    options = QuizOption.objects.filter(quiz=quiz)
    print(options)
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
    quiz_user = QuizUser.objects.get(pk=request.session['quiz_user'])
    exam = Exam.objects.get(slug=slug)
    quiz = Quiz.objects.get(pk=pk, exam=exam)
    result = Result.objects.get(
        user=quiz_user, exam=Exam.objects.get(slug=slug))
    if request.method == 'GET' and loads(request.GET.get("data")).get("answer"):
        data = request.GET
        data = loads(data.get("data"))
        user_answer = data['answer']
        result.quiz = quiz
        result.save()
        useranswer = UserAnswer.objects.create(
            user=quiz_user, answer=user_answer)
        useranswer.save()
        print('user', useranswer)
        quiz.user_answer.add(useranswer)
        result.score += 1 if quiz.answer == user_answer else 0
        result.save()
        exam_quizzes = Quiz.objects.filter(exam=exam)
        # if quiz.id == exam_quizzes.order_by('-id')[0].id:
        #     result.passed_exams.add(exam)
        #     result.save()
        #     return JsonResponse({'status': 'passed'})
        current = exam_quizzes.get(id=pk)
        all_ids = []
        for x in exam_quizzes:
            all_ids.append(x.id)

        try:
            next_id = all_ids[all_ids.index(current.id) + 1]
            next_quiz = Quiz.objects.get(id=next_id)
        except:
            next_quiz = None
        if next_quiz:
            return JsonResponse({"next_quiz_url": '/my/quiz/' + slug + '/' + 'test/' + str(next_quiz.id) + '/', "next_quiz_id": next_quiz.id, 'quiz_user': quiz_user.name})
        else:
            quiz_user.quiz_passed += 1
            quiz_user.passed_exams.add(exam)
            quiz_user.save()
            # send message to telegram with api.telegram.org
            # message text should be like this: User {name} passed exam {exam} with score {score} out of {quizzes_length}
            message = 'User "' + quiz_user.name + '" passed exam "' + exam.name + '" with score ' + str(result.score) + ' out of ' + str(exam.quizzes_length) + '" at "' + datetime.now().strftime("%d/%m/%Y %H:%M") + '"'
            url = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + CHAT_ID + '&text=' + message
            try:
                requests.get(url)
            except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError):
                print("CONNECTION ERROR ON SENDING MESSAGE TO THE GROUP")
            return JsonResponse({"exam_result_url": '/my/quiz/' + slug + '/' + 'result/', "quiz_user": request.user.username})

    result.score = 0
    result.save()
    print(result.score)
    return redirect('/my/quiz/' + slug + '/' + 'test/1/')


def redirect_exam_quiz(request, slug):
    if request.user.is_authenticated:
        url = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + CHAT_ID + '&text=User "' + request.user.username + '" started exam "' + Exam.objects.get(slug=slug).name + '" at "' + datetime.now().strftime("%d/%m/%Y %H:%M") + '"'
        try:
            requests.get(url)
        except:
            print("CONNECTION ERROR ON SENDING MESSAGE TO THE GROUP")
        quiz_user = QuizUser.objects.get(pk=request.session['quiz_user'])
        result = Result.objects.get(
            user=quiz_user, exam=Exam.objects.get(slug=slug))
        result.score = 0
        quizzes = Quiz.objects.filter(exam=Exam.objects.get(slug=slug))
        for quiz in quizzes.all():
            for answer in quiz.user_answer.all():
                if answer.user.id == quiz_user.id:
                    answer.delete()
        result.save()
        first_quiz_id = Quiz.objects.filter(
            exam=Exam.objects.get(slug=slug)).first().id
        return redirect(str(first_quiz_id) + '/')
    else:
        return render(request, 'her/start.html')


def exam_result(request, slug):
    print(QuizUser.objects.get(
        id=request.session['quiz_user']).passed_exams.all())
    exam = Exam.objects.get(slug=slug)
    result = Result.objects.get(user=QuizUser.objects.get(
        id=request.session['quiz_user']), exam=exam)
    quizzes = Quiz.objects.filter(exam=exam)
    f = exam.quizzes_length - result.score
    if f < 0:
        f = 0
    context = {
        'exam': exam,
        'result': result,
        'quizzes': quizzes,
        'f': f
    }
    return render(request, 'her/result.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/my/")
    return render(request, 'her/login.html')


def register_view(request):
    return render(request, 'her/register.html')
