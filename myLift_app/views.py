from django.shortcuts import render
# from . import forms
# from django.db import models
# from myLift_app.models import *
from . import models
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib import messages
from django.core import serializers
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
# Create your views here.
def editRides(request, ride_id):
    ride = models.Ride.objects.filter(id=ride_id)[0]
    rideform = models.RideForm(instance=ride)

    if 'delete' in request.POST:
        print('delete')
        ride.delete()
        return showYourRides(request)

    print(request.POST)
    if 'dest' in request.POST:
        print('hi')
        rideform = models.RideForm(request.POST, request.FILES)
        if rideform.is_valid():
            ride.dest = rideform.cleaned_data['dest']
            ride.datetime = rideform.cleaned_data['datetime']
            ride.num_passenger = rideform.cleaned_data['num_passenger']
            ride.shareOrNot = rideform.cleaned_data['shareOrNot']
            ride.save()
        else:
            print("not valid")
            print(rideform)
            messages.success(request, 'edit fails')
            return render(request, 'myLift_app/editRide.html', {'form': rideform})

        request.method="GET"
        return showYourRides(request)

    return render(request, 'myLift_app/editRide.html', {'form': rideform})

def editShareRides(request, shareride_id):
    shareride = models.ShareRide.objects.filter(id=shareride_id)[0]
    sharerideform = models.ShareRideForm(instance=shareride)

    if request.method=='POST':
        sharerideform = models.ShareRideForm(request.POST, request.FILES)
        if sharerideform.is_valid():
            shareride.num_pass = sharerideform.cleaned_data['num_pass']
            shareride.save()
        else:
            print("not valid")
            print(sharerideform)
            messages.success(request, 'edit fails')
            return render(request, 'myLift_app/editShareRide.html', {'form': sharerideform})
        # return render(request, 'myLift_app/succ.html')
        request.method="GET"
        return showYourRides(request)
    return render(request, 'myLift_app/editShareRide.html', {'form': sharerideform})

def addShareRides(request, shareride_id):
    shareride = models.ShareRide.objects.filter(id=shareride_id)[0]
    ride = models.Ride.objects.filter(id=request.POST['ride'])[0]

    shareride.ride = ride
    shareride.save()

    return render(request, 'accounts/home.html')


def showYourRides(request):
    curr_user_rides = models.Ride.objects.filter(creater=request.user)
    curr_user_sharerides = models.ShareRide.objects.filter(sharer=request.user).exclude(ride__isnull=True)
    for ride in curr_user_rides:
        if ride.shareOrNot:
            sharerides = models.ShareRide.objects.filter(ride=ride)
            ride.num_sharers = 0
            for shareride in sharerides:
                ride.num_sharers += shareride.num_pass
            ride.num_total = ride.num_passenger + ride.num_sharers
            ride.save()
    # if request.POST:
    #     ride = models.Ride(request.POST)
    #     request.method = 'GET'
        # return editRides(request, ride)
        # # print(rideform)
        # if rideform.is_valid():
        #     rideform.savemodel(request=request)
        #     return render(request, 'myLift_app/showYourRides.html', {'rideforms': rideforms})
        # else:
        #     print("forms.errors")
        #     return render(request, 'myLift_app/showYourRides.html', {'rideforms': rideforms, 'rideform': rideform})



    return render(request, 'myLift_app/showYourRides.html', {'rides': curr_user_rides, 'sharerides': curr_user_sharerides})


def ride_form_name_view(request):
    rideform = models.RideForm()

    if request.POST:
        rideform = models.RideForm(request.POST, request.FILES)
        if rideform.is_valid():
            print(rideform)
            model_instance = rideform.save(commit=False)
            model_instance.creater = request.user
            messages.success(request, 'Ride created successfully')
            try:
                model_instance.save()
            except Exception as e:
                messages.error(request, 'Not save successfully')
                return render(request, 'myLift_app/createRide.html', {'form': rideform})

            return render(request, 'myLift_app/createRide.html', {'form': rideform})

        else:
            messages.error(request, 'The ride form is invalid!')
            return render(request, 'myLift_app/createRide.html', {'form': rideform})

    return render(request, 'myLift_app/createRide.html', {'form': rideform})


# def shareRide(request):
#     shareform = models.ShareRideForm()
#
#     if request.POST:
#         shareform = models.ShareRideForm(request.POST, request.FILES)
#         if shareform.is_valid():
#             model_instance = shareform.save(commit=False)
#             model_instance.sharer = request.user
#             target_rides = models.Ride.objects.filter(
#                 dest=model_instance.dest,
#                 datetime__contains=model_instance.datetime.date(),
#                 ).exclude(creater=request.user)
#             try:
#                 model_instance.save()
#             except Exception as e:
#                 print(e)
#                 messages.error(request, 'Not save successfully')
#                 return render(request, 'myLift_app/shareRide.html', {'form': shareform})
#             print(model_instance.datetime.date())
#             return render(request, "myLift_app/showShareRides.html", {"shareride" : model_instance, "rides" : target_rides})
#         else:
#             messages.error(request, 'The share form is invalid!')
#             return render(request, 'myLift_app/shareRide.html', {'form': shareform})
#
#     return render(request, 'myLift_app/shareRide.html', {'form': shareform})

