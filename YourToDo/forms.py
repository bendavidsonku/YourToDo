from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from registration.forms import RegistrationForm
	
class ContactForm(forms.Form):
    name = forms.CharField(max_length = 50, widget = forms.TextInput(attrs={'placeholder': 'Name'}), required = True)
    subject = forms.CharField(max_length = 100, widget=forms.TextInput(attrs={'placeholder': 'Subject'}), required = True)
    message = forms.CharField(widget = forms.Textarea(attrs={'placeholder': 'Message'}), required = True)
    sender = forms.EmailField(widget = forms.TextInput(attrs={'placeholder': 'Email'}), required = True)
