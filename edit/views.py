from django.shortcuts import redirect, render
from django.http import JsonResponse
from her.models import *
import json
from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    return render(request, 'settings/index.html')


@staff_member_required
def quiz_user_detail(request, pk):
    quiz_user = QuizUser.objects.get(pk=pk)
    return render(request, 'settings/quiz_user_detail.html', {'quiz_user': quiz_user})


@staff_member_required
def delete_quiz(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    options = QuizOption.objects.filter(quiz=quiz)
    for option in options:
        option.delete()
    quiz.delete()
    return JsonResponse({"ok": True, 'status': 'OK'})


@staff_member_required
def exams(request):
    
    exams = Exam.objects.all()
    return render(request, 'settings/exams.html', {'exams': exams})


@staff_member_required
def exam(request, pk):
    exam = Exam.objects.get(id=pk)
    # all quiz users who have taken this exam
    quiz_users = QuizUser.objects.all()
    quizzes = Quiz.objects.filter(exam=exam)
    t = []
    for quiz_user in quiz_users:
        if quiz_user.passed_exams.filter(id=pk).exists():
            t.append(quiz_user)
    return render(request, 'settings/exam.html', {'exam': exam, 't': t, 'quizzes': quizzes})


@staff_member_required
def quiz_users(request):
    quiz_users = QuizUser.objects.all()
    return render(request, 'settings/quiz_users.html', {'quiz_users': quiz_users})


@staff_member_required
def add_quiz(request, pk):
    if request.method == "POST":
        default_quiz_type = QuizType.objects.get(name="test")
        data = json.load(request)['data']
        question = data['question']
        answers = data['answers']
        correct = data['correct']
        exam = Exam.objects.get(pk=pk)
        quiz = Quiz.objects.create(
            question=question, exam=exam, answer=correct[0], species=default_quiz_type)
        for answer in answers:
            QuizOption.objects.create(
                quiz=quiz, option=answer, is_true=True if answer == correct[0] else False).save()
        quiz.save()
        print('Quiz',  quiz.id, 'created')
        print("successfully ", quiz.question, ' created')
        return JsonResponse({"ok": True, 'status': 'OK'})
    return render(request, 'settings/new_quiz.html', {'exam': Exam.objects.get(pk=pk)})


@staff_member_required
def add_exam(request):
    if request.method == "POST":
        data = request.POST
        name = data['exam_name']
        description = data['exam_desc']
        is_private = False
        private = True if is_private == 'on' else False
        count_down = data['exam_limit']
        def make_slug(x): return ''.join(
            e for e in x if e.isalnum() or e == ' ').lower().replace(' ', '-')
        slug = make_slug(name)
        exam = Exam.objects.create(
            name=name, description=description, private=private, count_down=count_down, slug=slug)
        exam.save()
        print("successfully", exam.name, ' created')
        return redirect('/settings/exams/')
    return render(request, 'settings/new_exam.html')


@staff_member_required
def delete_exam(request, pk):
    exam = Exam.objects.get(pk=pk)
    exam.delete()
    return JsonResponse({"ok": True, 'status': 'OK'})