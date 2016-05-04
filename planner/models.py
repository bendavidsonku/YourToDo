import calendar
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import string
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from planner.category_color_choices import *
from planner.event_time_estimate_choices import *
from planner.planner_view_choices import *

class PlannerManager(models.Manager):
	def get_planner(self, request):
		return super(PlannerManager, self).filter(user = request)


class Planner(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length = 30, null = True)
	miscellaneousNotes = models.TextField(verbose_name = "Miscellaneous", null = True)

	objects = PlannerManager()

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name + "'s planner"

	def set_name(self, name):
		self.name = name
		self.save()

	def get_name(self):
		return self.name

	def set_miscellaneousNotes(self, miscellaneousNotes):
		self.miscellaneousNotes = miscellaneousNotes
		self.save()

	def get_miscellaneousNotes(self):
		return self.miscellaneousNotes


# If a user doesn't have a planner, generate it, if a user already has a planner, get it
User.planner = property(lambda u: Planner.objects.get_or_create(user = u, name = u.get_username().capitalize())[0])


class CategoryManager(models.Manager):
	def create_category(self, request, name, color, order):
		# Given a planner's list of categories
		existingCategoryList = Category.objects.get_categories_in_order(request)
		temp = False
		orderAlreadyTakenIndex = 0

		if len(existingCategoryList) == 10:
			raise ValidationError("A planner can only hold 10 categories")

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

	def get_category_by_user_and_id(self, request, id):
		plannerId = request.planner.id
		existingCategoryList = super(CategoryManager, self).filter(owner = plannerId)
		desiredCategory = existingCategoryList.get(id = id)
		return desiredCategory

	def get_category_by_name(self, request, name):
		plannerId = request.planner.id
		existingCategoryList = super(CategoryManager, self).filter(owner = plannerId)
		desiredCategory = existingCategoryList.get(name = name)
		return desiredCategory

	def update_category_name(self, request, currentName, newName):
		plannerId = request.planner.id
		desiredCategoryToUpdate = super(CategoryManager, self).filter(owner = plannerId).get(name = currentName)

		existingCategoryList = Category.objects.get_categories(request)

		if existingCategoryList.filter(name = newName).exists():
			raise ValidationError("Categories cannot have duplicate names")
		else:
			desiredCategoryToUpdate.set_name(newName)

	def update_category_order(self, request, id, newOrder):
		plannerId = request.planner.id
		existingCategoryList = Category.objects.get_categories_in_order(request)
		desiredCategoryToUpdate = existingCategoryList.get(id = id)
		originalCategoryOrder = desiredCategoryToUpdate.get_order()

		if newOrder > originalCategoryOrder:
			for category in existingCategoryList:
				if category.get_order() <= newOrder and category.get_order() > originalCategoryOrder:
					category.set_order(category.get_order() - 1)
		elif newOrder < originalCategoryOrder:
			for category in existingCategoryList:
				if category.get_order() >= newOrder and category.get_order() < originalCategoryOrder:
					category.set_order(category.get_order() + 1)

		desiredCategoryToUpdate.set_order(newOrder)
		
	def delete_category(self, request, id):
		existingCategoryList = Category.objects.get_categories_in_order(request)
		categoryToDelete = existingCategoryList.get(id = id)
		categoryToDeleteOrder = categoryToDelete.get_order()

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

	def get_category_id(self):
		return self.id

	def set_color(self, color):
		self.color = color
		self.save()

	def get_color(self):
		return self.color

	def get_color_forHTML(self):
		if self.color == 1:
			return "Red"
		elif self.color == 2:
			return "Dark Red"
		elif self.color == 3:
			return "Light Red"
		elif self.color == 4:
			return "Blue"
		elif self.color == 5:
			return "Dark Blue"
		elif self.color == 6:
			return "Light Blue"
		elif self.color == 7:
			return "Green"
		elif self.color == 8:
			return "Dark Green"
		elif self.color == 9:
			return "Light Green"
		elif self.color == 10:
			return "Yellow"
		elif self.color == 11:
			return "Gold"
		elif self.color == 12:
			return "Orange"
		elif self.color == 13:
			return "Pink"
		elif self.color == 14:
			return "Turquoise"
		elif self.color == 15:
			return "Navy"
		else:
			pass

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

