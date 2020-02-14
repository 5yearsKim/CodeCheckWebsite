from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django.shortcuts import redirect, render

from .models import Question, Answer
from .utils import check_answer


class QuestionAdmin(admin.ModelAdmin, DynamicArrayMixin):
    fieldsets = (
        (None, {
            'fields': ('title', 'question_text', 'description',)
        }),
        ("Code", {
            'fields': ('sample_code', 'answer_code', 'test_expression')
        }),
        ("Detail", {
            'fields': ('max_score', 'due_date')
        }),
    )
    list_display = ['title', 'pub_date', 'due_date', 'test_value']
    # list_display_links = ['id', 'title']
    # list_editable = ['author']
    # list_per_page = 3
    list_filter = ['title', 'pub_date', 'due_date']

    def response_add(self, request, obj):
        answer, err_msg, m_stdout = check_answer(obj.answer_code, obj.test_expression)
        context = {"answer": answer, "err_msg": err_msg, "question": obj}
        if answer == "code_error" or answer == "test_error":
            context["error"] = True
            return render(request, "admin/upload_result.html", context)
        context["error"] = False
        obj.test_value = answer
        obj.save()
        return render(request, "admin/upload_result.html", context)

    def response_change(self, request, obj):
        answer, err_msg, m_stdout = check_answer(obj.answer_code, obj.test_expression)
        context = {"answer": answer, "err_msg": err_msg, "question": obj}
        if answer == "code_error" or answer == "test_error":
            context["error"] = True
            return render(request, "admin/upload_result.html", context)
        context["error"] = False
        obj.test_value = answer
        obj.save()
        return render(request, "admin/upload_result.html", context)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ["user", "question", "score"]
    list_filter = ["user", "question"]
    ordering = ["question", "user"]





admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)

