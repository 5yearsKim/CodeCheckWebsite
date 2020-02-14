from django.shortcuts import render, redirect
from .models import MyUser as User
from .forms import UserRegistrationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


def basic(request):
    return render(request, 'accounts/base.html')

def signup(request):
    if request.method =="POST":
        form = UserRegistrationForm(request.POST)
        if not form.is_valid():
            return render(request, 'accounts/signup.html', {'form': UserRegistrationForm(),
                                                            'error': 'Please fill in the form correctly'})
        userObj = form.cleaned_data
        student_id = userObj['student_id']
        password1 =  userObj['password1']
        password2 =  userObj['password2']
        nickname =  userObj['nickname']

        if password1 != password2:
            return render(request, 'accounts/signup.html', {'form': UserRegistrationForm(),
                                                            'error': 'password confirmation doesn\'t match'})
        if User.objects.filter(student_id=student_id).exists():
            return render(request, 'accounts/signup.html', {'form': UserRegistrationForm(),
                                                            'error': 'User name or Email already exists'})
        User.objects.create_user(
            student_id=student_id, password=password1, nickname=nickname,
        )
        user = auth.authenticate(student_id=student_id, password=password1)
        auth.login(request, user)
        return redirect("/")

    else:
        return render(request, 'accounts/signup.html', {"form": UserRegistrationForm()})

def login(request):
    if request.method == "POST":
        student_id = request.POST['student_id']
        password = request.POST['password']
        user = auth.authenticate(request, student_id=student_id, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            return render(request, 'accounts/login.html', {'error':'student_id or password is incorrect'})
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect("/")

@login_required(login_url='/accounts/login/')
def change_password(request):
    error = ""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/')
        else:
            error = "please fill in the form correctly"

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form, 'error': error
    })

