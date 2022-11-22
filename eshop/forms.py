from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets

#Sign up form (with this form we create customers)
class UserCustomerForm(UserCreationForm):
    name=forms.CharField()
    email=forms.EmailField()
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'password1', 'password2')
