from django import forms

class Login_form(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput,min_length=3)