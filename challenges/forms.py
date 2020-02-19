from django import forms
from django_ace import AceWidget
from .models import Answer

class EditorForm(forms.ModelForm):
    class Meta:
        model = Answer
        widgets = {
            "answer_code": AceWidget(mode='python', theme='twilight')
        }
        fields = ['answer_code']


class EditorForm2(forms.Form):
    text = forms.CharField(widget=AceWidget(mode='python', theme='twilight'))

class QuestionTypeForm(forms.ModelForm):
    MY_CHOICES = (
        ('q', 'quiz'),
        ('c', 'challenge'),
    )

    type = forms.ChoiceField(choices=MY_CHOICES)
