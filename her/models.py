from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Exam(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    count_down = models.PositiveBigIntegerField(default=0)  # in minutes
    quizzes_length = models.PositiveBigIntegerField(default=0)
    private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_quiz_length(self):
        self.quizzes_length = len(Question.objects.filter(exam=self))
        self.save()
        return self.quizzes_length

    def __str__(self):
        return self.name


class EditorUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    quiz_created = models.IntegerField(default=0)
    quizzes = models.ManyToManyField('Question', blank=True)

    def __str__(self):
        return self.user.username if self.user.username else self.user.first_name


class QuizUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(help_text='Enter your email')
    password = models.CharField(max_length=100, blank=True)
    quiz_passed = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    passed_exams = models.ManyToManyField('Exam', blank=True)
    point_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Result(models.Model):
    user = models.ForeignKey(QuizUser, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    finished_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.name} - {self.exam.name}'


class UserAnswer(models.Model):
    user = models.ForeignKey(QuizUser, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.answer


class Question(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    user_answer = models.ManyToManyField(
        UserAnswer, blank=True) 
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, null=True, default=None)
    species = models.ForeignKey('QuizType', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question



class QuizOption(models.Model):
    option = models.CharField(max_length=255)
    quiz = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_true = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.option


class QuizType(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
