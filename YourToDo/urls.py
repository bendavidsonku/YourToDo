from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth.views import logout_then_login

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

admin.autodiscover()

# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

urlpatterns = i18n_patterns("",
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    ("^admin/", include(admin.site.urls)),
)

if settings.USE_MODELTRANSLATION:
    urlpatterns += patterns('',
        url('^i18n/$', 'django.views.i18n.set_language', name='set_language'),
    )

urlpatterns += patterns('',
    # We don't want to presume how your homepage works, so here are a
    # few patterns you can use to set it up.

    url(r"^$", direct_to_template, {"template": "base.html"}, name="home"),

    # Static Pages
    url(r'^about/$',    'YourToDo.views.about'),
    url(r'^contact/$',    'YourToDo.views.contact'),

    # User Authentication Urls
    url(r'^login/$',    'YourToDo.views.login'),
    url(r'^logout/$',   lambda request: logout_then_login(request, "/"), name='logout'),

    # User Registration Urls
    url(r'^registration/$', 'YourToDo.views.registration'),
    url(r'^registration_success/$', 'YourToDo.views.registration_success'),
    
    ("^", include("mezzanine.urls")),
)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
