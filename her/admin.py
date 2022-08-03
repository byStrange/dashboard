from django.contrib import admin
from her.models import QuizUser, Quiz, QuizOption, QuizType, EditorUser, Exam, Result, UserAnswer
# Register your models here.

admin.site.register(QuizUser)
admin.site.register(Quiz)
admin.site.register(QuizOption)
admin.site.register(QuizType)
admin.site.register(EditorUser)
admin.site.register(Result)
admin.site.register(UserAnswer)

# admin site register exam with prepopulated fields name and slug
class ExamAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Exam, ExamAdmin)