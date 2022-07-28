from django.shortcuts import redirect, render
from her.models import QuizUser, Quiz, QuizOption, QuizType, EditorUser, Exam

# Create your views here.

def welcome(request):
    exams = Exam.objects.filter(private=False)
    [x.set_quiz_length() for x in exams]
    context = {
        'exams': exams,
    }
    return render(request, 'her/welcome.html', context)


def exam_quiz_view(request, slug, pk):
    if not request.user.is_authenticated:
        return redirect('/signup')
    exam = Exam.objects.get(slug=slug)
    quiz = Quiz.objects.get(pk=pk, exam=exam)
    options = QuizOption.objects.filter(quiz=quiz)
    
    context = {
        'quiz': quiz,
        'options': options,
        'exam': exam
    }

    print(context)
    return render(request, 'her/quiz.html', context)


def redirect_exam_quiz(request, slug):
    return redirect('1/')

def login_view(request):
    pass


def register_view(request):
    return render(request, 'her/register.html')