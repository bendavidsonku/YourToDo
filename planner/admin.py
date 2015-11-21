from django.contrib import admin

from planner.models import Planner, Event, Category

admin.site.register(Planner)
admin.site.register(Event)
admin.site.register(Category)
