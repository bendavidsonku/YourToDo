import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import math

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from YourToDo.forms import ContactForm
from planner.models import Planner, Category, Event, RecurringEventReference
from userprofile.models import UserProfile
from userprofile.forms import UserAccountSettingsImageUploadForm

# Static Page Views
def about(request):
    return render_to_response('static/about.html', context_instance = RequestContext(request))

def contact(request):
    args = {}
    args.update(csrf(request))

    if request.method == 'POST':
        form = ContactForm(request.POST)
        args['form'] = form
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            message += "\n\r" + form.cleaned_data['name']
            sender = form.cleaned_data['sender']

            recipients = ['ytdplanner@gmail.com']

            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/contact_success/')
    else:
        args['form'] = ContactForm()

    return render_to_response('static/contact.html', args, context_instance = RequestContext(request))

def contact_success(request):
        return render_to_response('static/contact_success.html')

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')

@login_required
def loadUpdateAccountInformation(request):
    context = {}

    loadUpdateAccountInformationForm = request.POST.get("load_user_information_form", "")

    if loadUpdateAccountInformationForm == "ready":
        username = None

        if request.user.is_authenticated():
            username = request.user.username

        user = User.objects.get(username = username)

        context['user'] = user
        context['userProfile'] = user.profile

        profilePictureForm = UserAccountSettingsImageUploadForm(request.POST, instance = request.user.profile)

        context['profilePictureForm'] = profilePictureForm

        return render_to_response('userprofile/user-account-information.html', context, context_instance = RequestContext(request))


    return render_to_response('userprofile/ajax_user_account_information_container.html', context, context_instance = RequestContext(request))


def updateAccountInformation(request):
    typeOfDataIncoming = request.POST.get("ajax_update_account_data_type", "")

    if typeOfDataIncoming == "html":
        updateUserProfileFirstName = request.POST.get("ajax_user_first_name", "")
        updateUserProfileLastName = request.POST.get("ajax_user_last_name", "")
        updateUserProfilePhoneNumber = request.POST.get("ajax_user_phone_number", "")
        updateUserProfileDateOfBirth = request.POST.get("ajax_user_date_of_birth", "")

        username = None

        if request.user.is_authenticated():
            username = request.user.username

        user = User.objects.get(username = username)

        oldUserProfile = user.profile

        if oldUserProfile.get_firstName() != updateUserProfileFirstName:
            oldUserProfile.set_firstName(updateUserProfileFirstName)

        if oldUserProfile.get_lastName() != updateUserProfileLastName:
            oldUserProfile.set_lastName(updateUserProfileLastName)

        if oldUserProfile.get_phoneNumber() != updateUserProfilePhoneNumber:
            oldUserProfile.set_phoneNumber(updateUserProfilePhoneNumber)

        if oldUserProfile.get_dateOfBirth_forHTML() == None and updateUserProfileDateOfBirth != "":
            oldUserProfile.set_dateOfBirth(updateUserProfileDateOfBirth)
        elif oldUserProfile.get_dateOfBirth_forHTML() == None and updateUserProfileDateOfBirth == "":
            pass
        elif oldUserProfile.get_dateOfBirth_forHTML() != updateUserProfileDateOfBirth:
            if updateUserProfileDateOfBirth != "":
                oldUserProfile.set_dateOfBirth(updateUserProfileDateOfBirth)
            elif updateUserProfileDateOfBirth == "":
                oldUserProfile.set_dateOfBirth(None)

    return HttpResponse('')


@csrf_exempt
def updateUserProfilePicture(request):
    if request.method == 'POST':

        profilePictureForm = UserAccountSettingsImageUploadForm(request.POST, request.FILES, instance = request.user.profile)

        if profilePictureForm.is_valid():
            profilePictureForm.save()
            return HttpResponse('')

@login_required
def PlannerView(request):
    plannerLayoutSelection = request.POST.get("planner_layout", "")
    context = {}

    if plannerLayoutSelection == "Day":
        username = None
        if request.user.is_authenticated():
            username = request.user.username

        user = User.objects.get(username = username)
        # Get the necessary context to display
        context['planner'] = user.planner
        context['categoriesInPlanner'] = Category.objects.get_categories_in_order(user)
        context['eventsInPlanner'] = Event.objects.get_all_events(user)
        return render_to_response('planner/planner_day_view.html', context, context_instance = RequestContext(request))

    elif plannerLayoutSelection == "Week":
        username = None
        if request.user.is_authenticated():
            username = request.user.username

        user = User.objects.get(username = username)

        # Get the necessary context to display
        context['planner'] = user.planner
        
        return render_to_response('planner/planner_week_view.html', context, context_instance = RequestContext(request))

    elif plannerLayoutSelection == "Month":
        username = None
        if request.user.is_authenticated():
            username = request.user.username

        user = User.objects.get(username = username)
        # Get the necessary context to display
        context['planner'] = user.planner
        context['categoriesInPlanner'] = Category.objects.get_categories_in_order(user)
        context['eventsInPlanner'] = Event.objects.get_all_events(user)
        
        return render_to_response('planner/planner_month_view.html', context, context_instance = RequestContext(request))

    else:
        pass

    return render_to_response('planner/planner_base.html', context, context_instance = RequestContext(request))

