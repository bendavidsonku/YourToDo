from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class defaultUserRegistrationForm(UserCreationForm):
	email = forms.EmailField(required = True)
	firstName = forms.CharField(label = "First Name", required = True)
	lastName = forms.CharField(label = "Last Name", required = True)

	class Meta:
		model = User
		fields = ('username', 'firstName', 'lastName', 'email', 'password1', 'password2')

		def save(self, commit = True):
			user = super(defaultUserRegistrationForm, self).save(commit = False)
			user.email = self.cleaned_data['email']
			user.firstName = self.cleaned_data['firstName']
			user.lastName = self.cleaned_data['lastName']

			if commit:
				user.save()

			return user