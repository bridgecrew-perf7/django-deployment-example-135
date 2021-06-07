from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout



# Create your views here.


def index(request):
    return render(request, 'basic_app/index.html')

def register(request):
    registerd = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            print('is valid')
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registerd = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        print("Request method was: GET")
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html', {
                                'user_form':user_form,
                             'profile_form':profile_form, 
                             'registerd':registerd, 
                             })



def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                HttpResponse("Account not active")
        else:
            print(f"{username} tried to log in with {password}")
            return HttpResponse("invalid log in details")
    else:
        return render(request, "basic_app/login.html", {})
        




@login_required
def user_logout(request):

    logout(request)
    return HttpResponseRedirect(reverse('index'))
    
