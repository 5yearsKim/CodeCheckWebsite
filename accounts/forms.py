from django import forms

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 12
    )
    password1 = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput()
    )
    password2 = forms.CharField(
        required = True,
        label = 'Password Confirmation',
        max_length = 32,
        widget = forms.PasswordInput()
    )

    email = forms.EmailField(
        required = True,
        label = 'Email',
    )
    date_of_birth = forms.DateField(
        required = True,
        label = 'Date of Birth',
        widget = forms.SelectDateWidget(),
    )
