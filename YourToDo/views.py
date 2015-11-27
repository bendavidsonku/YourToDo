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
        context['categoriesInPlanner'] = Category.objects.get_categories_in_order(user)
        context['eventsInPlanner'] = Event.objects.get_all_events(user)
        
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
            if newEventTimeEstimate == "":
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

            # Check to see if user assigned timeStart AND timeEnd to event
            if newEventStartTime == "" or newEventEndTime == "":
                Event.objects.create_event_no_timeBox(user, newEventParentCategory, newEventDate, newEventName, newEventDescription, newEventImportant, newEventTimeEstimate)
            else:
                # else user has given time frame for event so create with timeBox
                Event.objects.create_event_with_timeBox(user, newEventParentCategory, newEventDate, newEventName, newEventDescription, newEventImportant, newEventTimeEstimate, newEventStartTime, newEventEndTime)

    return HttpResponse('')
