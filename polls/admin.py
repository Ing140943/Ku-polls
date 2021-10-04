"""This module is about admin section and creating question section."""
from django.contrib import admin
from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """This class determine the number of choice that must include in line."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """This class let admin can handle all question in the web application."""

    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'],
                              'classes': ['collapse']}),
        ('End Date information', {'fields': ['end_date'],
                                  'classes': ['collapse']})
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date',
                    'end_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