def loadPlannerDayEvents(request):
    if request.method == 'POST':
        username = None
        if request.user.is_authenticated():
            username = request.user.username

            user = User.objects.get(username = username)
            
            # Process to get planner content to display
            context = {}
            context['categoriesInPlanner'] = Category.objects.get_categories_in_order(user)

            # Get the input start date
            date = request.POST.get("date", "")
            today = datetime.datetime.strptime(date, "%Y-%m-%d")

            untimedEvents = Event.objects.get_all_events(user).filter(timeStart = None)
            context['allDayEvents'] = untimedEvents.filter(dateOfEvent = today)

            timeBlocks = ['12 am', '1 am', '2 am', '3 am', '4 am', '5 am',
                          '6 am', '7 am', '8 am', '9 am', '10 am', '11 am',
                          '12 pm', '1 pm', '2 pm', '3 pm', '4 pm', '5 pm',
                          '6 pm', '7 pm', '8 pm', '9 pm', '10 pm', '11 pm']
            timedEvents = Event.objects.get_all_events(user).exclude(timeStart = None)
            timedEvents = timedEvents.filter(dateOfEvent = today)
            
            eventList = []
            durationList = []
            passEvent = False

            # For each time block, associate a timeBlock with it, events, if any, and their durations
            # If no events, append a duration of -1.

            # This assumes no event overlap, so we'll have to take that into account later on.

            for index, block in enumerate(timeBlocks):
                for event in timedEvents:
                    start_time = datetime.time.strftime(event.get_timeStart(), "%H")

                    if int(start_time) == index:
                        end_time = datetime.time.strftime(event.get_timeEnd(), "%H")
                        duration = int(end_time) - int(start_time)

                        if duration < 1:
                            duration = 1
                            
                        durationList.append(duration)
                        eventList.append(event)
                        passEvent = False
                        break
                    else:
                        passEvent = True

                if passEvent or len(timedEvents) == 0:
                    durationList.append(0)
                    eventList.append("NO")
                    passEvent = False
            
            context['timedEvents'] = zip(eventList, durationList)
            context['timeBlocks'] = timeBlocks
            
            return render_to_response('planner/ajax_events_in_planner_day_view.html', context)

