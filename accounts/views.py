# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from . import models
from django import forms
from django.contrib.auth import authenticate
# from django.views import generic


# class SignUp(generic.edit.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'accounts/signup.html'

# def signup(request):
#     if request.method == 'POST':
#         user = UserCreationForm(request.POST)
#         if user.is_valid():
#             user.save()
#             messages.success(request, 'Account created successfully')
#             success_url = reverse_lazy('login')
#             return HttpResponseRedirect(success_url)
#         else:
#             print("not valid")
#
#     else:
#         user = UserCreationForm()
#
#     return render(request, 'accounts/signup.html', {'form': user})

def signup(request):
    if request.method == 'POST':
        form = models.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            user = authenticate(username=username, password=raw_password)
            messages.success(request, 'Account created successfully')
            success_url = reverse_lazy('login')
            print('redirect')
            return HttpResponseRedirect(success_url)
        else:
            print("Invalid!")
    else:
        form = models.SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
