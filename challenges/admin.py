from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django.shortcuts import render, redirect
from import_export.admin import ImportExportModelAdmin
from markdownx.widgets import AdminMarkdownxWidget

from .models import Question, Answer, DescriptionField
from .utils import check_answer
from .forms import QuestionTypeForm
from accounts.models import MyUser as User


class QuestionAdmin(admin.ModelAdmin, DynamicArrayMixin):
    fieldsets = (
        (None, {
            'fields': ('title', 'question_text', 'description',)
        }),
        ("Code", {
            'fields': ('sample_code', 'answer_code', 'test_expression')
        }),
        ("Detail", {
            'fields': ('type', 'max_score', 'pub_date', 'due_date')
        }),
    )
    list_display = ['title', 'type', 'pub_date', 'due_date', 'test_value']
    # list_display_links = ['id', 'title']
    # list_editable = ['author']
    # list_per_page = 3
    list_filter = ['title']
    formfield_overrides = {
        DescriptionField: {'widget': AdminMarkdownxWidget},
    }
    form = QuestionTypeForm

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

    def response_delete(self, request, obj_display, obj):
        def update_score(m_user):
            answer = m_user.answer_set.all()
            m_score = 0
            for ans in answer:
                m_score += ans.score
            m_user.total_score = m_score
            m_user.save()
        users = User.objects.all()
        for user in users:
            update_score(user)
        return redirect('/admin')

class AnswerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["user", "question", "score"]
    list_filter = ["question"]
    ordering = ["question", "user"]





admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)