def loadPlannerWeekEvents(request):
    if request.method == 'POST':
        username = None

        if request.user.is_authenticated():
            username = request.user.username

            user = User.objects.get(username = username)
            
            # Process to get planner content to display
            context = {}
            context['categoriesInPlanner'] = Category.objects.get_categories_in_order(user)

            #Get startDate and endDate out of the ajax data that was passed in
            plannerViewStartDate = request.POST.get("view_start_date", "")
            plannerViewEndDate = request.POST.get("view_end_date", "")

            # Get all dates as datetime objects
            plannerViewStartDateAsDateTime = datetime.datetime.strptime(plannerViewStartDate, "%Y-%m-%d")
            secondDayInViewAsDateTime = plannerViewStartDateAsDateTime + datetime.timedelta(days = 1)
            thirdDayInViewAsDateTime = plannerViewStartDateAsDateTime + datetime.timedelta(days = 2)
            fourthDayInViewAsDateTime = plannerViewStartDateAsDateTime + datetime.timedelta(days = 3)
            fifthDayInViewAsDateTime = plannerViewStartDateAsDateTime + datetime.timedelta(days = 4)
            sixthDayInViewAsDateTime = plannerViewStartDateAsDateTime + datetime.timedelta(days = 5)
            plannerViewEndDateAsDateTime = datetime.datetime.strptime(plannerViewEndDate, "%Y-%m-%d")

            allEventsInPlanner = Event.objects.get_all_events(user)
            baseNeverEndingEventsInPlanner = allEventsInPlanner.filter(neverEnding = True)
            potentialNonBaseNeverEndingEventsInPlanner = allEventsInPlanner.filter(neverEnding = False)

            plannerViewStartDateAsDate = plannerViewStartDateAsDateTime.date()
            plannerViewEndDateAsDate = plannerViewEndDateAsDateTime.date()
            # Cleanup never ending events that aren't in current view date range then
            # Generate never ending events for current view date range
            for event in baseNeverEndingEventsInPlanner:
                tempRecurrenceReference = event.get_recurrenceReference()
                nonBaseNeverEndingEventsInPlanner = potentialNonBaseNeverEndingEventsInPlanner.filter(recurrenceReference = tempRecurrenceReference)
                for nonBaseEvent in nonBaseNeverEndingEventsInPlanner:
                    Event.objects.delete_event(user, nonBaseEvent.get_event_id())

                recurrenceType = tempRecurrenceReference.get_recurrenceType()
                originalDateOfEvent = tempRecurrenceReference.get_dateOfFirstEvent()
                if recurrenceType == 0:
                    if originalDateOfEvent >= plannerViewStartDateAsDate and originalDateOfEvent <= plannerViewEndDateAsDate:
                        originalDateOfEvent = originalDateOfEvent.strftime("%Y-%m-%d")
                        Event.objects.create_never_ending_daily_event_dynamically(user, event.get_parentCategory(), originalDateOfEvent, event.get_name(), event.get_description(), event.get_important(), event.get_timeEstimate(), event.get_timeStart(), event.get_timeEnd(), tempRecurrenceReference.get_periodOfRecurrence(), plannerViewEndDate, None, tempRecurrenceReference)
                    else:
                        gapBetweenOriginalDateAndViewStartDate = (plannerViewStartDateAsDate - originalDateOfEvent).days
                        gapBetweenOriginalDateAndViewStartDate = math.ceil(gapBetweenOriginalDateAndViewStartDate / tempRecurrenceReference.get_periodOfRecurrence())
                        firstDateEventShouldOccurInCurrentViewDate = originalDateOfEvent + timedelta(days = gapBetweenOriginalDateAndViewStartDate * tempRecurrenceReference.get_periodOfRecurrence())
                        firstDateEventShouldOccurInCurrentViewDate = firstDateEventShouldOccurInCurrentViewDate.strftime("%Y-%m-%d")
                        Event.objects.create_never_ending_daily_event_dynamically(user, event.get_parentCategory(), firstDateEventShouldOccurInCurrentViewDate, event.get_name(), event.get_description(), event.get_important(), event.get_timeEstimate(), event.get_timeStart(), event.get_timeEnd(), tempRecurrenceReference.get_periodOfRecurrence(), plannerViewEndDate, originalDateOfEvent, tempRecurrenceReference)
                elif recurrenceType == 1:
                    if originalDateOfEvent >= plannerViewStartDateAsDate and originalDateOfEvent <= plannerViewEndDateAsDate:
                        originalDateOfEvent = originalDateOfEvent.strftime("%Y-%m-%d")
                        if tempRecurrenceReference.get_listOfDaysToOccur() != None:
                            tempDayHolderArray = RecurringEventReference.objects.get_listOfDaysToOccurAsList(tempRecurrenceReference.get_listOfDaysToOccur())
                        else:
                            tempDayHolderArray = None
                        Event.objects.create_never_ending_weekly_event_dynamically(user, event.get_parentCategory(), originalDateOfEvent, event.get_name(), event.get_description(), event.get_important(), event.get_timeEstimate(), event.get_timeStart(), event.get_timeEnd(), tempRecurrenceReference.get_periodOfRecurrence(), plannerViewEndDate, tempDayHolderArray, None, tempRecurrenceReference)
                    else:
                        gapBetweenOriginalDateAndViewStartDate = math.ceil((plannerViewStartDateAsDate - originalDateOfEvent).days / 7)
                        gapBetweenOriginalDateAndViewStartDate = math.ceil(gapBetweenOriginalDateAndViewStartDate / tempRecurrenceReference.get_periodOfRecurrence())
                        firstDateEventShouldOccurInCurrentViewDate = originalDateOfEvent + timedelta(weeks = gapBetweenOriginalDateAndViewStartDate * tempRecurrenceReference.get_periodOfRecurrence())
                        if tempRecurrenceReference.get_listOfDaysToOccur() != None:
                            tempDayHolderArray = RecurringEventReference.objects.get_listOfDaysToOccurAsList(tempRecurrenceReference.get_listOfDaysToOccur())
                            while firstDateEventShouldOccurInCurrentViewDate.weekday() != 6:
                                firstDateEventShouldOccurInCurrentViewDate = firstDateEventShouldOccurInCurrentViewDate - timedelta(days = 1)
                        else:
                            tempDayHolderArray = None
                        firstDateEventShouldOccurInCurrentViewDate = firstDateEventShouldOccurInCurrentViewDate.strftime("%Y-%m-%d")
                        Event.objects.create_never_ending_weekly_event_dynamically(user, event.get_parentCategory(), firstDateEventShouldOccurInCurrentViewDate, event.get_name(), event.get_description(), event.get_important(), event.get_timeEstimate(), event.get_timeStart(), event.get_timeEnd(), tempRecurrenceReference.get_periodOfRecurrence(), plannerViewEndDate, tempDayHolderArray, originalDateOfEvent, tempRecurrenceReference)
                elif recurrenceType == 2:
                    if originalDateOfEvent >= plannerViewStartDateAsDate and originalDateOfEvent <= plannerViewEndDateAsDate:
                        originalDateOfEvent = originalDateOfEvent.strftime("%Y-%m-%d")
                        Event.objects.create_never_ending_monthly_event_dynamically(user, event.get_parentCategory(), originalDateOfEvent, event.get_name(), event.get_description(), event.get_important(), event.get_timeEstimate(), event.get_timeStart(), event.get_timeEnd(), tempRecurrenceReference.get_periodOfRecurrence(), plannerViewEndDate, tempRecurrenceReference.get_sameDayOrSameDayOfWeek(), tempRecurrenceReference.get_nthOccurrenceOfEventDate(), None, tempRecurrenceReference)
                    else:
                        originalDateOfEvent = originalDateOfEvent.strftime("%Y-%m-%d")
                        Event.objects.create_never_ending_monthly_event_dynamically(user, event.get_parentCategory(), originalDateOfEvent, event.get_name(), event.get_description(), event.get_important(), event.get_timeEstimate(), event.get_timeStart(), event.get_timeEnd(), tempRecurrenceReference.get_periodOfRecurrence(), plannerViewEndDate, tempRecurrenceReference.get_sameDayOrSameDayOfWeek(), tempRecurrenceReference.get_nthOccurrenceOfEventDate(), plannerViewStartDate, tempRecurrenceReference)
                elif recurrenceType == 3:
                    if originalDateOfEvent >= plannerViewStartDateAsDate and originalDateOfEvent <= plannerViewEndDateAsDate:
                        originalDateOfEvent = originalDateOfEvent.strftime("%Y-%m-%d")
                        Event.objects.create_never_ending_yearly_event_dynamically(user, event.get_parentCategory(), originalDateOfEvent, event.get_name(), event.get_description(), event.get_important(), event.get_timeEstimate(), event.get_timeStart(), event.get_timeEnd(), tempRecurrenceReference.get_periodOfRecurrence(), plannerViewEndDate, None, tempRecurrenceReference)
                    else:
                        originalDateOfEvent = originalDateOfEvent.strftime("%Y-%m-%d")
                        Event.objects.create_never_ending_yearly_event_dynamically(user, event.get_parentCategory(), originalDateOfEvent, event.get_name(), event.get_description(), event.get_important(), event.get_timeEstimate(), event.get_timeStart(), event.get_timeEnd(), tempRecurrenceReference.get_periodOfRecurrence(), plannerViewEndDate, plannerViewStartDate, tempRecurrenceReference)

            allEventsInPlannerWithTimeBox = Event.objects.get_all_events(user).exclude(timeStart = None).exclude(neverEnding = True)
            allEventsInPlannerWithoutTimeBox = Event.objects.get_all_events(user).filter(timeStart = None).exclude(neverEnding = True)

            context['eventsInViewStartDateWithTimeBox'] = allEventsInPlannerWithTimeBox.filter(dateOfEvent = plannerViewStartDateAsDateTime)
            context['eventsInViewSecondDateWithTimeBox'] = allEventsInPlannerWithTimeBox.filter(dateOfEvent = secondDayInViewAsDateTime)
            context['eventsInViewThirdDateWithTimeBox'] = allEventsInPlannerWithTimeBox.filter(dateOfEvent = thirdDayInViewAsDateTime)
            context['eventsInViewFourthDateWithTimeBox'] = allEventsInPlannerWithTimeBox.filter(dateOfEvent = fourthDayInViewAsDateTime)
            context['eventsInViewFifthDateWithTimeBox'] = allEventsInPlannerWithTimeBox.filter(dateOfEvent = fifthDayInViewAsDateTime)
            context['eventsInViewSixthDateWithTimeBox'] = allEventsInPlannerWithTimeBox.filter(dateOfEvent = sixthDayInViewAsDateTime)
            context['eventsInViewEndDateWithTimeBox'] = allEventsInPlannerWithTimeBox.filter(dateOfEvent = plannerViewEndDateAsDateTime)

            context['eventsInViewStartDateWithoutTimeBox'] = allEventsInPlannerWithoutTimeBox.filter(dateOfEvent = plannerViewStartDateAsDateTime)
            context['eventsInViewSecondDateWithoutTimeBox'] = allEventsInPlannerWithoutTimeBox.filter(dateOfEvent = secondDayInViewAsDateTime)
            context['eventsInViewThirdDateWithoutTimeBox'] = allEventsInPlannerWithoutTimeBox.filter(dateOfEvent = thirdDayInViewAsDateTime)
            context['eventsInViewFourthDateWithoutTimeBox'] = allEventsInPlannerWithoutTimeBox.filter(dateOfEvent = fourthDayInViewAsDateTime)
            context['eventsInViewFifthDateWithoutTimeBox'] = allEventsInPlannerWithoutTimeBox.filter(dateOfEvent = fifthDayInViewAsDateTime)
            context['eventsInViewSixthDateWithoutTimeBox'] = allEventsInPlannerWithoutTimeBox.filter(dateOfEvent = sixthDayInViewAsDateTime)
            context['eventsInViewEndDateWithoutTimeBox'] = allEventsInPlannerWithoutTimeBox.filter(dateOfEvent = plannerViewEndDateAsDateTime)

            return render_to_response('planner/ajax_events_in_planner_week_view.html', context)

