from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from planner.planner_view_choices import *
from planner.category_color_choices import *
from planner.event_time_estimate_choices import *


#class PlannerManager(models.Manager):

class Planner(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length = 30, null = True)
	view = models.IntegerField(choices = VIEW_CHOICES, default = 2)
	miscellaneousNotes = models.TextField(verbose_name = "Miscellaneous", null = True)

	#objects = PlannerManager()

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name + "'s planner"

# If a user doesn't have a planner, generate it, if a user already has a planner, get it
User.planner = property(lambda u: Planner.objects.get_or_create(user = u, name = u.get_username())[0])

class CategoryManager(models.Manager):
	def create_category(self, request, name, color, order):
		# Given a planner's list of categories
		existingCategoryList = Category.objects.get_categories_in_order(request)
		temp = False
		orderAlreadyTakenIndex = 0

		if existingCategoryList.filter(name = name).exists():
			raise ValidationError("Categories cannot have duplicate names")
			
		# Check to see if the desired order position already exists
		for orderIndex in existingCategoryList:
			if orderIndex.order == order:
				orderAlreadyTakenIndex = orderIndex.order
				temp = True
		else:
			pass

		# If it does, insert it, and move every category after it +1 in order
		if temp == True:
			for orderIndex in existingCategoryList:
				if orderIndex.order < orderAlreadyTakenIndex:
					pass
				else:
					orderIndex.set_order(orderIndex.order + 1)
		# Else, append the category to the earliest available order
		else:
			appendCategoryOrderNumber = len(existingCategoryList)
			order = appendCategoryOrderNumber

		plannerId = request.planner
		return self.create(owner = plannerId, name = name,
			color = color, order = order)

	def get_categories(self, request):
		plannerId = request.planner.id
		return super(CategoryManager, self).filter(owner = plannerId)

	def get_categories_in_order(self, request):
		plannerId = request.planner.id
		return super(CategoryManager, self).filter(owner = plannerId).order_by('order')

	def get_category_by_name(self, request, name):
		plannerId = request.planner.id
		existingCategoryList = super(CategoryManager, self).filter(owner = plannerId)
		desiredCategory = existingCategoryList.get(name = name)
		return desiredCategory

	def update_category_name(self, request, currentName, newName):
		plannerId = request.planner.id
		desiredCategoryToUpdate = super(CategoryManager, self).filter(owner = plannerId).get(name = currentName)
		desiredCategoryToUpdate.set_name(newName)

	def update_category_color(self, request, name, newColor):
		plannerId = request.planner.id
		desiredCategoryToUpdate = super(CategoryManager, self).filter(owner = plannerId).get(name = currentName)
		desiredCategoryToUpdate.set_color(newColor)

	def update_category_order(self, request, name, newOrder):
		plannerId = request.planner.id
		existingCategoryList = super(CategoryManager, self).filter(owner = plannerId)
		desiredCategoryToUpdate = existingCategoryList.get(name = name)

		temp = False
		orderAlreadyTakenIndex = 0

		# Check to see if the desired order position already exists
		for orderIndex in existingCategoryList:
			if orderIndex.order == newOrder:
				orderAlreadyTakenIndex = orderIndex.order
				temp = True
		else:
			pass

		# If it does, insert it, and move every category after it +1 in order
		if temp == True:
			for orderIndex in existingCategoryList:
				if orderIndex.order < orderAlreadyTakenIndex:
					pass
				else:
					orderIndex.set_order(orderIndex.order + 1)

		desiredCategoryToUpdate.set_order(newOrder)
		
	def delete_category(self, request, name):
		existingCategoryList = Category.objects.get_categories_in_order(request)
		categoryToDelete = existingCategoryList.get(name = name)
		categoryToDeleteOrder = categoryToDelete.order

		for orderIndex in existingCategoryList:
			if orderIndex.order < categoryToDeleteOrder:
				pass
			else:
				orderIndex.set_order(orderIndex.order - 1)

		return categoryToDelete.delete()

class Category(models.Model):
	owner = models.ForeignKey(Planner)
	name = models.CharField(max_length = 30, default = "New Category")
	color = models.IntegerField(choices = CATEGORY_COLOR_CHOICES, default = 10)
	order = models.IntegerField(default = 0)

	objects = CategoryManager()

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name

	def set_color(self, color):
		self.color = color
		self.save()

	def get_color(self):
		return self.color

	def set_name(self, name):
		self.name = name
		self.save()

	def get_name(self):
		return self.name

	def set_order(self, order):
		self.order = order
		self.save()

	def get_order(self):
		return self.order

#class EventManager(models.Manager):


class Event(models.Model):
	parentPlanner = models.ForeignKey(Planner)
	parentCategory = models.ForeignKey(Category)
	name = models.CharField(max_length = 60, default = "Name")
	description = models.CharField(max_length = 500, default = "Description")
	important = models.BooleanField(default = False)
	timeEstimate = models.IntegerField(choices = TIME_ESTIMATE_CHOICES, default = 1)
	timeStart = models.TimeField(auto_now = False, auto_now_add = False, null = True)
	timeEnd = models.TimeField(auto_now = False, auto_now_add = False, null = True)
	complete = models.BooleanField(default = False)

	#objects = EventManager()

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name

