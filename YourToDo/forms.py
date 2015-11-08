from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UniqueUserEmailField(forms.EmailField):
    """
    An EmailField which only is valid if no User has that email.
    """
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
	username = forms.CharField(label = 'Username', max_length=30, help_text=('Length: 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'), widget=forms.TextInput(attrs={'placeholder': 'Username'}))
	email = UniqueUserEmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))
	first_name = forms.CharField(label = "First Name", required = True,  widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
	last_name = forms.CharField(label = "Last Name", required = True,  widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
	password1 = forms.CharField(label = "Password", required = True,  widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
	password2 = forms.CharField(label = "Password confirmation", required = True,  widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

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