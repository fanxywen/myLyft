from django import forms

class RideForm(forms.Form):
    # class Meta:
    #     model = ride
    #     fields = ['dest', 'date', 'time', 'num_passenger', 'shareOrNot'
    # creater = forms.ForeignKey(User, on_delete=models.CASCADE)
    dest = forms.CharField()
    date = forms.CharField()
    time = forms.CharField()
    num_passenger = forms.IntegerField()
    # driver = forms.ForeignKey(User, on_delete=models.CASCADE)
    shareOrNot = forms.CharField()
    
