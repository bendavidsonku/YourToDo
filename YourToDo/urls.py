from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth.views import logout_then_login

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

from YourToDo.views import logout

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
    url(r'^about/$',            'YourToDo.views.about'),
    url(r'^contact/$',          'YourToDo.views.contact'),
    url(r'^contact_success/$',  'YourToDo.views.contact_success'),
    
    # Accounts Urls
    url(r'^accounts/logout/',   'YourToDo.views.logout', name='auth_logout'),
    url(r'^accounts/',          include('registration.backends.default.urls')),

    # Application Urls
    url(r'^planner/', 'YourToDo.views.PlannerView', name = "planner_view"),
    url(r'^load-day-events/', 'YourToDo.views.loadPlannerDayEvents', name="planner_load_day_events"),
    url(r'^load-week-events/', 'YourToDo.views.loadPlannerWeekEvents', name="planner_load_week_events"),
    url(r'^load-month-events/', 'YourToDo.views.loadPlannerMonthEvents', name="planner_load_month_events"),
    url(r'^create-category/', 'YourToDo.views.createNewCategory', name ="create_category"),
    url(r'^update-category/', 'YourToDo.views.updateCategory', name="update_category"),
    url(r'^delete-category/', 'YourToDo.views.deleteCategory', name="delete_category"),
    url(r'^create-event/', 'YourToDo.views.createNewEvent', name="create_event"),
    url(r'^update-event/', 'YourToDo.views.updateEvent', name="update_event"),
    url(r'^delete-event/', 'YourToDo.views.deleteEvent', name="delete_event"),
    url(r'^load-planner-notes/', 'YourToDo.views.loadPlannerNotes', name="load-planner-notes"),
    url(r'^load-important-and-upcoming/', 'YourToDo.views.loadImportantAndUpcoming', name="load-important-and-upcoming"),
    url(r'^update-planner-notes/', 'YourToDo.views.updatePlannerNotes', name="update-planner-notes"),
    url(r'^load-category-creation-modal/', 'YourToDo.views.loadCategoryCreationModal', name="load-category-creation-modal"),
    url(r'^load-event-creation-modal/', 'YourToDo.views.loadEventCreationModal', name='load-event-creation-modal'),
    url(r'^load-event-update-modal/', 'YourToDo.views.loadEventUpdateModal', name="load-event-update-modal"),
    url(r'^load-category-update-modal/', 'YourToDo.views.loadCategoryUpdateModal', name="load-category-update-modal"),
    # Include All Mezzanine Urls
    ("^", include("mezzanine.urls")),
)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
