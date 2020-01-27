from django.shortcuts import render, redirect
from .models import MyUser as User
from .forms import UserRegistrationForm
from django.contrib import auth

def basic(request):
    return render(request, 'accounts/base.html')

def signup(request):
    if request.method =="POST":
        form = UserRegistrationForm(request.POST)
        if not form.is_valid():
            return render(request, 'accounts/signup.html', {'form': UserRegistrationForm(),
                                                            'error': 'Please fill in the form correctly'})
        userObj = form.cleaned_data
        username = userObj['username']
        email =  userObj['email']
        password1 =  userObj['password1']
        password2 =  userObj['password2']
        date_of_birth =  userObj['date_of_birth']

        if password1 != password2:
            return render(request, 'accounts/signup.html', {'form': UserRegistrationForm(),
                                                            'error': 'password confirmation doesn\'t match'})
        if (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
            return render(request, 'accounts/signup.html', {'form': UserRegistrationForm(),
                                                            'error': 'User name or Email already exists'})
        User.objects.create_user(
            username=username, password=password1,
            email=email, date_of_birth=date_of_birth
        )
        user = auth.authenticate(username=username, password=password1)
        auth.login(request, user)
        return redirect("/")

    else:
        return render(request, 'accounts/signup.html', {"form": UserRegistrationForm()})

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            return render(request, 'accounts/login.html', {'error':'username or password is incorrect'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect("/")