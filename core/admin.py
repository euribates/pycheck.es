from django.contrib import admin


from core.models import Context
from core.models import Exercise
from core.models import Student
from core.models import Submission
from core.models import Topic


class StudentAdmin(admin.ModelAdmin):
    ordering = ['pk']
    list_display = ('pk', 'username', 'context', 'last_active')
    list_filter = ('context',)


class ContextAdmin(admin.ModelAdmin):
    ordering = ['pk']
    list_display = ('pk', 'code', 'name')


class ExerciseAdmin(admin.ModelAdmin):
    ordering = ['pk']
    list_display = ('name', 'title', 'hash', 'topic')
    search_fields = [
        'name',
        'title',
        'hash',
        ]
    list_filter = ('topic',)


class TopicAdmin(admin.ModelAdmin):
    ordering = ['pk']
    list_display = ('pk', 'name')


class SubmissionAdmin(admin.ModelAdmin):
    ordering = ['pk']
    list_display = ('pk', 'student', 'exercise', 'passed', 'submitted_at')


admin.site.register(Student, StudentAdmin)
admin.site.register(Context, ContextAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Submission, SubmissionAdmin)
