from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Exam(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    count_down = models.PositiveBigIntegerField(default=0) # in minutes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class EditorUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    quiz_created = models.IntegerField(default=0)
    quizzes = models.ManyToManyField('Quiz', blank=True)
    
    def __str__(self):
        return self.user.username if self.user.username else self.user.first_name

class QuizUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(help_text='Enter your email', unique=True)
    password = models.CharField(max_length=100)
    quiz_passed = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Quiz(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True, default=None)
    species = models.ForeignKey('QuizType', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "Quizes"

class QuizOption(models.Model):
    option = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
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