from django.contrib import admin

from planner.models import Planner, Category, Event, RecurringEventReference

admin.site.register(Planner)
admin.site.register(Event)
admin.site.register(Category)
admin.site.register(RecurringEventReference)
