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
    quiz = Question.objects.get(pk=quiz_id)
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
    quizzes = Question.objects.filter(exam=exam)
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
    exam = Exam.objects.get(pk=pk)
    question_types = QuizType.objects.all()
    if request.method == "POST":
        data = json.load(request)['data']
        if data.get('name'):
            quiz_type = QuizType.objects.create(name=data.get('name'))
            quiz_type.save()
            return JsonResponse({'status': 'ok', 'name': quiz_type.name})
        question = data['question']
        answers = data['answers']
        correct = data['correct']
        question_type = data['question_type']
        try:
            question_type = QuizType.objects.get(pk=question_type)
        except:
            # create a new one
            question_type = QuizType.objects.create(name=question_type)
            question_type.save()
        quiz = Question.objects.create(
            question=question, exam=exam, answer=correct[0], species=question_type)
        for answer in answers:
            QuizOption.objects.create(
                quiz=quiz, option=answer, is_true=True if answer == correct[0] else False).save()
        quiz.save()
        return JsonResponse({"ok": True, 'status': 'OK'})
    return render(request, 'settings/new_quiz.html', {'exam': exam, 'types': question_types})


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