# myapp/forms.py
from django import forms


class UserInputForm(forms.Form):
    text_input = forms.CharField(max_length=255)


class InputForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    roll_number = forms.IntegerField(
        help_text="Enter 6 digit roll number"
    )
    password = forms.CharField(widget=forms.PasswordInput())


class AnswerForm(forms.Form):
    answer = forms.IntegerField(
        help_text="Enter answer"
    )
