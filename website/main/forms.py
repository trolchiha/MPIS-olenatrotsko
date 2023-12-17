from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Project, Task, Volunteer, Application

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Псевдонім',
            'first_name': 'Ім\'я',
            'last_name': 'Прізвище',
            'email': 'Електронна пошта',
        }

class RegisterVolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['birth_date', 'location', 'phone_number']
        labels = {
            'birth_date': 'Дата народження',
            'location': 'Місце проживання',
            'phone_number': 'Номер телефону'
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'location', 'work_type']
        labels = {
            'name': 'Назва',
            'description': 'Опис',
            'start_date': 'Дата початку',
            'end_date': 'Дата закінчення',
            'location': 'Місце проведення',
            'work_type': 'Тип робіт'
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['application_text']
        labels = {
            'application_text': 'Примітки'
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'start_date', 'end_date']
        labels = {
            'name': 'Назва',
            'description': 'Опис',
            'start_date': 'Дата початку',
            'end_date': 'Дата закінчення'
        }