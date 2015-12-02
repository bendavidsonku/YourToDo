from datetime import datetime
import string

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	firstName = models.CharField(max_length = 30)
	lastName = models.CharField(max_length = 60)
	phoneNumber = models.CharField(max_length = 15)
	dateOfBirth = models.DateField(auto_now = False, auto_now_add = False, null = True)
	profilePicture = models.ImageField(upload_to = 'profile-pictures', null = True)

	def __unicode__(self):
		return self.user.username

	def __str__(self):
		return self.user.username + "'s Profile"

	def set_firstName(self, firstName):
		self.firstName = firstName
		self.save()

	def get_firstName(self):
		return self.firstName

	def set_lastName(self, lastName):
		self.lastName = lastName
		self.save()

	def get_lastName(self):
		return self.lastName

	def set_phoneNumber(self, phoneNumber):
		self.phoneNumber = phoneNumber
		self.save()

	def get_phoneNumber(self):
		return self.phoneNumber

	def set_dateOfBirth(self, dateOfBirth):
		self.dateOfBirth = dateOfBirth
		self.save()

	def get_dateOfBirth(self):
		return self.dateOfBirth

	def get_dateOfBirth_forHTML(self):
		if self.dateOfBirth != None:
			timeInHTMLFormat = self.dateOfBirth.strftime("%Y-%m-%d")
			return(timeInHTMLFormat)
		else:
			return None

	def get_profilePicture(self):
		return self.profilePicture

User.profile = property(lambda u: UserProfile.objects.get_or_create(user = u)[0])
