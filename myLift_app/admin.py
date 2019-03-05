from django.contrib import admin

from .models import Ride, ShareRide, Driver

admin.site.register([Ride, ShareRide, Driver])
