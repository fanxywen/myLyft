# accounts/urls.py
from django.urls import path
from django.views.generic.base import TemplateView # new

from . import views


urlpatterns = [
    path('success', TemplateView.as_view(template_name='myLift_app/success.html'), name='success'),
    path('showYourRides', views.showYourRides, name='showYourRides'),
    path('rideformpage', views.ride_form_name_view, name='rideFormPage'),
    path('shareRide', views.shareRide, name='shareRide'),
    path('driverPage', views.driverPage, name='driverPage'),
    path('driverRegister', views.driverRegister, name='driverRegister'),
    path('driverEdit', views.driverEdit, name='driverEdit'),
    path('changeprofile', views.profile_change, name = 'changeprofile'),
    path('driverRideSearch', views.driverRideSearch, name='driverRideSearch'),
    path('showConfirmedOngoingRides', views.showConfirmedOngoingRides, name='showConfirmedOngoingRides'),
    path('showConfirmedRides', views.showConfirmedRides, name='showConfirmedRides'),
    path('driverSearchAll', views.driverSearchAll, name='driverSearchAll'),
    path('driverCustomSearch', views.driverCustomSearch, name='driverCustomSearch'),
    path('<int:ride_id>confirmRides', views.confirmRides, name='confirmRides'),
    path('<int:ride_id>completeRides', views.completeRides, name='completeRides'),
    path('<int:ride_id>/editRides', views.editRides, name='editRides'),
    path('<int:shareride_id>/editShareRides', views.editShareRides, name='editShareRides'),
    path('<int:shareride_id>/addShareRides', views.addShareRides, name='addShareRides'),
]
