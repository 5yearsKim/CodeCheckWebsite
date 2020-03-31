from django.shortcuts import get_object_or_404, render
from accounts.models import MyUser as User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import Question, Answer
from .forms import EditorForm
from .utils import check_answer, get_score


def basic(request):
    return render(request, 'challenges/startpage.html')

@login_required(login_url='/accounts/login/')
def mypage(request):
    m_user = get_object_or_404(User, student_id=request.user.student_id)
    m_answer = m_user.answer_set.all().order_by('question__type','-pub_date')
    q_done = [ans.question.id for ans in m_answer]
    unsubmitted = Question.objects.exclude(id__in=q_done).exclude(pub_date__gte=timezone.now())
    return render(request, "challenges/mypage.html", {"unsubmitted": unsubmitted, "m_user": m_user, "m_answer": m_answer})

@login_required(login_url='/accounts/login/')
def quiz_index(request):
    question_list = Question.objects.filter(type='q').exclude(pub_date__gte=timezone.now()).order_by('-pub_date')
    paginator = Paginator(question_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {'posts': posts}
    return render(request, 'challenges/index.html', context)

@login_required(login_url='/accounts/login/')
def challenge_index(request):
    question_list = Question.objects.filter(type='a').exclude(pub_date__gte=timezone.now()).order_by('-pub_date')
    paginator = Paginator(question_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {'posts': posts}
    return render(request, 'challenges/index.html', context)

@login_required(login_url='/accounts/login/')
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if question.pub_date >= timezone.now():
        raise Http404("Question not uploaded")
    answer, created = question.answer_set.get_or_create(
        user=request.user,
        defaults={'trial': 0,},
    )
    before_due = timezone.now() < question.due_date
    return render(request, 'challenges/detail.html', {'question': question, 'answer': answer, 'before_due':before_due})

@login_required(login_url='/accounts/login/')
def submitpage(request, question_id, is_reset=False):
    def update_score(request):
        m_user = get_object_or_404(User, student_id=request.user.student_id)
        answer = m_user.answer_set.all()
        m_score = 0
        for ans in answer:
            m_score += ans.score
        m_user.total_score = m_score
        m_user.save()
    question = get_object_or_404(Question, pk=question_id)
    answer = question.answer_set.get(user=request.user)
    if question.pub_date >= timezone.now():
        raise Http404("Question not uploaded")
    before_due = timezone.now() < question.due_date
    if request.method =="POST":
        form = EditorForm(request.POST, instance=answer)
        answer = form.save(commit=False)
        answer.trial = answer.trial + 1
        answer.pub_date = timezone.now()
        # answer.save(update_fields=['answer_code', 'trial', 'pub_date'])
        answer.save()
        mode = request.POST["dbgmode"]
        try:
            t_val, err_msg, m_stdout = check_answer(answer.answer_code, question.test_expression, mode)
        except:
            m_stdout, err_msg = "TimeoutError", "Potential Danger: It takes too much time to run your code!"
            context = {"question": question, "answer": answer, "err_msg": err_msg,
                       "m_stdout": m_stdout, "error": True}
            return render(request, "challenges/resultpage.html", context)
        context = {"question": question, "answer": answer, "t_val": t_val, "err_msg": err_msg, "m_stdout": m_stdout}
        if t_val == "code_error" or t_val == "test_error":
            context["error"] = True
            return render(request, "challenges/resultpage.html", context)
        else:
            context["error"] = False
            answer.test_value = t_val
            answer.score = get_score(question.test_value, answer.test_value, question.max_score)
            if not before_due:
                answer.score = 0.
                context["m_stdout"] = context["m_stdout"] + "\n TIMEOUT ERROR! You don't get any score!"
            answer.save()
            update_score(request)
            return render(request, 'challenges/resultpage.html', context)
    else:
        if answer.trial == 0 or is_reset:
            form = EditorForm(initial={"answer_code": question.sample_code})
            print("HIHI")
        else:
            form = EditorForm(initial={"answer_code": answer.answer_code})
            print("lose")
        return render(request, 'challenges/submitpage.html', {'question': question, 'answer': answer, "form": form, "before_due": before_due})


@login_required(login_url='/accounts/login/')
def reset_submitpage(request, question_id):
    return submitpage(request, question_id, is_reset=True)