from django.db import models
from django.contrib.auth.models import User

from planner.planner_view_choices import *
from planner.category_color_choices import *
from planner.event_time_estimate_choices import *


class Planner(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length = 30, null = True)


# If a user doesn't have a planner, generate it, if a user already has a planner, get it

User.planner = property(lambda u: Planner.objects.get_or_create(user = u, name = u.get_username())[0])

class Category(models.Model):
	owner = models.ForeignKey(Planner)
	name = models.CharField(max_length = 30, default = "New Category")


class Event(models.Model):
	parentPlanner = models.ForeignKey(Planner)
	parentCategory = models.ForeignKey(Category)
