import datetime
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.core.context_processors import csrf
from django.template import RequestContext
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse

from YourToDo.forms import ContactForm
from planner.models import Planner, Category, Event

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
	return render_to_response('base.html')

# TODO
# Update this view to include all supported layouts (day, week, and month)
# We're either going to need to send a different html layout here, or something.
#
# At this point, I'm just making one layout to get started.

#LOGIN REQUIRED?????
def PlannerView(request):
    plannerLayoutSelection = request.POST.get("planner_layout", "")
    context = {}

    if plannerLayoutSelection == "Day":
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

            context['eventsInViewStartDate'] = allEventsInPlanner.filter(dateOfEvent = plannerViewStartDateAsDateTime)
            context['eventsInViewSecondDate'] = allEventsInPlanner.filter(dateOfEvent = secondDayInViewAsDateTime)
            context['eventsInViewThirdDate'] = allEventsInPlanner.filter(dateOfEvent = thirdDayInViewAsDateTime)
            context['eventsInViewFourthDate'] = allEventsInPlanner.filter(dateOfEvent = fourthDayInViewAsDateTime)
            context['eventsInViewFifthDate'] = allEventsInPlanner.filter(dateOfEvent = fifthDayInViewAsDateTime)
            context['eventsInViewSixthDate'] = allEventsInPlanner.filter(dateOfEvent = sixthDayInViewAsDateTime)
            context['eventsInViewEndDate'] = allEventsInPlanner.filter(dateOfEvent = plannerViewEndDateAsDateTime)

            return render_to_response('planner/ajax_events_in_planner_week_view.html', context)

def loadImportantAndUpcoming(request):
    context = {}

    if request.method == 'GET':
        username = None
        if request.user.is_authenticated():
            username = request.user.username

        user = User.objects.get(username = username)

        # Get all events in planner
        context['eventsInPlanner'] = Event.objects.get_all_events(user)

        # Get current date
        todaysDate = datetime.datetime.today()
        threeWeeksAhead = todaysDate + datetime.timedelta(days = 21)

        todaysDate = todaysDate.strftime("%Y-%m-%d")
        threeWeeksAhead = threeWeeksAhead.strftime("%Y-%m-%d")

        todaysDate = datetime.datetime.strptime(todaysDate, "%Y-%m-%d")
        threeWeeksAhead = datetime.datetime.strptime(threeWeeksAhead, "%Y-%m-%d")

        importantAndUpcomingList = []

        for event in context['eventsInPlanner']:
            if event.get_important() == True:
                tempDate = event.get_dateOfEvent().strftime("%Y-%m-%d")
                tempDate = datetime.datetime.strptime(tempDate, "%Y-%m-%d")
                if tempDate >= todaysDate and tempDate <= threeWeeksAhead:
                    importantAndUpcomingList.append(event)
                else:
                    pass

        context['importantAndUpcoming'] = importantAndUpcomingList

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

            newEventName = request.POST.get("ajax_event_name", "")
            newEventParentCategory = request.POST.get("ajax_event_parentCategory", "")
            newEventDescription = request.POST.get("ajax_event_description", "")
            newEventDate = request.POST.get("ajax_event_date", "")
            newEventTimeEstimate = request.POST.get("ajax_event_timeEstimate", "")
            newEventStartTime = request.POST.get("ajax_event_startTime", "")
            newEventEndTime = request.POST.get("ajax_event_endTime", "")
            newEventImportant = request.POST.get("ajax_event_important", "")

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

            if newEventImportant == "false":
                newEventImportant = False
            else:
                newEventImportant = True

            # Check to see if user assigned timeStart AND timeEnd to event
            if newEventStartTime == "" or newEventEndTime == "":
                Event.objects.create_event_no_timeBox(user, newEventParentCategory, newEventDate, newEventName, newEventDescription, newEventImportant, newEventTimeEstimate)
            else:
                # else user has given time frame for event so create with timeBox
                Event.objects.create_event_with_timeBox(user, newEventParentCategory, newEventDate, newEventName, newEventDescription, newEventImportant, newEventTimeEstimate, newEventStartTime, newEventEndTime)

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

            if oldEvent.get_timeEnd() != updateEventEndTime:
                if updateEventEndTime != "":
                    oldEvent.set_timeEnd(updateEventEndTime)

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