class RecurringEventReferenceManager(models.Manager):
	def create_recurringEventReference(self, listOfDaysToOccur, periodOfRecurrence, recurrenceType, sameDayOrSameDayOfWeek, nthOccurrenceOfEventDate, dateOfFirstEvent):
		return self.create(listOfDaysToOccur = listOfDaysToOccur, periodOfRecurrence = periodOfRecurrence, recurrenceType = recurrenceType, sameDayOrSameDayOfWeek = sameDayOrSameDayOfWeek, nthOccurrenceOfEventDate = nthOccurrenceOfEventDate, dateOfFirstEvent = dateOfFirstEvent)

	def generate_listOfDaysToOccur_String(self, dayHolderArray):
		generatedString = ""
		for i in range(0, 7):
			generatedString = generatedString + str(dayHolderArray[i])

		return generatedString

	def get_listOfDaysToOccurAsList(self, dayHolderString):
		dayHolderArray = []
		for i in range(0, 7):
			dayHolderArray.append(int(dayHolderString[i]))

		return dayHolderArray

class RecurringEventReference(models.Model):
	listOfDaysToOccur = models.TextField(max_length = 7, null = True)
	periodOfRecurrence = models.IntegerField(default = 0)
	# 0: daily, 1: weekly, 2: monthly, 3: yearly
	recurrenceType = models.IntegerField(default = 0)
	sameDayOrSameDayOfWeek = models.NullBooleanField(default = True, null = True)
	nthOccurrenceOfEventDate = models.CharField(max_length = 1, null = True)
	dateOfFirstEvent = models.DateField(auto_now = False, auto_now_add = False, default = datetime.now, null = True)

	objects = RecurringEventReferenceManager()

	def get_recurringEventReference_id(self):
		return self.id

	def get_listOfDaysToOccur(self):
		return self.listOfDaysToOccur

	def set_listOfDaysToOccur(self, listOfDaysToOccur):
		self.listOfDaysToOccur = listOfDaysToOccur
		self.save()

	def get_periodOfRecurrence(self):
		return self.periodOfRecurrence

	def set_periodOfRecurrence(self, periodOfRecurrence):
		self.periodOfRecurrence = periodOfRecurrence
		self.save()

	def get_recurrenceType(self):
		return self.recurrenceType

	def set_recurrenceType(self, recurrenceType):
		self.recurrenceType = recurrenceType
		self.save()

	def get_sameDayOrSameDayOfWeek(self):
		return self.sameDayOrSameDayOfWeek

	def set_sameDayOrSameDayOfWeek(self, sameDayOrSameDayOfWeek):
		self.sameDayOrSameDayOfWeek = sameDayOrSameDayOfWeek
		self.save()

	def get_nthOccurrenceOfEventDate(self):
		return self.nthOccurrenceOfEventDate

	def set_nthOccurrenceOfEventDate(self, nthOccurrenceOfEventDate):
		self.nthOccurrenceOfEventDate = nthOccurrenceOfEventDate
		self.save()

	def get_dateOfFirstEvent(self):
		return self.dateOfFirstEvent

	def set_dateOFFirstEvent(self, dateOfFirstEvent):
		self.dateOfFirstEvent = dateOfFirstEvent
		self.save()

	def get_neverEnding(self):
		return self.neverEnding

	def set_neverEnding(self, neverEnding):
		self.neverEnding = neverEnding
		self.save()


