from django.shortcuts import redirect, render

# Create your views here.

def welcome(request):
    return render(request, 'her/welcome.html')

def testview(request):
    return render(request, 'her/quiz.html')