def loadPlannerMonthEvents(request):
    if request.method == 'POST':
        username = None
        if request.user.is_authenticated():
            username = request.user.username

            user = User.objects.get(username = username)
            
            # Process to get planner content to display
            context = {}
            context['categoriesInPlanner'] = Category.objects.get_categories_in_order(user)

            #Get startDate and endDate out of the ajax data that was passed in
            plannerViewStartDate = request.POST.get("view_start_date", "")

            # Get all dates as datetime objects
            dateTracker = datetime.datetime.strptime(plannerViewStartDate, "%Y-%m-%d")
            allEventsInPlanner = Event.objects.get_all_events(user)

            eventsTime = []
            eventsNoTime = []
            dates = []
            classes = []

            for day in range(0, 42):
                events = allEventsInPlanner.filter(dateOfEvent = dateTracker)

                eventsWithoutTime = events.filter(timeStart = None)
                eventsWithTime = events.exclude(timeStart = None)

                eventsNoTime.append(eventsWithoutTime)
                eventsTime.append(eventsWithTime)
                dates.append(dateTracker.day)

                if day < 7 and dateTracker.day > 7 or day > 28 and dateTracker.day < 15:
                    classes.append("planner-month-outside-day")
                else:
                    classes.append("")

                dateTracker += timedelta(days = 1)

            context['information'] = zip(eventsTime, eventsNoTime, dates, classes)

            return render_to_response('planner/ajax_events_in_planner_month_view.html', context)


def loadRecentlyCompletedEvents(request):
    context = {}

    if request.method == 'GET':
        username = None
        if request.user.is_authenticated():
            username = request.user.username

        user = User.objects.get(username = username)

        # Filter events in planner to get events that are within a 3 day +/- range of today
        todaysDate = datetime.datetime.today()
        threeDaysBefore = todaysDate - datetime.timedelta(days = 3)
        threeDaysAhead = todaysDate + datetime.timedelta(days = 3)

        threeDaysBefore = threeDaysBefore.strftime("%Y-%m-%d")
        threeDaysAhead = threeDaysAhead.strftime("%Y-%m-%d")
        
        context['recentlyCompletedEvents'] = Event.objects.get_all_events(user).filter(dateOfEvent__range=[threeDaysBefore, threeDaysAhead]).filter(complete = True)

        return render_to_response('planner/ajax_recently_completed.html', context)