class EventManager(models.Manager):
	def create_event(self, request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, recurrenceReference, neverEnding):
		plannerId = request.planner
		categoryId = Category.objects.get_category_by_name(request, categoryName)

		if (timeStart == "" or timeEnd == ""):
			return self.create(parentPlanner = plannerId, parentCategory = categoryId, dateOfEvent = dateOfEvent, name = name,
			description = description, important = important, timeEstimate = timeEstimate, recurrenceReference = recurrenceReference, neverEnding = neverEnding)
		else:
			return self.create(parentPlanner = plannerId, parentCategory = categoryId, dateOfEvent = dateOfEvent, name = name,
			description = description, important = important, timeEstimate = timeEstimate, timeStart = timeStart, timeEnd = timeEnd, recurrenceReference = recurrenceReference, neverEnding = neverEnding)

	# Given a user specified number of times to occur, create daily event
	def create_daily_recurring_event_given_number_to_repeat(self, request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, periodOfRecurrence, numberOfTimesToRepeat):
		plannerId = request.planner
		categoryId = Category.objects.get_category_by_name(request, categoryName)

		dateOfEvent = datetime.strptime(dateOfEvent, "%Y-%m-%d")

		tempRecurrenceReference = RecurringEventReference.objects.create_recurringEventReference(None, periodOfRecurrence, 0, None, None, None)

		for i in range(0, int(numberOfTimesToRepeat)):
			self.create_event(request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
			dateOfEvent = dateOfEvent + timedelta(days = int(periodOfRecurrence))

		return

	# Given a user specified date to stop, create event until stop date is reached
	def create_daily_recurring_event_given_stop_date(self, request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, periodOfRecurrence, dateToStop, originalDateOfNeverEndingEvent, recurrenceReference):
		plannerId = request.planner
		categoryId = Category.objects.get_category_by_name(request, categoryName)

		dateToStop = datetime.strptime(dateToStop, "%Y-%m-%d")
		dateOfEvent = datetime.strptime(dateOfEvent, "%Y-%m-%d")
		originalDateOfNeverEndingEvent = originalDateOfNeverEndingEvent

		if recurrenceReference == None:
			tempRecurrenceReference = RecurringEventReference.objects.create_recurringEventReference(None, periodOfRecurrence, 0, None, None, None)
		else:
			tempRecurrenceReference = recurrenceReference

		if originalDateOfNeverEndingEvent == None:
			while dateOfEvent <= dateToStop:
				self.create_event(request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
				dateOfEvent = dateOfEvent + timedelta(days = int(periodOfRecurrence))

		else:
			originalDateOfNeverEndingEvent = datetime.combine(originalDateOfNeverEndingEvent, datetime.min.time())
			while dateOfEvent <= dateToStop and dateOfEvent >= originalDateOfNeverEndingEvent:
				self.create_event(request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
				dateOfEvent = dateOfEvent + timedelta(days = int(periodOfRecurrence))

		return

	# User specified that daily recurring event should never end
	def create_never_ending_daily_event(self, request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, periodOfRecurrence):
		plannerId = request.planner
		categoryId = Category.objects.get_category_by_name(request, categoryName)

		dateOfFirstEvent = datetime.strptime(dateOfEvent, "%Y-%m-%d")
		
		tempRecurrenceReference = RecurringEventReference.objects.create_recurringEventReference(None, periodOfRecurrence, 0, None, None, dateOfFirstEvent)

		self.create_event(request, categoryName, dateOfFirstEvent, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, True)

		return

	# Given a user specified number of times to occur, create weekly event
	def create_weekly_recurring_event_given_number_to_repeat(self, request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, periodOfRecurrence, numberOfTimesToRepeat, dayHolderArray):
		plannerId = request.planner
		categoryId = Category.objects.get_category_by_name(request, categoryName)

		dateOfEvent = datetime.strptime(dateOfEvent, "%Y-%m-%d")

		if dayHolderArray == None:
			tempRecurrenceReference = RecurringEventReference.objects.create_recurringEventReference(None, periodOfRecurrence, 1, None, None, None)
			for i in range(0, int(numberOfTimesToRepeat)):
				self.create_event(request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
				dateOfEvent = dateOfEvent + timedelta(weeks = int(periodOfRecurrence))

		else:
			# Fix dateOfEvent for example case: user chooses Saturday, 4/16 but specifies Tues & Wednesday for event to repeat
			# This fix will effectively change dateOfEvent to the next available Tuesday
			dateOfEventFixed = self.fix_dateOfEvent_for_weekly_events(dateOfEvent, dayHolderArray)

			dayHolderString = RecurringEventReference.objects.generate_listOfDaysToOccur_String(dayHolderArray)
			tempRecurrenceReference =  RecurringEventReference.objects.create_recurringEventReference(dayHolderString, periodOfRecurrence, 1, None, None, None)

			sundayOfCurrentWeek = dateOfEventFixed

			while sundayOfCurrentWeek.weekday() != 6:
				sundayOfCurrentWeek = sundayOfCurrentWeek - timedelta(days = 1)

			for i in range(0, int(numberOfTimesToRepeat)):
				tempDate = sundayOfCurrentWeek
				for j in range(0,7):
					if dayHolderArray[tempDate.weekday()] == 1 and tempDate >= dateOfEventFixed:
						self.create_event(request, categoryName, tempDate, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
					tempDate = tempDate + timedelta(days = 1)

				sundayOfCurrentWeek = sundayOfCurrentWeek + timedelta(weeks = int(periodOfRecurrence))

		return



	# Given a user specified date to stop, create event until stop date is reached
	def create_weekly_recurring_event_given_stop_date(self, request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, periodOfRecurrence, dateToStop, dayHolderArray, originalDateOfNeverEndingEvent, recurrenceReference):
		plannerId = request.planner
		categoryId = Category.objects.get_category_by_name(request, categoryName)

		dateToStop = datetime.strptime(dateToStop, "%Y-%m-%d")
		dateOfEvent = datetime.strptime(dateOfEvent, "%Y-%m-%d")

		if dayHolderArray == None:
			tempRecurrenceReference = RecurringEventReference.objects.create_recurringEventReference(None, periodOfRecurrence, 1, None, None, None)

			if originalDateOfNeverEndingEvent == None:
				while dateOfEvent <= dateToStop:
					self.create_event(request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
					dateOfEvent = dateOfEvent + timedelta(weeks = int(periodOfRecurrence))
			else:
				originalDateOfNeverEndingEvent = datetime.combine(originalDateOfNeverEndingEvent, datetime.min.time())
				while dateOfEvent <= dateToStop and dateOfEvent >= originalDateOfNeverEndingEvent:
					self.create_event(request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
					dateOfEvent = dateOfEvent + timedelta(weeks = int(periodOfRecurrence))
		else:
			# Fix dateOfEvent for example case: user chooses Saturday, 4/16 but specifies Tues & Wednesday for event to repeat
			# This fix will effectively change dateOfEvent to the next available Tuesday
			dateOfEventFixed = self.fix_dateOfEvent_for_weekly_events(dateOfEvent, dayHolderArray)

			dayHolderString = RecurringEventReference.objects.generate_listOfDaysToOccur_String(dayHolderArray)

			if recurrenceReference == None:
				tempRecurrenceReference =  RecurringEventReference.objects.create_recurringEventReference(dayHolderString, periodOfRecurrence, 1, None, None, None)
			else:
				tempRecurrenceReference = recurrenceReference

			sundayOfCurrentWeek = dateOfEventFixed

			while sundayOfCurrentWeek.weekday() != 6:
				sundayOfCurrentWeek = sundayOfCurrentWeek - timedelta(days = 1)

			if originalDateOfNeverEndingEvent == None:
				while sundayOfCurrentWeek <= dateToStop:
					tempDate = sundayOfCurrentWeek
					for i in range(0,7):
						if dayHolderArray[tempDate.weekday()] == 1 and tempDate <= dateToStop and tempDate >= dateOfEventFixed:
							self.create_event(request, categoryName, tempDate, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
						tempDate = tempDate + timedelta(days = 1)

					sundayOfCurrentWeek = sundayOfCurrentWeek + timedelta(weeks = int(periodOfRecurrence))
			else:
				originalDateOfNeverEndingEvent = datetime.combine(originalDateOfNeverEndingEvent, datetime.min.time())
				while sundayOfCurrentWeek <= dateToStop:
					tempDate = sundayOfCurrentWeek
					for i in range(0,7):
						if dayHolderArray[tempDate.weekday()] == 1 and tempDate <= dateToStop and tempDate >= dateOfEventFixed and tempDate >= originalDateOfNeverEndingEvent:
							self.create_event(request, categoryName, tempDate, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
						tempDate = tempDate + timedelta(days = 1)

					sundayOfCurrentWeek = sundayOfCurrentWeek + timedelta(weeks = int(periodOfRecurrence))

		return

	# User specified that weekly recurring event should never end
	def create_never_ending_weekly_event(self, request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, periodOfRecurrence, dayHolderArray):
		plannerId = request.planner
		categoryId = Category.objects.get_category_by_name(request, categoryName)

		dateOfFirstEvent = datetime.strptime(dateOfEvent, "%Y-%m-%d")

		if dayHolderArray == None:
			pass
		else:
			dateOFFirstEventFixed = self.fix_dateOfEvent_for_weekly_events(dateOfFirstEvent, dayHolderArray)
			tempDayHolderString = RecurringEventReference.objects.generate_listOfDaysToOccur_String(dayHolderArray)

		tempRecurrenceReference = RecurringEventReference.objects.create_recurringEventReference(tempDayHolderString, periodOfRecurrence, 1, None, None, dateOFFirstEventFixed)

		return self.create_event(request, categoryName, dateOFFirstEventFixed, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, True)


	# Returns corrected DateOfEvent
	def fix_dateOfEvent_for_weekly_events(self, dateOfEvent, dayHolderArray):
		if dateOfEvent.weekday() == 6:
			return dateOfEvent
		else:
			lastDayOfTheWeekInDayHolderArray = 0
			for i in range(0,6):
				if dayHolderArray[i] == 1:
					lastDayOfTheWeekInDayHolderArray = i

			while dateOfEvent.weekday() > lastDayOfTheWeekInDayHolderArray:
				dateOfEvent = dateOfEvent + timedelta(days = 1)

			return dateOfEvent

	def create_monthly_recurring_event_given_number_to_repeat(self, request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, periodOfRecurrence, numberOfTimesToRepeat, sameDayOrSameDayOfWeek, nthOccurrenceOfSelectedDate):
		plannerId = request.planner
		categoryId = Category.objects.get_category_by_name(request, categoryName)		

		dateOfEvent = datetime.strptime(dateOfEvent, "%Y-%m-%d")

		# If sameDayOrSameDayOfWeek is true, treat as same-day-next-month creation, else treat as same-day-of-week-next-month creation
		if sameDayOrSameDayOfWeek == True:
			tempRecurrenceReference =  RecurringEventReference.objects.create_recurringEventReference(None, periodOfRecurrence, 2, True, None, None)

			if dateOfEvent.day == 31:
				for i in range(0, int(numberOfTimesToRepeat)):
					dateOfEvent = datetime(dateOfEvent.year, dateOfEvent.month, 1) + relativedelta(months = 1, days = -1)
					self.create_event(request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
					dateOfEvent = dateOfEvent + relativedelta(months = int(periodOfRecurrence))
			else:
				for i in range(0, int(numberOfTimesToRepeat)):
					self.create_event(request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
					dateOfEvent = dateOfEvent + relativedelta(months = int(periodOfRecurrence))

		else:
			originalDayOfEventDate = dateOfEvent.weekday()
			firstDayOfMonthOfEventDate = dateOfEvent.replace(day = 1)
			nthOccurrenceOfSelectedDateAsInt = int(nthOccurrenceOfSelectedDate)

			tempRecurrenceReference =  RecurringEventReference.objects.create_recurringEventReference(None, periodOfRecurrence, 2, False, nthOccurrenceOfSelectedDate, None)

			for i in range(0, int(numberOfTimesToRepeat)):
				tempDate = self.find_date_of_nth_recurrence_of_given_weekday(firstDayOfMonthOfEventDate, nthOccurrenceOfSelectedDateAsInt, originalDayOfEventDate)
				self.create_event(request, categoryName, tempDate, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
				firstDayOfMonthOfEventDate = firstDayOfMonthOfEventDate + relativedelta(months = int(periodOfRecurrence))

		return

	def create_monthly_recurring_event_given_stop_date(self, request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, periodOfRecurrence, dateToStop, sameDayOrSameDayOfWeek, nthOccurrenceOfSelectedDate, plannerViewStartDate, recurrenceReference):
		plannerId = request.planner
		categoryId = Category.objects.get_category_by_name(request, categoryName)		

		dateToStop = datetime.strptime(dateToStop, "%Y-%m-%d")
		dateOfEvent = datetime.strptime(dateOfEvent, "%Y-%m-%d")

		# Fix plannerViewStartDate
		if plannerViewStartDate != None:
			plannerViewStartDate = datetime.strptime(plannerViewStartDate, "%Y-%m-%d")

		# If sameDayOrSameDayOfWeek is true, treat as same-day-next-month creation, else treat as same-day-of-week-next-month creation
		if sameDayOrSameDayOfWeek == True:
			if recurrenceReference == None:
				tempRecurrenceReference = RecurringEventReference.objects.create_recurringEventReference(None, periodOfRecurrence, 2, True, None, None)
			else:
				tempRecurrenceReference = recurrenceReference

			if plannerViewStartDate == None:
				if dateOfEvent.day == 31:
					while dateOfEvent <= dateToStop:
						dateOfEvent = datetime(dateOfEvent.year, dateOfEvent.month, 1) + relativedelta(months = 1, days = -1)
						self.create_event(request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
						dateOfEvent = dateOfEvent + relativedelta(months = int(periodOfRecurrence))
				else:
					while dateOfEvent <= dateToStop:
						self.create_event(request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
						dateOfEvent = dateOfEvent + relativedelta(months = int(periodOfRecurrence))
			else:
				if dateOfEvent.day == 31:
					while dateOfEvent <= dateToStop:
						dateOfEvent = datetime(dateOfEvent.year, dateOfEvent.month, 1) + relativedelta(months = 1, days = -1)
						if dateOfEvent >= plannerViewStartDate:
							self.create_event(request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
						dateOfEvent = dateOfEvent + relativedelta(months = int(periodOfRecurrence))
				else:
					while dateOfEvent <= dateToStop:
						if dateOfEvent >= plannerViewStartDate:
							self.create_event(request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
						dateOfEvent = dateOfEvent + relativedelta(months = int(periodOfRecurrence))
		else:
			originalDayOfEventDate = dateOfEvent.weekday()
			firstDayOfMonthOfEventDate = dateOfEvent.replace(day = 1)
			nthOccurrenceOfSelectedDateAsInt = int(nthOccurrenceOfSelectedDate)

			if recurrenceReference == None:
				tempRecurrenceReference = RecurringEventReference.objects.create_recurringEventReference(None, periodOfRecurrence, 2, True, None, None)
			else:
				tempRecurrenceReference = recurrenceReference

			if plannerViewStartDate == None:
				while firstDayOfMonthOfEventDate <= dateToStop:
					tempDate = self.find_date_of_nth_recurrence_of_given_weekday(firstDayOfMonthOfEventDate, nthOccurrenceOfSelectedDateAsInt, originalDayOfEventDate)
					if tempDate <= dateToStop:
						self.create_event(request, categoryName, tempDate, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
					firstDayOfMonthOfEventDate = firstDayOfMonthOfEventDate + relativedelta(months = int(periodOfRecurrence))
			else:
				while firstDayOfMonthOfEventDate <= dateToStop:
					tempDate = self.find_date_of_nth_recurrence_of_given_weekday(firstDayOfMonthOfEventDate, nthOccurrenceOfSelectedDateAsInt, originalDayOfEventDate)
					if tempDate <= dateToStop and tempDate >= plannerViewStartDate:
						self.create_event(request, categoryName, tempDate, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
					firstDayOfMonthOfEventDate = firstDayOfMonthOfEventDate + relativedelta(months = int(periodOfRecurrence))

		return

	def create_never_ending_monthly_event(self, request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, periodOfRecurrence, sameDayOrSameDayOfWeek, nthOccurrenceOfSelectedDate):
		plannerId = request.planner
		categoryId = Category.objects.get_category_by_name(request, categoryName)

		dateOfFirstEvent = datetime.strptime(dateOfEvent, "%Y-%m-%d")

		# If sameDayOrSameDayOfWeek is true, treat as same-day-next-month creation, else treat as same-day-of-week-next-month creation
		if sameDayOrSameDayOfWeek == True:
			tempRecurrenceReference = RecurringEventReference.objects.create_recurringEventReference(None, periodOfRecurrence, 2, True, None, dateOfFirstEvent)
		else:
			tempRecurrenceReference = RecurringEventReference.objects.create_recurringEventReference(None, periodOfRecurrence, 2, False, nthOccurrenceOfSelectedDate, dateOfFirstEvent)

		self.create_event(request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, True)

		return

	# Helper function for creating monthly recurring events
	def find_date_of_nth_recurrence_of_given_weekday(self, dateOfEvent, nthOccurrenceOfSelectedDate, weekday):
		if (nthOccurrenceOfSelectedDate == 5):
			tempDate = datetime(dateOfEvent.year, dateOfEvent.month, 1) + relativedelta(months = 1, days = -1)

			while tempDate.weekday() != weekday:
				tempDate = tempDate - timedelta(days = 1)

			return tempDate

		else:
			tempDate = dateOfEvent
			tempAdjust = (weekday - tempDate.weekday()) % 7
			tempDate = tempDate + timedelta(days = tempAdjust)

			return (tempDate + timedelta(weeks = nthOccurrenceOfSelectedDate - 1))

	def create_yearly_recurring_event_given_number_to_repeat(self, request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, periodOfRecurrence, numberOfTimesToRepeat):
		plannerId = request.planner
		categoryId = Category.objects.get_category_by_name(request, categoryName)

		dateOfEvent = datetime.strptime(dateOfEvent, "%Y-%m-%d")

		tempRecurrenceReference = RecurringEventReference.objects.create_recurringEventReference(None, periodOfRecurrence, 3, None, None, None)

		for i in range(0, int(numberOfTimesToRepeat)):
			self.create_event(request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
			dateOfEvent = dateOfEvent + relativedelta(years = int(periodOfRecurrence))

		return

	def create_yearly_recurring_event_given_stop_date(self, request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, periodOfRecurrence, dateToStop):
		plannerId = request.planner
		categoryId = Category.objects.get_category_by_name(request, categoryName)

		dateToStop = datetime.strptime(dateToStop, "%Y-%m-%d")
		dateOfEvent = datetime.strptime(dateOfEvent, "%Y-%m-%d")

		tempRecurrenceReference = RecurringEventReference.objects.create_recurringEventReference(None, periodOfRecurrence, 3, None, None, None)

		while dateOfEvent <= dateToStop:
			self.create_event(request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, False)
			dateOfEvent = dateOfEvent + relativedelta(years = int(periodOfRecurrence))

		return

	def create_never_ending_yearly_event(self, request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, periodOfRecurrence):
		plannerId = request.planner
		categoryId = Category.objects.get_category_by_name(request, categoryName)

		dateOfFirstEvent = datetime.strptime(dateOfEvent, "%Y-%m-%d")

		tempRecurrenceReference = tempRecurrenceReference = RecurringEventReference.objects.create_recurringEventReference(None, periodOfRecurrence, 3, None, None, dateOfFirstEvent)

		self.create_event(request, categoryName, dateOfFirstEvent, name, description, important, timeEstimate, timeStart, timeEnd, tempRecurrenceReference, True)

		return

	def create_never_ending_yearly_event_dynamically(self, request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, periodOfRecurrence, dateToStop, plannerViewStartDate, recurrenceReference):
		plannerId = request.planner
		categoryId = Category.objects.get_category_by_name(request, categoryName)

		dateToStop = datetime.strptime(dateToStop, "%Y-%m-%d")
		dateOfEvent = datetime.strptime(dateOfEvent, "%Y-%m-%d")

		# Fix plannerViewStartDate
		if plannerViewStartDate != None:
			plannerViewStartDate = datetime.strptime(plannerViewStartDate, "%Y-%m-%d")

			while dateOfEvent <= dateToStop:
				if dateOfEvent >= plannerViewStartDate:
					self.create_event(request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, recurrenceReference, False)
				dateOfEvent = dateOfEvent + relativedelta(years = int(periodOfRecurrence))
		else:
			while dateOfEvent <= dateToStop:
				self.create_event(request, categoryName, dateOfEvent, name, description, important, timeEstimate, timeStart, timeEnd, recurrenceReference, False)
				dateOfEvent = dateOfEvent + relativedelta(years = int(periodOfRecurrence))

		return

	def get_single_event_by_user_and_id(self, request, id):
		existingEventsInPlanner = Event.objects.get_all_events(request)
		return existingEventsInPlanner.get(id = id)

	def get_event_list(self, request, categoryName):
		plannerId = request.planner.id
		categoryId = Category.objects.get_category_by_name(request, categoryName).get_category_id()
		return super(EventManager, self).filter(parentPlanner = plannerId).filter(parentCategory = categoryId)

	def get_all_events_in_date_order(self, request):
		plannerId = request.planner.id
		return super(EventManager, self).filter(parentPlanner = plannerId).order_by('dateOfEvent')

	def get_all_events(self, request):
		plannerId = request.planner.id
		return super(EventManager, self).filter(parentPlanner = plannerId)

	def delete_event(self, request, id):
		eventToDelete = Event.objects.get_single_event_by_user_and_id(request, id)
		return eventToDelete.delete()

class Event(models.Model):
	parentPlanner = models.ForeignKey(Planner)
	parentCategory = models.ForeignKey(Category)
	name = models.CharField(max_length = 60, default = "Name")
	description = models.CharField(max_length = 500, default = "Description")
	important = models.BooleanField(default = False)
	timeEstimate = models.IntegerField(choices = TIME_ESTIMATE_CHOICES, default = 1)
	timeStart = models.TimeField(auto_now = False, auto_now_add = False, null = True)
	timeEnd = models.TimeField(auto_now = False, auto_now_add = False, null = True)
	dateOfEvent = models.DateField(auto_now = False, auto_now_add = False, default = datetime.now)
	complete = models.BooleanField(default = False)
	recurrenceReference = models.ForeignKey(RecurringEventReference, null = True)
	neverEnding = models.BooleanField(default = False)

	objects = EventManager()

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name

	def get_event_id(self):
		return self.id

	def get_parentCategory(self):
		return self.parentCategory

	def set_parentCategory(self, parentCategory):
		self.parentCategory = parentCategory
		self.save()

	def set_dateOfEvent(self, dateOfEvent):
		self.dateOfEvent = dateOfEvent
		self.save()

	def get_dateOfEvent(self):
		return self.dateOfEvent

	def get_dateOfEvent_forHTML(self):
		dateInHTMLFormat = self.dateOfEvent.strftime("%Y-%m-%d")
		return dateInHTMLFormat

	def set_name(self, name):
		self.name = name
		self.save()

	def get_name(self):
		return self.name

	def set_description(self, description):
		self.description = description
		self.save()

	def get_description(self):
		return self.description

	def set_important(self, important):
		self.important = important
		self.save()

	def get_important(self):
		return self.important

	def set_timeEstimate(self, timeEstimate):
		self.timeEstimate = timeEstimate
		self.save()

	def get_timeEstimate(self):
		return self.timeEstimate

	def get_timeEstimate_forHTML(self):
		if self.timeEstimate == 1:
			return "--"
		elif self.timeEstimate == 2:
			return "15 minutes"
		elif self.timeEstimate == 3:
			return "30 minutes"
		elif self.timeEstimate == 4:
			return "45 minutes"
		elif self.timeEstimate == 5:
			return "1 hour"
		elif self.timeEstimate == 6:
			return "2 hours"
		elif self.timeEstimate == 7:
			return "3 hours"
		elif self.timeEstimate == 8:
			return "4 hours"
		elif self.timeEstimate == 9:
			return "5 hours"
		elif self.timeEstimate == 10:
			return "6 hours"
		elif self.timeEstimate == 11:
			return "7 hours"
		elif self.timeEstimate == 12:
			return "8 hours"
		elif self.timeEstimate == 13:
			return "More than 8 hours"
		else:
			pass

	def set_timeStart(self, timeStart):
		self.timeStart = timeStart
		self.save()

	def get_timeStart(self):
		return self.timeStart

	def get_timeStart_forHTML(self):
		timeInHTMLFormat = self.timeStart.strftime("%H:%M")
		return(timeInHTMLFormat)

	def set_timeEnd(self, timeEnd):
		self.timeEnd = timeEnd
		self.save()

	def get_timeEnd(self):
		return self.timeEnd

	def get_timeEnd_forHTML(self):
		timeInHTMLFormat = self.timeEnd.strftime("%H:%M")
		return(timeInHTMLFormat)

	def set_complete(self, complete):
		self.complete = complete
		self.save()

	def get_complete(self):
		return self.complete

	def get_recurrenceReference(self):
		return self.recurrenceReference

	def set_recurrenceReference(self, recurrenceReference):
		self.recurrenceReference = recurrenceReference
		self.save()
