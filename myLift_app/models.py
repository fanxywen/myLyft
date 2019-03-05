from django.db import models
from django import forms
from django.forms import ModelForm
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Driver(models.Model):
    driver = models.OneToOneField(User, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=200)
    licence = models.CharField(max_length=200)
    capacity = models.IntegerField(default=4)
    def __iter__(self):
        field_names = [f.name for f in self._meta.fields]
        for field_name in field_names:
            if field_name =="capacity":
                continue
            value = getattr(self, field_name, None)
            yield(field_name, value)

class Ride(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creater_ride_set')
    dest = models.CharField(max_length=200)
    datetime = models.DateTimeField()   # 20190101
    num_passenger = models.IntegerField(default=1)
    num_sharers = models.IntegerField(default=0)
    num_total = models.IntegerField(default=1)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'driver_ride_set', null=True) ## set to null
    vehicle = models.CharField(max_length=200, null=True)
    capacity = models.IntegerField(null=True)
    licence = models.CharField(max_length=200, null=True)
    shareOrNot = models.BooleanField()
    confirmedOrNot = models.BooleanField(default=False)
    completeOrNot = models.BooleanField(default=False)
    #driverinfo = models.OneToOneField(Driver, on_delete=models.CASCADE, related_name='confirmed_driver_info', null=True)
    def __iter__(self):
        field_names = [f.name for f in self._meta.fields]
        for field_name in field_names:
            if field_name == "id":
                continue
            value = getattr(self, field_name, None)
            yield (field_name, value)

    # def __iter__(self):
    #     for field_name in self._meta.get_fields():
    #         value = getattr(self, field_name, None)
    #         yield (field_name, value)

class ShareRide(models.Model):
    dest = models.CharField(max_length=200)
    datetime = models.DateTimeField()   # 20190101
    sharer = models.ForeignKey(User, on_delete=models.CASCADE)
    num_pass = models.IntegerField(default=1)
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='ride_shareride_set', blank=True, null=True)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver_share_ride_set', null=True)
    vehicle = models.CharField(max_length=200, null=True)
    capacity = models.IntegerField(null=True)
    licence = models.CharField(max_length=200, null=True)
    completeOrNot = models.BooleanField(default=False)
    confirmedOrNot = models.BooleanField(default=False)
    #driverinfo = models.OneToOneField(Driver, on_delete=models.CASCADE, related_name='confirmed_shareride_driver_info', null=True)
    def __iter__(self):
        field_names = [f.name for f in self._meta.fields]
        for field_name in field_names:
            if field_name == "id" or field_name == "ride":
                continue
            # if field_name == "num_pass":
            value = getattr(self, field_name, None)
            yield (field_name, value)



# class DriverEditableForm(ModelForm):
#      class Meta:
#          model = Ride
#          exclude = ['creater', 'num_passenger', 'num_total', 'num_sharers', 'confirmedOrNot', 'driver', 'datetime', 'dest', 'shareOrNot']
class PasswordChange(ModelForm):

    class Meta:
        model = User
        exclude = ['last_name','first_name', 'groups','user_permissions','is_staff','is_active','is_superuser', 'last_login', 'date_joined','password']
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(PasswordChange, self).save(commit=False)
        #user_profile = UserProfile(user=user)
        user.save()
        #user_profile.save()
        return user

class RideForm(ModelForm):
    # datetime = forms.DateTimeField(input_formats = ['%Y-%m-%d %H:%M'])
    #READONLY_FIELDS = ('completeOrNot')
    datetime = forms.DateTimeField(
        input_formats = ['%Y-%m-%d %H:%M:%S',],
        label='DateTime',
        widget = forms.widgets.TextInput()
        # widget=forms.widgets.DateTimeInput(attrs={'type':'date'}),
        # widget=forms.widgets.DateTimeInput(attrs={'type':'datetime-local'}),
    )
    class Meta:
        model = Ride
        exclude = ['creater', 'driver', 'num_sharers', 'num_total', 'confirmedOrNot', 'completeOrNot','vehicle', 'licence', 'capacity']

    # def __init__(self, readonly_form=False, *args, **kwargs):
    #     super(RideForm, self).__init__(*args, **kwargs)
    #     if readonly_form:
    #         for field in self.READONLY_FIELDS:
    #             self.fields[field].widget.attrs['readonly'] = True

    # def savemodel(self, request, commit=True):
    #     ride = super(RideForm,self).save(commit=False)
    #     ride.creater = request.user
    #     if commit:
    #         ride.save()
    #     return ride


class DriverForm(ModelForm):
    class Meta:
        model = Driver
        exclude = ['driver',]

class ShareRideForm(ModelForm):
    datetime = forms.DateTimeField(
        input_formats = ['%Y-%m-%d %H:%M:%S',],
        label='DateTime',
        widget = forms.widgets.TextInput()
    )
    class Meta:
        model = ShareRide
        exclude = ['ride', 'sharer', 'confirmedOrNot', 'completeOrNot', 'driver', 'vehicle', 'licence', 'capacity']

class DriverSearchForm(ModelForm):
    datetime = forms.DateTimeField(
        input_formats = ['%Y-%m-%d %H:%M:%S',],
        label='DateTime',
        widget = forms.widgets.TextInput()
    )
    class Meta:
        model = ShareRide
        exclude = ['ride', 'sharer', 'num_pass', 'driver', 'capacity', 'vehicle', 'licence', 'confirmedOrNot', 'completeOrNot']
