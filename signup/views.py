from django.shortcuts import render, redirect
from .forms import Register, ProfileInfo, UserLoginForm
from django.contrib.auth import (
        authenticate,
        login,
        logout,
        get_user_model,
    )
from .models import Profile

# Create your views here.

def login_view(request):
    login_form = UserLoginForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = authenticate(username=username,password=password)
        login(request, authenticate(username=username, password=password))
        return render(request, "signin/profile.html", {'username':username})
    return render(request,'registration/login.html',{'login_form':login_form})

def logout_view(request):
    logout(request)
    login_form = UserLoginForm(request.POST or None)
    return redirect("/login", {'login_form':login_form})

def register(request):
    form = Register(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        user_auth = authenticate(username=user.username,password=password)
        login(request, user_auth)
        return redirect("/profile")
    context = {"form":form}
    return render(request, "signin/register.html", context)

def profile(request):
    get_user = request.user
    username = get_user.username
    return render(request,'signin/profile.html',{'name':username})

















# registered = False
# if request.method == 'POST':
#     user_form = Register(request.POST)
#     profile_form = ProfileInfo(request.POST, request.FILES)
#
#     if user_form.is_valid() and profile_form.is_valid():
#         user = user_form.save()
#         user.set_password(user.password)
#         user.save()
#
#         username = user_form.cleaned_data.get('username')
#         raw_password = user_form.cleaned_data.get('password')
#
#         profile = profile_form.save(commit=False)
#         profile.user = user
#         profile.profile_pic = request.FILES['profile_pic']
#         profile.save()
#         login(request, authenticate(username=username, password=raw_password))
#         registered = True
#
#     username = user_form.cleaned_data.get('username')
#     raw_password = user_form.cleaned_data.get('password')
#     from django.contrib.auth import authenticate
#     user = authenticate(username=username, password=raw_password)
#     if user is not None:
#         return render(request,'signin/profile.html',{'name':username})
#     else:
#         return render(request, 'signin/profile.html', {'name':username, 'user_form': user_form, 'profile_form': profile_form })
#     user_form = Register(request.POST)
#     profile_form = ProfileInfo(request.POST, request.FILES)
