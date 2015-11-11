from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.core.context_processors import csrf
from django.template import RequestContext
from django.core.mail import send_mail

from YourToDo.forms import defaultUserRegistrationForm
from YourToDo.forms import defaultAuthenticationForm
from YourToDo.forms import ContactForm

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

# Authentication Views
def login(request):
    args = {}
    args.update(csrf(request))

    if request.method == 'POST':
        form = defaultAuthenticationForm(data = request.POST)
        args['form'] = form
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username = username, password = password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('home'))
    else:
        args['form'] = defaultAuthenticationForm()

    return render_to_response('auth/login.html', args, context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    return render_to_response('auth/logout.html')

def registration(request):
    args = {}
    args.update(csrf(request))

    if request.method == 'POST':
        form = defaultUserRegistrationForm(request.POST)
        args['form'] = form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/registration_success/')
    else:
        args['form'] = defaultUserRegistrationForm()

    return render_to_response('auth/registration.html', args, context_instance=RequestContext(request))

def registration_success(reqest):
        return render_to_response('auth/registration_success.html')