def shareRide(request):
    shareform = models.ShareRideForm()

    if request.POST:
        shareform = models.ShareRideForm(request.POST, request.FILES)
        if shareform.is_valid():
            model_instance = shareform.save(commit=False)
            model_instance.sharer = request.user
            target_rides = models.Ride.objects.filter(
                dest=model_instance.dest,
                datetime__contains=model_instance.datetime.date(),
                ).exclude(creater=request.user)
            try:
                model_instance.save()
            except Exception as e:
                print(e)
                messages.error(request, 'Not save successfully')
                return render(request, 'myLift_app/shareRide.html', {'form': shareform})
            print(model_instance.datetime.date())
            return render(request, "myLift_app/showShareRides.html", {"shareride" : model_instance, "rides" : target_rides})
        else:
            messages.error(request, 'The share form is invalid!')
            return render(request, 'myLift_app/shareRide.html', {'form': shareform})

    return render(request, 'myLift_app/shareRide.html', {'form': shareform})

def driverPage(request):
    driver = models.Driver.objects.filter(driver=request.user)
    return render(request, 'myLift_app/driverhomepage.html', {'driver': driver});

def driverRegister(request):
    driverform = models.DriverForm()
    if request.POST:
        driverform = models.DriverForm(request.POST)
        if driverform.is_valid():
            model_instance = driverform.save(commit=False)
            model_instance.driver = request.user
            try:
                model_instance.save()
                messages.success(request, 'Success! You registered as a driver')
            except Exception as e:
                messages.error(request, 'You have already register a car')
                return render(request, 'myLift_app/driverRegister.html', {'form': driverform})
        else:
            messages.error(request, 'Your driver form is not valid, not saving successfully')
            render(request, 'myLift_app/driverRegister.html', {'form': driverform})

        return render(request, 'myLift_app/driverRegister.html', {'form': driverform})

    return render(request, 'myLift_app/driverRegister.html', {'form': driverform})

def driverEdit(request):
    driver = models.Driver.objects.filter(driver=request.user)[0]
    driverform = models.DriverForm(instance=driver)

    if 'delete' in request.POST:
        print('delete')
        driver.delete()
        return driverPage(request)

    if 'licence' in request.POST:
        driverform = models.DriverForm(request.POST, request.FILES)
        if driverform.is_valid():
            driver.vehicle_type = driverform.cleaned_data['vehicle_type']
            driver.licence = driverform.cleaned_data['licence']
            driver.capacity = driverform.cleaned_data['capacity']
            driver.save()
            return driverPage(request)
        else:
            print("not valid")
            messages.error(request, 'edit fails')
            return render(request, 'myLift_app/driverEdit.html', {'form': driverform})

    return render(request, 'myLift_app/driverEdit.html', {'form': driverform})

#@login_required
def profile_change(request):
    user = models.User.objects.get(username=request.user)
    userForm = models.PasswordChange(instance=user)
    if 'edit' in request.POST:
        userForm = models.PasswordChange(request.POST, instance = request.user)
        if userForm.is_valid():
            # user.username = userForm.cleaned_data['username']
            # user.email = userForm.cleaned_data['email']
            # user.password1 = userForm.cleaned_data['password1']
            # user.password2 = userForm.cleaned_data['password2']

            user = userForm.save()
            #update_session_auth_hash(request, user)
            return render(request, 'accounts/home.html')
        else:
            messages.error(request, 'change password fails')
            return render(request, 'myLift_app/changeprofile.html', {'form':userForm})

    return render(request, 'myLift_app/changeprofile.html', {'form': userForm})


##############################################################################

# def driverEditForm(request, ride_id):
#     driver=models.Driver.objects.filter(driver=request.user)[0]
#     incompletride = models.Rides.objects.filter(id=ride_id)[0]
#     driverEdit = models.driverEditableForm(instance=incompleteride)
#     if method=='POST':
#         driverEdit = models.driverEditableForm(request.POST, request.FILES)
#         if driverEdit.is_valid():
#             incompletride.completeOrNot=driverEdit.cleaned_data['completeOrNot']
#             incompletride.save()
#         else:
#             print("not valid")
#             print(driverEdit)
#             messages.error(request, 'edit fails')
#             return render(request, 'myLift_app/driverEditForms.html', {'form': driverEdit})
#         # return render(request, 'myLift_app/succ.html')
#         request.method="GET"
#         return showConfrimedOngoingRides(request)


###############################################################################
def driverRideSearch(request):
    try:
        driver = models.Driver.objects.filter(driver=request.user)[0]
    except Exception as e:
        messages.error(request, "You did not registered as a driver!")
        return render(request, 'myLift_app/driverRideSearch.html')
    return render(request, 'myLift_app/driverRideSearch.html')

