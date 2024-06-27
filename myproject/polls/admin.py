#https://docs.djangoproject.com/en/4.2/intro/tutorial07/

from django.contrib import admin

from .models import *

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Vote)