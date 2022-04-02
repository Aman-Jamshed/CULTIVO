from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class FarmerForm(ModelForm):
    class Meta:
        model = FarmerUser
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.NumberInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'profile_pic':forms.ClearableFileInput(attrs={'class':'form-control'})
        }
       

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title','image','content']
        

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'image':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control'})
        }
       

        

       

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']