def driverSearchAll(request):
    driver = models.Driver.objects.filter(driver=request.user)[0]

    # update ride information on sharers
    rides = models.Ride.objects.all()
    for ride in rides:
        if ride.shareOrNot:
            sharerides = models.ShareRide.objects.filter(ride=ride)
            for shareride in sharerides:
                ride.num_sharers += shareride.num_pass
        ride.num_total = ride.num_passenger + ride.num_sharers
        ride.save()

    target_rides = models.Ride.objects.filter(num_total__lte=driver.capacity, confirmedOrNot=False).exclude(creater=request.user)


    return render(request, 'myLift_app/showDriverRides.html',{'rides': target_rides})

def driverCustomSearch(request):
    driversearchform = models.DriverSearchForm()

    if request.POST:
        driver = models.Driver.objects.filter(driver=request.user)[0]
        # update ride information on sharers
        rides = models.Ride.objects.filter()
        for ride in rides:
            if ride.shareOrNot:
                sharerides = models.ShareRide.objects.filter(ride=ride)
                for shareride in sharerides:
                    ride.num_sharers += shareride.num_pass
            ride.num_total = ride.num_passenger + ride.num_sharers
            ride.save()
        driversearchform = models.DriverSearchForm(request.POST, request.FILES)
        if driversearchform.is_valid():
            model_instance = driversearchform.save(commit=False)
            target_rides = models.Ride.objects.filter(
                dest=model_instance.dest,
                datetime__contains=model_instance.datetime.date(),
                confirmedOrNot=False,
                completeOrNot=False,
                num_total__lte=driver.capacity
                ).exclude(creater=request.user)
            return render(request, 'myLift_app/showDriverRides.html', {'rides': target_rides})
        else:
            messages.error(request, 'The share form is invalid!')
            return render(request, 'myLift_app/driverSearchForm.html', {'form': driversearchform})

    return render(request, 'myLift_app/driverSearchForm.html', {'form': driversearchform})

def confirmRides(request, ride_id):
    driver = models.Driver.objects.filter(driver=request.user)[0]
    ride = models.Ride.objects.filter(id=ride_id)[0]
    #shareride = models.ShareRide.objects.filter(ride=ride)
    if 'confirmed' in request.POST:
        ride.driver = request.user
        ride.vehicle = driver.vehicle_type
        ride.capacity = driver.capacity
        ride.licence = driver.licence
        ride.confirmedOrNot = True
        ride.save()
        sharerides = models.ShareRide.objects.filter(ride=ride)
        print(sharerides)
        for shareride in sharerides:
            if shareride is not None:
                shareride.driver = request.user
                shareride.vehicle = driver.vehicle_type
                shareride.capacity = driver.capacity
                shareride.licence = driver.licence
                shareride.confirmedOrNot = True
                shareride.save()
                shareuser = shareride.sharer
                useremail = shareuser.email
                send_mail('Ride Confirmation', 'Your ride has been confirmed by a driver!', 'mylyft568@gmail.com', [useremail], fail_silently=False)
            # user = shareride.get('sharer')
            # useremail = user.email
            # send_mail('Ride Confirmation', 'Your ride has been confirmed by a driver!', 'mylyft568@gmail.com', [useremail], fail_silently=False)
        #except Exception as e:
        # user = ride.creater
        # useremail = user.email
        # send_mail('Ride Confirmation', 'Your ride has been confirmed by a driver!', 'mylyft568@gmail.com', [useremail], fail_silently=False)
        # return render(request, 'myLift_app/driverRideSearch.html')
        # if shareride is not None:
        #     for ride in shareride:
        #         ride.driver = request.user
        #         ride.vehicle = driver.vehicle_type
        #         ride.capacity = driver.capacity
        #         ride.confirmedOrNot = True
        #         ride.save()
        #         shareuser = ride.sharer
        #         shareusermail = shareuser.email
        #         send_mail('Ride Confirmation', 'Your ride has been confirmed by a driver!', 'mylyft568@gmail.com',[shareusermail],fail_silently=False)


        user = ride.creater
        useremail = user.email
        send_mail('Ride Confirmation', 'Your ride has been confirmed by a driver!', 'mylyft568@gmail.com', [useremail], fail_silently=False)

    return render(request, 'myLift_app/driverRideSearch.html')

def completeRides(request, ride_id):
    driver = models.Driver.objects.filter(driver=request.user)[0]
    ride = models.Ride.objects.filter(id=ride_id)[0]
    if 'completed' in request.POST:
        ride.driver = request.user
        ride.completeOrNot = True
        ride.save()
        sharerides = models.ShareRide.objects.filter(ride=ride)
        print(sharerides)
        for shareride in sharerides:
            if shareride is not None:
                shareride.driver = request.user
                shareride.completeOrNot = True
                shareride.save()
        #except Exception as e:
            #return render(request, 'myLift_app/driverhomepage.html',{'driver':driver})


    return render(request, 'myLift_app/driverhomepage.html',{'driver':driver})

def showConfirmedOngoingRides(request):
    incompleterides = models.Ride.objects.filter(driver=request.user, completeOrNot=False)

    return render(request, 'myLift_app/showConfirmedOngoingRides.html', {'rides': incompleterides})

def showConfirmedRides(request):
    confirmedrides = models.Ride.objects.filter(driver=request.user)

    return render(request, 'myLift_app/showConfirmedRides.html', {'rides': confirmedrides})
