from django.contrib import admin
from .models import Module, Lesson, Assignment, AssignmentSubmission, Quiz, QuizQuestion, QuizChoice, QuizSubmission, QuizAnswer, DiscussionForum, DiscussionPost, DiscussionReply

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'is_active')
    search_fields = ('title', 'course__name')
    list_filter = ('course', 'is_active')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'is_active')
    search_fields = ('title', 'module__title')
    list_filter = ('module', 'is_active')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'max_points', 'is_active')
    search_fields = ('title', 'course__name')
    list_filter = ('course', 'is_active')

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submission_date', 'points_awarded', 'is_graded')
    search_fields = ('assignment__title', 'student__name')
    list_filter = ('is_graded', 'submission_date')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'max_points', 'is_active')
    search_fields = ('title', 'course__name')
    list_filter = ('course', 'is_active')

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz', 'question_type', 'points', 'order')
    search_fields = ('question_text', 'quiz__title')
    list_filter = ('quiz', 'question_type')

@admin.register(QuizChoice)
class QuizChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice_text', 'is_correct')
    search_fields = ('choice_text', 'question__question_text')

@admin.register(QuizSubmission)
class QuizSubmissionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'student', 'submission_date', 'score', 'is_graded')
    search_fields = ('quiz__title', 'student__name')
    list_filter = ('is_graded', 'submission_date')

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ('submission', 'question', 'answer_text')
    search_fields = ('answer_text', 'question__question_text')

@admin.register(DiscussionForum)
class DiscussionForumAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_by', 'created_at', 'is_active')
    search_fields = ('title', 'course__name')
    list_filter = ('course', 'is_active')

@admin.register(DiscussionPost)
class DiscussionPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'forum', 'author', 'created_at', 'is_pinned')
    search_fields = ('title', 'forum__title')
    list_filter = ('forum', 'is_pinned')

@admin.register(DiscussionReply)
class DiscussionReplyAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('post__title', 'author__username')