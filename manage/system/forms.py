from cProfile import label
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from django import forms
from django.shortcuts import redirect
from .models import Entities, Files, Documents, Users, User_groups
import uuid
from django.contrib.auth import login
from django.contrib.auth.models import User



class EntitiesForm(forms.ModelForm):
    """Форма для внесения новых категорий в базу данных"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].empty_label = 'Родитель не выбран'
        

    class Meta:
        model = Entities
        fields=('id', 'parent','ent_name', 'description', 'cat_file')

        widgets = {
            'ent_name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }
        

class DocumentsAddForm(forms.ModelForm):
    """Форма для добавления новых документов в дазу данных"""
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['doc_name'].empty_label = ''
    Language_choise = (
        ("0", "Русский"),
        ("1", "Английский"),

    )
    document_language = forms.ChoiceField(choices=Language_choise)
    class Meta:
        model = Documents
        fields = ('id', 'doc_name', 'description', 'document_language')
        widgets = {
            'doc_name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),

        }

class FilesAddForm(forms.ModelForm):
    """Форма для добавления новых файлов в базу данных"""
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     #self.fields['id_document'].empty_label = 'Выберите к какому документу привязать файл'
    file = forms.FileField()
    class Meta:
        model = Files
        fields = ('id', 'id_document', 'file_name', 'file', 'file_version', 'add_data')

        widgets ={
            'file_name': forms.TextInput(attrs={'class': 'form-input'}),
            'file_version': forms.TextInput(attrs={'class': 'form-input'}),


        }


class RegisterUserForm(UserCreationForm):
    """Форма для регистрации новых пользователей"""
    username=forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    #email=forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Password again', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    choice = (
        ("Нет", "Нет"),

    )
    default_group = forms.ChoiceField(choices=choice)
    class Meta:

        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUserForm(AuthenticationForm):
    """Форма для авторизации пользователей"""
    username=forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))