def loadImportantAndUpcoming(request):
    context = {}

    if request.method == 'GET':
        username = None
        if request.user.is_authenticated():
            username = request.user.username

        user = User.objects.get(username = username)

        # Get all events in planner in date order
        context['eventsInPlanner'] = Event.objects.get_all_events_in_date_order(user)

        # Get current date
        todaysDate = datetime.datetime.today()
        threeWeeksAhead = todaysDate + datetime.timedelta(days = 21)

        todaysDate = todaysDate.strftime("%Y-%m-%d")
        threeWeeksAhead = threeWeeksAhead.strftime("%Y-%m-%d")
        currentTime = datetime.datetime.now()

        context['importantAndUpcoming']  = Event.objects.get_all_events(user).filter(dateOfEvent__range=[todaysDate, threeWeeksAhead]).filter(important = True).exclude(dateOfEvent = todaysDate, timeEnd__lt = currentTime)
        
        return render_to_response('planner/ajax_important_and_upcoming.html', context)

def loadCategoryCreationModal(request):
    if request.method == 'GET':
        context = {}
        username = None
        if request.user.is_authenticated():
            username = request.user.username

        user = User.objects.get(username = username)

        context['categoriesInPlanner'] = Category.objects.get_categories_in_order(user)

        return render_to_response('planner/ajax_load_new_category_modal.html', context)

def loadEventCreationModal(request):
    if request.method == 'GET':
        context = {}

        username = None
        if request.user.is_authenticated():
            username = request.user.username

        user = User.objects.get(username = username)

        context['categoriesInPlanner'] = Category.objects.get_categories_in_order(user)

        return render_to_response('planner/ajax_load_new_event_modal.html', context)


def loadEventUpdateModal(request):
    if request.method == 'GET':
        context = {}

        username = None
        if request.user.is_authenticated():
            username = request.user.username

        user = User.objects.get(username = username)

        context['categoriesInPlanner'] = Category.objects.get_categories_in_order(user)

        return render_to_response('planner/ajax_load_update_event_modal.html', context)

    elif request.method == 'POST':
        context = {}

        desiredEventToUpdateId = request.POST.get("desiredEventToUpdateId", "")

        username = None
        if request.user.is_authenticated():
            username = request.user.username

        user = User.objects.get(username = username)

        desiredEventToUpdate = Event.objects.get_single_event_by_user_and_id(user, desiredEventToUpdateId)
        context['returnEvent'] = desiredEventToUpdate
        context['categoriesInPlanner'] = Category.objects.get_categories_in_order(user)

        return render_to_response('planner/ajax_load_update_event_modal.html', context)


def loadCategoryUpdateModal(request):
    if request.method == 'GET':
        context = {}

        username = None
        if request.user.is_authenticated():
            username = request.user.username

        user = User.objects.get(username = username)

        context['categoriesInPlanner'] = Category.objects.get_categories_in_order(user)

        return render_to_response('planner/ajax_load_update_category_modal.html', context)

    elif request.method == 'POST':
        context = {}

        desiredCategoryToUpdateId = request.POST.get("desiredCategoryToUpdateId", "")

        username = None
        if request.user.is_authenticated():
            username = request.user.username

        user = User.objects.get(username = username)

        desiredCategoryToUpdate = Category.objects.get_category_by_user_and_id(user, desiredCategoryToUpdateId)

        context['returnCategory'] = desiredCategoryToUpdate
        context['categoriesInPlanner'] = Category.objects.get_categories_in_order(user)

        return render_to_response('planner/ajax_load_update_category_modal.html', context)

def updateCategory(request):
    if request.method == 'POST':
        context = {}

        username = None
        if request.user.is_authenticated():
            username = request.user.username

        user = User.objects.get(username = username)

        updateCategoryName = request.POST.get("ajax_category_name", "")
        updateCategoryId = request.POST.get("ajax_category_id", "")
        updateCategoryColor = request.POST.get("ajax_category_color", "")
        updateCategoryOrder = request.POST.get("ajax_category_order", "")

        # Fix the category color to be updated in the data base
        if updateCategoryColor == "Red":
            updateCategoryColor = 1
        elif updateCategoryColor == "Dark Red":
            updateCategoryColor = 2
        elif updateCategoryColor == "Light Red":
            updateCategoryColor = 3
        elif updateCategoryColor == "Blue":
            updateCategoryColor = 4
        elif updateCategoryColor == "Dark Blue":
            updateCategoryColor = 5
        elif updateCategoryColor == "Light Blue":
            updateCategoryColor = 6
        elif updateCategoryColor == "Green":
            updateCategoryColor = 7
        elif updateCategoryColor == "Dark Green":
            updateCategoryColor = 8
        elif updateCategoryColor == "Light Green":
            updateCategoryColor = 9
        elif updateCategoryColor == "Yellow":
            updateCategoryColor = 10
        elif updateCategoryColor == "Gold":
            updateCategoryColor = 11
        elif updateCategoryColor == "Orange":
            updateCategoryColor = 12
        elif updateCategoryColor == "Pink":
            updateCategoryColor = 13
        elif updateCategoryColor == "Turquoise":
            updateCategoryColor = 14
        elif updateCategoryColor == "Navy":
            updateCategoryColor = 15
        else:
            pass

        # Fix order index
        updateCategoryOrder = int(updateCategoryOrder) - 1

        # Get the actual category from the database
        oldCategory = Category.objects.get_category_by_user_and_id(user, updateCategoryId)

        # Check to see what fields need to be updated

        if oldCategory.get_color() != updateCategoryColor:
            oldCategory.set_color(updateCategoryColor)

        if oldCategory.get_name() != updateCategoryName:
            Category.objects.update_category_name(user, oldCategory.get_name(), updateCategoryName)

        if oldCategory.get_order() != updateCategoryOrder:
            Category.objects.update_category_order(user, updateCategoryId, updateCategoryOrder)

    return HttpResponse('')


