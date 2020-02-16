from django import forms

class UserRegistrationForm(forms.Form):
    student_id = forms.CharField(
        required = True,
        label = 'student_id',
        max_length = 10
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

    nickname = forms.CharField(
        required = True,
        label = 'nickname',
    )



