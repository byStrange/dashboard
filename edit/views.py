from django.shortcuts import render
from django.http import JsonResponse
from her.models import *
# Create your views here.


def is_staff(request):
    if request.user.is_authenticated and request.user.is_staff:
        return True
    else:
        return False


def exams_view(request):
    if is_staff(request):
        exam = Exam.objects


def new(request):
    if is_staff(request):
        return render(request, 'settings/new.html')
    else:
        return JsonResponse({"ok": False, 'status': 'NOT AUTHORIZED'})