def deleteCategory(request):
    if request.method == 'POST':
        username = None
        if request.user.is_authenticated():
            username = request.user.username

            user = User.objects.get(username = username)

            desiredCategoryToDeleteId = request.POST.get("ajax_desired_category_to_delete", "")
            Category.objects.delete_category(user, desiredCategoryToDeleteId)

    return HttpResponse('')


def createNewCategory(request):
    if request.method == 'POST':
        username = None
        if request.user.is_authenticated():
            username = request.user.username

            user = User.objects.get(username = username)

            newCategoryName = request.POST.get("ajax_category_name", "")
            newCategoryColor = request.POST.get("ajax_category_color", "")
            newCategoryOrder = request.POST.get("ajax_category_order", "")

            # Fix the category color to be persisted to the back end
            if newCategoryColor == "Red":
                newCategoryColor = 1
            elif newCategoryColor == "Dark Red":
                newCategoryColor = 2
            elif newCategoryColor == "Light Red":
                newCategoryColor = 3
            elif newCategoryColor == "Blue":
                newCategoryColor = 4
            elif newCategoryColor == "Dark Blue":
                newCategoryColor = 5
            elif newCategoryColor == "Light Blue":
                newCategoryColor = 6
            elif newCategoryColor == "Green":
                newCategoryColor = 7
            elif newCategoryColor == "Dark Green":
                newCategoryColor = 8
            elif newCategoryColor == "Light Green":
                newCategoryColor = 9
            elif newCategoryColor == "Yellow":
                newCategoryColor = 10
            elif newCategoryColor == "Gold":
                newCategoryColor = 11
            elif newCategoryColor == "Orange":
                newCategoryColor = 12
            elif newCategoryColor == "Pink":
                newCategoryColor = 13
            elif newCategoryColor == "Turquoise":
                newCategoryColor = 14
            elif newCategoryColor == "Navy":
                newCategoryColor = 15
            else:
                pass

            # Fix the category order to be persisted to the back end
            newCategoryOrder = int(newCategoryOrder) - 1

            # Call method to create new category in DB
            Category.objects.create_category(user, newCategoryName, newCategoryColor, newCategoryOrder)

    return HttpResponse('')


