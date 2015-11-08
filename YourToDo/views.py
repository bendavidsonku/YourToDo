from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.template import RequestContext

from YourToDo.forms import defaultUserRegistrationForm

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
    return render_to_response('auth/loggedin.html', 
        {
            'user': request.user
        })

def invalid_login(request):
    return render_to_response('auth/invalid.html')

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