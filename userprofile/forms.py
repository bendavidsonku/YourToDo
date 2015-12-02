from django import forms

from userprofile.models import UserProfile

class UserAccountSettingsImageUploadForm(forms.ModelForm):

	class Meta: 
		model = UserProfile

		fields = ('profilePicture',)