def createNewEvent(request):
    if request.method == 'POST':
        username = None
        if request.user.is_authenticated():
            username = request.user.username

            user = User.objects.get(username = username)

            # Get all information from ajax call
            newEventName = request.POST.get("ajax_event_name", "")
            newEventParentCategory = request.POST.get("ajax_event_parentCategory", "")
            newEventDescription = request.POST.get("ajax_event_description", "")
            newEventDate = request.POST.get("ajax_event_date", "")
            newEventTimeEstimate = request.POST.get("ajax_event_timeEstimate", "")
            newEventStartTime = request.POST.get("ajax_event_startTime", "")
            newEventEndTime = request.POST.get("ajax_event_endTime", "")
            newEventImportant = request.POST.get("ajax_event_important", "")
            newEventRecurrenceType = request.POST.get("ajax_event_recurrence_type", "")
            newEventRecurrenceCheckboxArray = request.POST.getlist("ajax_event_recurrence_checkbox_array[]", "")
            newEventPeriodOfRecurrence = request.POST.get("ajax_event_period_of_recurrence", "")
            newEventRecurrenceEndOptions = request.POST.getlist("ajax_event_recurrence_end_options_array[]", "")
            newEventNthOccurrenceOfSelectedDate = request.POST.get("ajax_event_nth_occurrence_of_selected_date", "")

            # Fix the Event Time Estimate Field
            if newEventTimeEstimate == "" or newEventTimeEstimate == "None":
                newEventTimeEstimate = 1
            elif newEventTimeEstimate == "15 minutes":
                newEventTimeEstimate = 2
            elif newEventTimeEstimate == "30 minutes":
                newEventTimeEstimate = 3
            elif newEventTimeEstimate == "45 minutes":
                newEventTimeEstimate = 4
            elif newEventTimeEstimate == "1 hour":
                newEventTimeEstimate = 5
            elif newEventTimeEstimate == "2 hours":
                newEventTimeEstimate = 6
            elif newEventTimeEstimate == "3 hours":
                newEventTimeEstimate = 7
            elif newEventTimeEstimate == "4 hours":
                newEventTimeEstimate = 8
            elif newEventTimeEstimate == "5 hours":
                newEventTimeEstimate = 9
            elif newEventTimeEstimate == "6 hours":
                newEventTimeEstimate = 10
            elif newEventTimeEstimate == "7 hours":
                newEventTimeEstimate = 11
            elif newEventTimeEstimate == "8 hours":
                newEventTimeEstimate = 12
            elif newEventTimeEstimate == "More than 8 hours":
                newEventTimeEstimate = 13
            else:
                pass

            # Check if event is important
            if newEventImportant == "false":
                newEventImportant = False
            else:
                newEventImportant = True

            # Store necessary data if user specifies the event should reccur & call create
            if newEventRecurrenceType == "None":
                Event.objects.create_event(user, newEventParentCategory, newEventDate, newEventName, newEventDescription, newEventImportant, newEventTimeEstimate, newEventStartTime, newEventEndTime, None, False)
            else:
                # Daily Recurrence
                if newEventRecurrenceType == "0":
                    if newEventRecurrenceEndOptions[0] == "never":
                        Event.objects.create_never_ending_daily_event(user, newEventParentCategory, newEventDate, newEventName, newEventDescription, newEventImportant, newEventTimeEstimate, newEventStartTime, newEventEndTime, newEventPeriodOfRecurrence)
                    elif newEventRecurrenceEndOptions[0] == "number":
                        Event.objects.create_daily_recurring_event_given_number_to_repeat(user, newEventParentCategory, newEventDate, newEventName, newEventDescription, newEventImportant, newEventTimeEstimate, newEventStartTime, newEventEndTime, newEventPeriodOfRecurrence, newEventRecurrenceEndOptions[1])
                    else:
                        # Last statement recognizes that the end option was specified to stop on a given date
                        Event.objects.create_daily_recurring_event_given_stop_date(user, newEventParentCategory, newEventDate, newEventName, newEventDescription, newEventImportant, newEventTimeEstimate, newEventStartTime, newEventEndTime, newEventPeriodOfRecurrence, newEventRecurrenceEndOptions[1])

                # Weekly Recurrence
                elif newEventRecurrenceType == "1":
                    # The following checks build an array holding the corresponding days of the week the user specified in the modal
                    checkBoxFound = False
                    dayHolderArray = None
                    for x in newEventRecurrenceCheckboxArray:
                        if x == "1":
                            checkBoxFound = True
                    if checkBoxFound == True:
                        dayHolderArray = []
                        if newEventRecurrenceCheckboxArray[0] == "1":
                            dayHolderArray = [1,1,1,1,1,0,0]
                        elif newEventRecurrenceCheckboxArray[1] == "1":
                            dayHolderArray = [1,0,1,0,1,0,0]
                        elif newEventRecurrenceCheckboxArray[2] == "1":
                            dayHolderArray = [0,1,0,1,0,0,0]
                        else:
                            for i in range(4,10):
                                dayHolderArray.append(int(newEventRecurrenceCheckboxArray[i]))
                            dayHolderArray.append(int(newEventRecurrenceCheckboxArray[3]))
                    if newEventRecurrenceEndOptions[0] == "never":
                        Event.objects.create_never_ending_weekly_event(user, newEventParentCategory, newEventDate, newEventName, newEventDescription, newEventImportant, newEventTimeEstimate, newEventStartTime, newEventEndTime, newEventPeriodOfRecurrence, dayHolderArray)
                    elif newEventRecurrenceEndOptions[0] == "number":
                        Event.objects.create_weekly_recurring_event_given_number_to_repeat(user, newEventParentCategory, newEventDate, newEventName, newEventDescription, newEventImportant, newEventTimeEstimate, newEventStartTime, newEventEndTime, newEventPeriodOfRecurrence, newEventRecurrenceEndOptions[1], dayHolderArray)
                    else:
                        # Last statement recognizes that the end option was specified to stop on a given date
                        Event.objects.create_weekly_recurring_event_given_stop_date(user, newEventParentCategory, newEventDate, newEventName, newEventDescription, newEventImportant, newEventTimeEstimate, newEventStartTime, newEventEndTime, newEventPeriodOfRecurrence, newEventRecurrenceEndOptions[1], dayHolderArray)

                # Monthly Recurrence
                elif newEventRecurrenceType == "2":
                    # Default way that recurring monthly events are to be created
                    sameDayNextMonth = True
                    checkBoxFound = False
                    for x in newEventRecurrenceCheckboxArray:
                        if x == "1":
                            checkBoxFound = True
                    if checkBoxFound == True:
                        if newEventRecurrenceCheckboxArray[10] == "1":
                            pass
                        else:
                            sameDayNextMonth = False
                    if newEventRecurrenceEndOptions[0] == "never":
                        Event.objects.create_never_ending_monthly_event(user, newEventParentCategory, newEventDate, newEventName, newEventDescription, newEventImportant, newEventTimeEstimate, newEventStartTime, newEventEndTime, newEventPeriodOfRecurrence, sameDayNextMonth, newEventNthOccurrenceOfSelectedDate)
                    elif newEventRecurrenceEndOptions[0] == "number":
                        Event.objects.create_monthly_recurring_event_given_number_to_repeat(user, newEventParentCategory, newEventDate, newEventName, newEventDescription, newEventImportant, newEventTimeEstimate, newEventStartTime, newEventEndTime, newEventPeriodOfRecurrence, newEventRecurrenceEndOptions[1], sameDayNextMonth, newEventNthOccurrenceOfSelectedDate)
                    else:
                        # Last statement recognizes that the end option was specified to stop on a given date
                        Event.objects.create_monthly_recurring_event_given_stop_date(user, newEventParentCategory, newEventDate, newEventName, newEventDescription, newEventImportant, newEventTimeEstimate, newEventStartTime, newEventEndTime, newEventPeriodOfRecurrence, newEventRecurrenceEndOptions[1], sameDayNextMonth, newEventNthOccurrenceOfSelectedDate)
                
                # Yearly Recurrence
                elif newEventRecurrenceType == "3":
                    if newEventRecurrenceEndOptions[0] == "never":
                        Event.objects.create_never_ending_yearly_event(user, newEventParentCategory, newEventDate, newEventName, newEventDescription, newEventImportant, newEventTimeEstimate, newEventStartTime, newEventEndTime, newEventPeriodOfRecurrence)
                    elif newEventRecurrenceEndOptions[0] == "number":
                        Event.objects.create_yearly_recurring_event_given_number_to_repeat(user, newEventParentCategory, newEventDate, newEventName, newEventDescription, newEventImportant, newEventTimeEstimate, newEventStartTime, newEventEndTime, newEventPeriodOfRecurrence, newEventRecurrenceEndOptions[1])
                    else:
                        # Last statement recognizes that the end option was specified to stop on a given date
                        Event.objects.create_yearly_recurring_event_given_stop_date(user, newEventParentCategory, newEventDate, newEventName, newEventDescription, newEventImportant, newEventTimeEstimate, newEventStartTime, newEventEndTime, newEventPeriodOfRecurrence, newEventRecurrenceEndOptions[1])

                else:
                    pass

    return HttpResponse('')


