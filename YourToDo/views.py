from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext

# Static Page Views
def about(request):
    return render_to_response('static/about.html', context_instance = RequestContext(request))

def contact(request):
    return render_to_response('static/contact.html', context_instance = RequestContext(request))

# Authentication Views
def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('auth/login.html', c)

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username = username, password = password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/loggedin')
    else:
        return HttpResponseRedirect('/invalid')

def loggedin(request):
    return render_to_response('auth/loggedin.html', context_instance = RequestContext(request))

def invalid_login(request):
    return render_to_response('auth/invalid.html')

def logout(request):
    auth.logout(request)
    return render_to_response('auth/logout.html')

def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/registration_success/')

    args = {}
    args.update(csrf(request))

    args['form'] = UserCreationForm()

    return render_to_response('auth/registration.html', args)

def registration_success(reqest):
        return render_to_response('auth/registration_success.html')
