from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UniqueEmailField(forms.EmailField):
   
    def validate(self, value):
        super(forms.EmailField, self).validate(value)
        try:
            User.objects.get(email = value)
            raise forms.ValidationError("The specified email already belongs to a registered user")
        except User.MultipleObjectsReturned:
            raise forms.ValidationError("The specified email already belongs to a registered user")
        except User.DoesNotExist:
            pass

class defaultUserRegistrationForm(UserCreationForm):
	username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Username'}), required = True)
	email = UniqueEmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))
	first_name = forms.CharField(required = True,  widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
	last_name = forms.CharField(required = True,  widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
	password1 = forms.CharField(required = True,  widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
	password2 = forms.CharField(required = True,  widget=forms.PasswordInput(attrs={'placeholder': 'Re-type Password'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

		def save(self, commit = True):
			user = super(defaultUserRegistrationForm, self).save(commit = False)
			user.email = self.cleaned_data['email']
			user.firstName = self.cleaned_data['first_name']
			user.lastName = self.cleaned_data['last_name']

			if commit:
				user.save()

			return user

class ContactForm(forms.Form):
    name = forms.CharField(max_length = 50, widget = forms.TextInput(attrs={'placeholder': 'Name'}), required = True)
    subject = forms.CharField(max_length = 100, widget=forms.TextInput(attrs={'placeholder': 'Subject'}), required = True)
    message = forms.CharField(widget = forms.Textarea(attrs={'placeholder': 'Message'}), required = True)
    sender = forms.EmailField(widget = forms.TextInput(attrs={'placeholder': 'Email'}), required = True)