def updateEvent(request):
    if request.method == 'POST':
        username = None
        if request.user.is_authenticated():
            username = request.user.username

            user = User.objects.get(username = username)

            updateEventName = request.POST.get("ajax_event_name", "")
            updateEventId = request.POST.get("ajax_event_id", "")
            updateEventParentCategory = request.POST.get("ajax_event_parentCategory", "")
            updateEventDescription = request.POST.get("ajax_event_description", "")
            updateEventDate = request.POST.get("ajax_event_date", "")
            updateEventTimeEstimate = request.POST.get("ajax_event_timeEstimate", "")
            updateEventStartTime = request.POST.get("ajax_event_startTime", "")
            updateEventEndTime = request.POST.get("ajax_event_endTime", "")
            updateEventImportant = request.POST.get("ajax_event_important", "")
            updateEventComplete = request.POST.get("ajax_event_complete", "")

            # Get Existing Event as it is currently stored in database
            oldEvent = Event.objects.get_single_event_by_user_and_id(user, updateEventId)

            # Fix the important and complete values
            if updateEventImportant == "false":
                updateEventImportant = False
            else:
                updateEventImportant = True

            if updateEventComplete == "false":
                updateEventComplete = False
            else: 
                updateEventComplete = True

            # Fix the Event Time Estimate Field
            if updateEventTimeEstimate == "" or updateEventTimeEstimate == "None" or updateEventTimeEstimate == "--":
                updateEventTimeEstimate = 1
            elif updateEventTimeEstimate == "15 minutes":
                updateEventTimeEstimate = 2
            elif updateEventTimeEstimate == "30 minutes":
                updateEventTimeEstimate = 3
            elif updateEventTimeEstimate == "45 minutes":
                updateEventTimeEstimate = 4
            elif updateEventTimeEstimate == "1 hour":
                updateEventTimeEstimate = 5
            elif updateEventTimeEstimate == "2 hours":
                updateEventTimeEstimate = 6
            elif updateEventTimeEstimate == "3 hours":
                updateEventTimeEstimate = 7
            elif updateEventTimeEstimate == "4 hours":
                updateEventTimeEstimate = 8
            elif updateEventTimeEstimate == "5 hours":
                updateEventTimeEstimate = 9
            elif updateEventTimeEstimate == "6 hours":
                updateEventTimeEstimate = 10
            elif updateEventTimeEstimate == "7 hours":
                updateEventTimeEstimate = 11
            elif updateEventTimeEstimate == "8 hours":
                updateEventTimeEstimate = 12
            elif updateEventTimeEstimate == "More than 8 hours":
                updateEventTimeEstimate = 13
            else:
                pass

            # Begin Comparison to see what fields need to be updated

            # fix this to disallow duplicate names
            if oldEvent.get_name() != updateEventName:
                oldEvent.set_name(updateEventName)

            if oldEvent.get_parentCategory().get_name() != updateEventParentCategory:
                newParentCategory = Category.objects.get_category_by_name(user, updateEventParentCategory)
                oldEvent.set_parentCategory(newParentCategory)

            if oldEvent.get_description() != updateEventDescription:
                oldEvent.set_description(updateEventDescription)

            if oldEvent.get_timeEstimate() != updateEventTimeEstimate:
                oldEvent.set_timeEstimate(updateEventTimeEstimate)
            
            if oldEvent.get_timeStart() != updateEventStartTime:
                if updateEventStartTime != "":
                    oldEvent.set_timeStart(updateEventStartTime)
                elif updateEventStartTime == "":
                    oldEvent.set_timeStart(None)

            if oldEvent.get_timeEnd() != updateEventEndTime:
                if updateEventEndTime != "":
                    oldEvent.set_timeEnd(updateEventEndTime)
                elif updateEventEndTime == "":
                    oldEvent.set_timeEnd(None)

            if oldEvent.get_important() != updateEventImportant:
                oldEvent.set_important(updateEventImportant)

            if oldEvent.get_complete() != updateEventComplete:
                oldEvent.set_complete(updateEventComplete)

            if oldEvent.get_dateOfEvent_forHTML() != updateEventDate:
                oldEvent.set_dateOfEvent(updateEventDate)

    return HttpResponse('')


def deleteEvent(request):
    if request.method == 'POST':
        username = None
        if request.user.is_authenticated():
            username = request.user.username

            user = User.objects.get(username = username)

            desiredEventToDeleteId = request.POST.get("ajax_desired_event_to_delete", "")
            Event.objects.delete_event(user, desiredEventToDeleteId)

    return HttpResponse('')


def loadPlannerNotes(request):
    if request.method == 'GET':
        context = {}

        username = None
        if request.user.is_authenticated():
            username = request.user.username

            user = User.objects.get(username = username)

            context['planner'] = user.planner

        return render_to_response('planner/ajax_load_misc_notes.html', context)

    if request.method == 'POST':
        context = {}

        username = None
        if request.user.is_authenticated():
            username = request.user.username

            user = User.objects.get(username = username)

            context['planner'] = user.planner

        return render_to_response('planner/ajax_load_misc_notes_modal.html', context)


def updatePlannerNotes(request):
    if request.method == 'POST':
        context = {}

        username = None
        if request.user.is_authenticated():
            username = request.user.username

            user = User.objects.get(username = username)

            newPlannerNotes = request.POST.get("ajax_planner_notes", "")

            user.planner.set_miscellaneousNotes(newPlannerNotes)

    return HttpResponse('')
