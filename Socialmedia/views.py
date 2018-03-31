from django.shortcuts import render, redirect
from signup.forms import UserLoginForm

def home(request):
    get_user = request.user
    username = get_user.username
    login_form = UserLoginForm(request.POST or None)
    if get_user.is_authenticated:
        return render(request,'signin/profile.html',{'name':username})
    else:
        message='message'
        print(message)
        return redirect("/login", {'login_form':login_form})
