from django.forms import ModelForm

from planner.models import Planner, Category, Event

from planner.category_color_choices import *
from planner.event_time_estimate_choices import *
from planner.planner_view_choices import *


class PlannerViewForm(ModelForm):
	view = forms.ChoiceField(choices = VIEW_CHOICES, widget = forms.Select(), required = True)

	class Meta:
		model = Planner
		fields = ['view']


class PlannerMiscellaneousNotesForm(ModelForm):
	class Meta:
		model = Planner
		fields = ['miscellaneousNotes']


class CategoryForm(ModelForm):
	class Meta:
		model = Category
		fields = ['name', 'color', 'order']


class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = ['name', 'description', 'important', 'timeEstimate', 'timeStart', 'timeEnd', 'dateOfEvent', 'complete']


