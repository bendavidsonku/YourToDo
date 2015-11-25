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
    print(plannerLayoutSelection)

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
        return render_to_response('planner/planner_month_view.html', context, context_instance = RequestContext(request))

    else:
        pass

    return render_to_response('planner/planner_base.html', context, context_instance = RequestContext(request))


def loadPlannerEvents(request):
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


def createNewCategory(request):
    return

