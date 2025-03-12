from django import forms
from django.contrib.auth.models import User
from .models import Job, Response

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('employer', 'Employer'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Who are you?')
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'salary']


class SearchForm(forms.Form):
    query = forms.CharField()

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['resume']

class ResponseStatusForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['status']
